import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unittest.mock import patch


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
         patch('models.db.folders.insert_one') as mock_insert_one, \
         patch('flask_login.utils._get_user') as mock_current_user:

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

        # Mock logged-in user
        mock_current_user.return_value.id = "fakeid123"

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

        # Create board
        create_response = client.post('/create-board', data={
            'board_name': 'My Test Board'
        }, follow_redirects=True)

        assert create_response.status_code == 200

        # Verify the board was created
        mock_insert_one.assert_called_once()
