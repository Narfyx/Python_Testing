import pytest
from server import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            yield client


def test_showSummary_valid_email(client):
    response = client.post("/showSummary", data={"email": "john@simplylift.co"})
    assert response.status_code == 200
    assert b"Welcome" in response.data
