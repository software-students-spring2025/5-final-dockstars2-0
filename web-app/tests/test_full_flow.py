import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import app
from bson.objectid import ObjectId
from models import db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def create_test_user(client):
    client.post('/signup', data={
        'username': 'realuser',
        'password': 'realpass'
    }, follow_redirects=True)
    client.post('/login', data={
        'username': 'realuser',
        'password': 'realpass'
    }, follow_redirects=True)

def test_real_event_flow(client):
    create_test_user(client)

    # Create event
    response_create = client.post('/create-event', data={
        'title': 'Real Event',
        'description': 'Real Description',
        'date': '2025-12-31',
        'location': 'Real City'
    }, follow_redirects=True)
    assert response_create.status_code == 200

    # Get event ID from database
    event = db.events.find_one({'title': 'Real Event'})
    assert event is not None
    event_id = str(event['_id'])

    # View event detail
    response_view = client.get(f'/event/{event_id}', follow_redirects=True)
    assert response_view.status_code == 200

    # Edit event
    response_edit = client.post(f'/event/{event_id}/edit', data={
        'title': 'Real Event Updated',
        'description': 'Updated Desc',
        'date': '2026-01-01',
        'location': 'Updated City'
    }, follow_redirects=True)
    assert response_edit.status_code == 200

    # Plan to attend
    response_plan = client.post(f'/event/{event_id}/plan', follow_redirects=True)
    assert response_plan.status_code == 200 or response_plan.status_code == 302

    # Maybe attend
    response_maybe = client.post(f'/event/{event_id}/maybe', follow_redirects=True)
    assert response_maybe.status_code == 200 or response_maybe.status_code == 302

    # Delete event
    response_delete = client.post(f'/event/{event_id}/delete', follow_redirects=True)
    assert response_delete.status_code == 200


