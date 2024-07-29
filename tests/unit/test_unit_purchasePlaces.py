import pytest
from flask import url_for
from server import app, loadCompetitions, competitions


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            loadCompetitions()
        yield client


def test_purchase_places_not_enough(client):
    client.post("/showSummary", data={"email": "john@simplylift.co"})

    competition = next(c for c in competitions if c["name"] == "Fall Classic")
    print(competition)
    competition["numberOfPlaces"] = "1"
    print(competition)
    response = client.post(
        "/purchasePlaces",
        data={"competition": "Fall Classic", "club": "She Lifts", "places": "2"},
    )

    assert response.status_code == 302
    assert response.headers["Location"] == url_for("showSummary", _external=False)

    response = client.get(url_for("showSummary"), follow_redirects=True)
    assert (
        b"Not enough places available for the quantity you requested." in response.data
    )
