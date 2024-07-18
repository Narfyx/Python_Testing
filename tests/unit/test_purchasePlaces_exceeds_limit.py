import pytest
from server import app, competitions


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            yield client


def test_purchase_places_exceeds_limit(client):
    client.post("/showSummary", data={"email": "john@simplylift.co"})
    competition = next(c for c in competitions if c["name"] == "Fall Classic")
    competition["numberOfPlaces"] = "13"

    response = client.post(
        "/purchasePlaces",
        data={"competition": "Fall Classic", "club": "Simply Lift", "places": "14"},
    )
    assert response.status_code == 302
    response = client.get("/showSummary", follow_redirects=True)
    assert b"You not authorize to get more 12 places per competition" in response.data
