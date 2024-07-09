import pytest
from flask import session
from server import app, loadClubs, loadCompetitions


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            # Charger les données nécessaires
            loadClubs()
            loadCompetitions()
        yield client


def test_index_page(client):
    """Tester l'accès à la page d'accueil."""
    response = client.get("/")
    assert response.status_code == 200


def test_book_page_requires_login(client):
    """Tester l'accès à la page de réservation sans être connecté."""
    response = client.get("/book/Spring%20Festival/Iron%20Temple")
    assert response.status_code == 401
    assert b"You should be redirected automatically to the target URL" in response.data


def test_book_page_with_login(client):
    """Tester l'accès à la page de réservation après connexion."""
    with client.session_transaction() as sess:
        sess["email"] = "john@simplylift.co"
    response = client.get("/book/Spring%20Festival/Iron%20Temple")
    assert response.status_code == 200
    assert b"Booking" in response.data


def test_logout(client):
    """Tester la déconnexion."""
    with client.session_transaction() as sess:
        sess["email"] = "john@simplylift.co"
    response = client.get("/logout")
    assert response.status_code == 302  # Redirection vers l'index
    with client.session_transaction() as sess:
        assert "email" not in sess
