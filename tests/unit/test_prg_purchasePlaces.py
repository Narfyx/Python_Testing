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
        data={"competition": "Spring Festival", "club": "Iron Temple", "places": "1"},
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

    # Vérifier que la session contient les informations nécessaires
    with client.session_transaction() as sess:
        assert sess["email"] == "john@simplylift.co"
        assert "club" in sess

    # Vérifier que le nombre de places a été mis à jour correctement
    competition = [c for c in competitions if c["name"] == "Spring Festival"][0]
    # print(competition)

    assert (
        int(competition["numberOfPlaces"]) == 24
    )  # Suppose que le nombre initial de places était 25
