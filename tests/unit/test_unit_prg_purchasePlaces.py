import pytest
from flask import session
from server import app, competitions


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            # Charger les données nécessaires
            competitions
        yield client


def test_purchase_places_post_redirect_get(client):
    # Simuler une connexion initiale pour stocker l'email dans la session
    client.post("/showSummary", data={"email": "john@simplylift.co"})

    # Simuler une requête POST pour acheter des places
    response = client.post(
        "http://localhost/purchasePlaces",
        data={"competition": "Fall Classic", "club": "Iron Temple", "places": "0"},
    )

    # Vérifier que la réponse est une redirection
    assert response.status_code == 302
    assert response.headers["Location"] == "/showSummary"

    # Suivre la redirection
    response = client.get("/showSummary", follow_redirects=True)

    # Vérifier que la page welcome.html est affichée correctement
    assert response.status_code == 200
    assert b"Welcome" in response.data
    assert b"Great-booking complete!" in response.data
