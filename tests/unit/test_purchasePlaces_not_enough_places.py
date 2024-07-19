import pytest
from server import app, competitions


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            yield client


def test_purchase_places_not_enough_places(client):
    client.post("/showSummary", data={"email": "john@simplylift.co"})
    competition = next(c for c in competitions if c["name"] == "Fall Classic")
    competition["numberOfPlaces"] = "1"

    response = client.post(
        "/purchasePlaces",
        data={"competition": "Fall Classic", "club": "Simply Lift", "places": "2"},
    )
    assert response.status_code == 302
    response = client.get("/showSummary", follow_redirects=True)
    assert (
        b"Not enough places available for the quantity you requested." in response.data
    )