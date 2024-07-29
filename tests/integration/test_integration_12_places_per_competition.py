import pytest
from flask import url_for
from server import app, loadCompetitions, competitions, session, request


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            loadCompetitions()
        yield client


def test_purchase_places_with_13_places(client):
    # Simuler une connexion initiale pour stocker l'email dans la session
    client.post("/showSummary", data={"email": "john@simplylift.co"})
    club_before = session.get("club")["points"]

    print(club_before)

    # Simuler une requête POST pour acheter des places
    response = client.post(
        "http://localhost/purchasePlaces",
        data={"competition": "Fall Classic", "club": "Iron Temple", "places": "13"},
    )
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    # Suivre la redirection
    response = client.get("/showSummary", follow_redirects=True)

    # Vérifier que la page welcome.html est affichée correctement
    assert response.status_code == 200
    print(f"CLUB == {session.get("club")["points"]}")
    print(f"COMPETITION == {competition["numberOfPlaces"]}")

    if (int(session.get("club")["points"]) and int(competition["numberOfPlaces"])) == 13:
        print('TRUE')

    assert b"You not authorize to get more 12 places per competition" in response.data
