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
    client.post('/signup', data={
        'username': 'boardtester',
        'password': 'boardpassword',
        'email': 'board@test.com'
    }, follow_redirects=True)

    client.post('/login', data={
        'username': 'boardtester',
        'password': 'boardpassword'
    }, follow_redirects=True)

    response = client.post('/create-board', data={
        'board_name': 'My Test Board'
    }, follow_redirects=True)

    
    from models import db
    board = db.folders.find_one({'name': 'My Test Board'})
    assert board is not None




