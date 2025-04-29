import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unittest.mock import patch
from flask_login import login_user

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

        # Mock database user
        mock_find_one.return_value = {
            "_id": "fakeid123",
            "username": "boardtester",
            "email": "board@test.com",
            "created_events": [],
            "planning_events": [],
            "maybe_events": [],
            "attended_events": []
        }

        # --- Set up a user in the session manually ---
        with client.session_transaction() as session:
            session['_user_id'] = "fakeid123"  # <- Flask-Login reads this!

        # --- Now no need to mock _get_user or login_user at all! ---

        # Create board
        create_response = client.post(
            '/create-board',
            data={'board_name': 'My Test Board'},
            content_type='application/x-www-form-urlencoded',
            follow_redirects=False
        )

        assert create_response.status_code in (302, 303)  # Expect redirect

        # ✅ Now the insert should happen
        mock_insert_one.assert_called_once()
