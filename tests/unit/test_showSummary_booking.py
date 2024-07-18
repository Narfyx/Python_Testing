import pytest
from flask import session, url_for
from server import app, loadClubs


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            loadClubs()
        yield client


def test_showSummary_post_valid_email(client):
    response = client.post("/showSummary", data={"email": "john@simplylift.co"})
    assert response.status_code == 200
    assert b"Welcome" in response.data
    assert b"Spring Festival" in response.data  # Future competition
    assert b"Fall Classic" in response.data  # Future competition
    assert b"Festival 2020" not in response.data  # Past competition
    assert b"test" not in response.data  # Past competition
