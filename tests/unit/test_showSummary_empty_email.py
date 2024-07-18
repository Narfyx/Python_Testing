import pytest
from server import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            yield client


def test_showSummary_empty_email(client):
    response = client.post("/showSummary", data={"email": ""})
    assert response.status_code == 400
    assert b"Email is required" in response.data
