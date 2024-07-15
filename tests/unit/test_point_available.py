import pytest
from flask import url_for
from server import app, loadCompetitions, competitions, session


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            loadCompetitions()
        yield client


def test_purchase_places(client):
    # Simuler une connexion initiale pour stocker l'email dans la session
    client.post("/showSummary", data={"email": "admin@irontemple.com"})
    club_before = session.get("club")["points"]

    # Simuler une requête POST pour acheter des places
    response = client.post(
        "http://localhost/purchasePlaces",
        data={"competition": "Fall Classic", "club": "Iron Temple", "places": "1"},
    )

    # Suivre la redirection
    response = client.get("/showSummary", follow_redirects=True)

    # Vérifier que la page welcome.html est affichée correctement
    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data

    club_after = session.get("club")["points"]
    assert int(club_before) - int(club_after) == 1
