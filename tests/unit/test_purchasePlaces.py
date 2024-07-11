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

    competition = next(c for c in competitions if c["name"] == "Spring Festival")

    response = client.post(
        "/purchasePlaces",
        data={"competition": "Spring Festival", "club": "Simply Lift", "places": "26"},
    )

    assert response.status_code == 302
    assert response.headers["Location"] == url_for("showSummary", _external=False)

    response = client.get(url_for("showSummary"), follow_redirects=True)
    assert (
        b"Not enough places available for the quantity you requested." in response.data
    )

    competition = next(c for c in competitions if c["name"] == "Spring Festival")

    assert int(competition["numberOfPlaces"]) == 25


def test_purchase_places_success(client):
    client.post("/showSummary", data={"email": "john@simplylift.co"})

    competition = next(c for c in competitions if c["name"] == "Spring Festival")
    print(f"Nombre de places initial: {competition['numberOfPlaces']}")

    # Avant la requête POST
    print("*" * 100)
    print("Avant la requête POST pour réserver des places:")
    print(f"Compétition: {competition['name']}")
    print(f"Nombre de places avant réservation: {competition['numberOfPlaces']}")
    print("*" * 100)

    response = client.post(
        "/purchasePlaces",
        data={"competition": "Spring Festival", "club": "Simply Lift", "places": "25"},
        follow_redirects=True,
    )

    # Après la requête POST
    print("*" * 100)
    print("Après la requête POST pour réserver des places:")
    print(f"Statut de la réponse: {response.status_code}")
    print(f"Corps de la réponse: {response.data}")
    print("*" * 100)

    assert (
        response.status_code == 200
    )  # La redirection a été suivie, donc le statut devrait être 200

    assert b"Great-booking complete!" in response.data

    competition = next(c for c in competitions if c["name"] == "Spring Festival")
    print(f"Nombre de places après réservation: {competition['numberOfPlaces']}")

    assert int(competition["numberOfPlaces"]) == 0
