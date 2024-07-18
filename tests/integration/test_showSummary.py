import pytest
from server import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_showSummary_empty_email(client):
    response = client.post("/showSummary", data={"email": ""})
    assert response.status_code == 400
    assert b"Email is required" in response.data


def test_showSummary_invalid_email(client):
    response = client.post("/showSummary", data={"email": "invalid@example.com"})
    assert response.status_code == 400
    assert b"Email not found" in response.data


def test_showSummary_valid_email(client):
    # Assumes there's a valid club with email 'valid@example.com' in clubs
    response = client.post("/showSummary", data={"email": "john@simplylift.co"})
    assert response.status_code == 200
    assert b"Welcome" in response.data
