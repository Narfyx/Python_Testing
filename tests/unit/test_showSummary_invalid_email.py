import pytest
from server import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            yield client


def test_showSummary_invalid_email(client):
    response = client.post("/showSummary", data={"email": "invalid@example.com"})
    assert response.status_code == 400
    assert b"Email not found" in response.data
