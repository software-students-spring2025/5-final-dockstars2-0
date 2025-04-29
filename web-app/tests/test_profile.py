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
    with patch('models.db.users.find_one') as mock_find_one, \
         patch('routes.profile_routes.db.folders.insert_one') as mock_insert_one, \
         patch('flask_login.utils._get_user') as mock_current_user, \
         patch('flask_login.login_user') as mock_login_user:

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

        # Mock current user
        mock_current_user.return_value.is_authenticated = True
        mock_current_user.return_value.id = "fakeid123"

        # Mock login_user
        mock_login_user.return_value = None

        # Signup
        client.post('/signup', data={
            'username': 'boardtester',
            'password': 'boardpassword',
            'email': 'board@test.com'
        }, follow_redirects=True)

        # Login
        login_response = client.post('/login', data={
            'username': 'boardtester',
            'password': 'boardpassword'
        }, follow_redirects=True)

        assert login_response.status_code == 200

        # Create board (NO redirect following)
        create_response = client.post(
            '/create-board',
            data={'board_name': 'My Test Board'},
            content_type='application/x-www-form-urlencoded',
            follow_redirects=False
        )

        assert create_response.status_code in (302, 303)  # Expect redirect

        # ✅ Verify the board was inserted
        mock_insert_one.assert_called_once()

