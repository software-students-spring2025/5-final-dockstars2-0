import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

    # 👇 FIRST: check login succeeded by checking something you know will be on your homepage
    assert b"Welcome" in login_response.data or b"Logout" in login_response.data

    # THEN: Access profile
    response = client.get('/profile', follow_redirects=True)

    # 👇 Instead of checking "Profile" text, check something like:
    assert b"My Boards" in response.data or b"Created Events" in response.data

    # Now create the board
    response = client.post('/create-board', data={
        'board_name': 'My Test Board'
    }, follow_redirects=True)

    # Validate creation
    from models import db
    board = db.folders.find_one({'name': 'My Test Board'})
    assert board is not None
