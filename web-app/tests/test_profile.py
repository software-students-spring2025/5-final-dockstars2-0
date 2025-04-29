import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unittest.mock import patch
from flask_login import login_user
from bson import ObjectId

from app import app
from models import db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_profile_requires_login(client):
    response = client.get('/profile', follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data



def test_create_board(client):
    with patch('routes.profile_routes.db.users.find_one') as mock_find_one, \
         patch('routes.profile_routes.db.folders.insert_one') as mock_insert_one:

        fake_user_id = "64b64c44bcf86cd799439011"  # ✅ 24-hex chars

        mock_find_one.return_value = {
            "_id": ObjectId(fake_user_id),
            "username": "boardtester",
            "email": "board@test.com",
            "created_events": [],
            "planning_events": [],
            "maybe_events": [],
            "attended_events": []
        }

        with client.session_transaction() as session:
            session['_user_id'] = fake_user_id  # ✅ use the same valid ID

        create_response = client.post(
            '/create-board',
            data={'board_name': 'My Test Board'},
            content_type='application/x-www-form-urlencoded',
            follow_redirects=False
        )

        assert create_response.status_code in (302, 303)

        mock_insert_one.assert_called_once()
