import pytest
from server import app, loadClubs, loadCompetitions


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            loadClubs()
            loadCompetitions()
        yield client


def test_functional_booking_workflow_part1(client):
    # Accéder à la page d'accueil
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data

    # Se connecter avec un email valide
    response = client.post("/showSummary", data={"email": "john@simplylift.co"})
    assert response.status_code == 200
    assert b"Welcome" in response.data

    # Accéder à la page de réservation
    response = client.get("/book/Fall%20Classic/Simply%20Lift")
    assert response.status_code == 200
    assert b"Booking" in response.data

    # Réserver des places
    response = client.post(
        "/purchasePlaces",
        data={"competition": "Fall Classic", "club": "Simply Lift", "places": "2"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data

    # Vérifier que les places ont été mises à jour
    response = client.get("/showSummary", follow_redirects=True)
    assert b"Number of Places: 11" in response.data
    assert b"Points available: 11" in response.data

    # Déconnexion
    response = client.get("/logout")
    assert response.status_code == 302
    assert b"You should be redirected automatically to the target URL" in response.data


def test_functional_booking_workflow_part2(client):
    # Accéder à la page d'accueil
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data

    # Se connecter avec un autre email valide
    response = client.post("/showSummary", data={"email": "kate@shelifts.co.uk"})
    assert response.status_code == 200
    assert b"Welcome" in response.data

    # Accéder à la page de réservation
    response = client.get("/book/Fall%20Classic/She%20Lifts")
    assert response.status_code == 200
    assert b"Booking" in response.data

    # Réserver des places
    response = client.post(
        "/purchasePlaces",
        data={"competition": "Fall Classic", "club": "She Lifts", "places": "1"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data

    # Vérifier que les places ont été mises à jour
    response = client.get("/showSummary", follow_redirects=True)
    assert b"Number of Places: 10" in response.data
    assert b"Points available: 11" in response.data

    # Déconnexion
    response = client.get("/logout")
    assert response.status_code == 302
    assert b"You should be redirected automatically to the target URL" in response.data
