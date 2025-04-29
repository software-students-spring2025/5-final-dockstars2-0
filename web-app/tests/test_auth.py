import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_signup_page_loads(client):
    response = client.get('/signup')
    assert response.status_code == 200
    assert b"Sign Up" in response.data

def test_login_page_loads(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b"Login" in response.data


