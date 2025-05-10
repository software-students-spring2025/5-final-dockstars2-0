import pytest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_add_comment_to_event(client):
    # create user and event
    client.post('/signup', data={
        'username': 'commenter',
        'password': 'pass',
        'email': 'comment@test.com'
    }, follow_redirects=True)
    client.post('/login', data={
        'username': 'commenter',
        'password': 'pass'
    }, follow_redirects=True)
    
    from models import create_event, add_comment_to_event, db
    user = db.users.find_one({"username": "commenter"})
    event_id = create_event(str(user["_id"]), "Test Event", "desc", None, "2025-12-31", "City")

    add_comment_to_event(str(user["_id"]), str(event_id), "Test comment")
    comment = db.comments.find_one({"text": "Test comment"})
    assert comment is not None


def test_delete_event_by_id(client):
    from models import create_event, delete_event_by_id, db
    client.post('/signup', data={
        'username': 'deleter',
        'password': 'pass',
        'email': 'delete@test.com'
    }, follow_redirects=True)
    client.post('/login', data={
        'username': 'deleter',
        'password': 'pass'
    }, follow_redirects=True)

    user = db.users.find_one({"username": "deleter"})
    event_id = create_event(str(user["_id"]), "To Delete", "desc", None, "2025-12-31", "Someplace")
    delete_event_by_id(str(event_id))

    deleted = db.events.find_one({"_id": event_id})
    assert deleted is None


def test_update_event_by_id(client):
    from models import create_event, update_event_by_id, db
    client.post('/signup', data={
        'username': 'updater',
        'password': 'pass',
        'email': 'update@test.com'
    }, follow_redirects=True)
    client.post('/login', data={
        'username': 'updater',
        'password': 'pass'
    }, follow_redirects=True)

    user = db.users.find_one({"username": "updater"})
    event_id = create_event(str(user["_id"]), "Old Title", "desc", None, "2025-12-31", "Oldplace")
    
    update_event_by_id(str(event_id), "New Title", "New Desc", None, "2026-01-01", "Newplace", 40.0, -74.0)
    updated = db.events.find_one({"_id": event_id})
    assert updated["title"] == "New Title"
    assert updated["location"] == "Newplace"

def test_get_user_by_id(client):
    from models import get_user_by_id, db
    client.post('/signup', data={
        'username': 'profileuser',
        'password': 'pass',
        'email': 'profile@test.com'
    }, follow_redirects=True)

    user = db.users.find_one({"username": "profileuser"})
    user_info = get_user_by_id(str(user["_id"]))
    assert user_info["username"] == "profileuser"
    assert "profile_pic_url" in user_info

