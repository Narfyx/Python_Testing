import pytest
from server import app, clubs, competitions


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            yield client


def test_purchase_places_success(client):
    client.post("/showSummary", data={"email": "john@simplylift.co"})
    club = next(c for c in clubs if c["name"] == "Simply Lift")
    competition = [c for c in competitions if c["name"] == "Fall Classic"][0]
    club["points"] = "1"
    competition["numberOfPlaces"] = "1"
    response = client.post(
        "/purchasePlaces",
        data={"competition": "Fall Classic", "club": "Simply Lift", "places": "1"},
    )
    assert response.status_code == 302
    response = client.get("/showSummary", follow_redirects=True)
    assert b"Great-booking complete!" in response.data

    assert int(club["points"]) == 0
    assert int(competition["numberOfPlaces"]) == 0
