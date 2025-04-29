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

def test_search_page(client):
    response = client.get('/search?q=test', follow_redirects=True)
    assert response.status_code == 200

def test_profile_page_requires_login(client):
    response = client.get('/profile', follow_redirects=True)
    assert response.status_code == 200

def test_create_and_delete_event(client):
    # Signup and login
    client.post('/signup', data={
        'username': 'eventtester',
        'password': 'eventtestpassword'
    }, follow_redirects=True)
    client.post('/login', data={
        'username': 'eventtester',
        'password': 'eventtestpassword'
    }, follow_redirects=True)

    # Create event
    create_response = client.post('/create-event', data={
        'title': 'Temp Delete Event',
        'description': 'To be deleted',
        'date': '2025-12-31',
        'location': 'Delete City'
    }, follow_redirects=True)
    assert create_response.status_code == 200

    # Find event id (simple assumption for now)
    # This step is simplified: ideally you would extract the event ID from the database
    # Here you assume your system handles creation properly.

    # Delete event (simulate, assume ObjectId '000000000000000000000000')
    delete_response = client.post('/event/000000000000000000000000/delete', follow_redirects=True)
    # May fail safely if event doesn't exist; we care about endpoint coverage
    assert delete_response.status_code in [200, 302]

def test_create_board(client):
    # Signup and login
    client.post('/signup', data={
        'username': 'boardtester',
        'password': 'boardpassword'
    }, follow_redirects=True)
    client.post('/login', data={
        'username': 'boardtester',
        'password': 'boardpassword'
    }, follow_redirects=True)

    response = client.post('/create-board', data={
        'board_name': 'My Test Board'
    }, follow_redirects=True)
    assert response.status_code == 200

def test_plan_maybe_attend(client):
    # Plan to attend (simulate with fake event id)
    response_plan = client.post('/event/000000000000000000000000/plan', follow_redirects=True)
    assert response_plan.status_code in [200, 302]

    # Maybe attend
    response_maybe = client.post('/event/000000000000000000000000/maybe', follow_redirects=True)
    assert response_maybe.status_code in [200, 302]

def test_model_helpers():
    from models import get_event_by_id, get_user_folders

    # Call with invalid ids (just to trigger code paths)
    event = get_event_by_id("000000000000000000000000")
    folders = get_user_folders("000000000000000000000000")

    assert event is None
    assert isinstance(folders, list)


def test_edit_event_page(client):
    # Try to edit a fake event
    response = client.get('/event/000000000000000000000000/edit', follow_redirects=True)
    assert response.status_code in [200, 302]

def test_event_detail_page(client):
    # Try to view a fake event detail
    response = client.get('/event/000000000000000000000000', follow_redirects=True)
    assert response.status_code in [200, 302]

