import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import app
from bson.objectid import ObjectId

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_signup_and_login(client):
    # Signup
    response = client.post('/signup', data={
        'username': 'testuser123',
        'password': 'testpassword123'
    }, follow_redirects=True)
    assert response.status_code == 200

    # Logout
    client.get('/logout')

    # Login
    response = client.post('/login', data={
        'username': 'testuser123',
        'password': 'testpassword123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome" in response.data

def test_create_event(client):
    # First log in (you could simulate or assume already logged in)
    response = client.post('/login', data={
        'username': 'testuser123',
        'password': 'testpassword123'
    }, follow_redirects=True)

    # Create Event
    response = client.post('/create-event', data={
        'title': 'Test Event',
        'description': 'This is a test event.',
        'date': '2025-12-31',
        'location': 'New York City'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Event created successfully!" in response.data

def test_explore_search(client):
    response = client.get('/search?q=test', follow_redirects=True)
    assert response.status_code == 200
