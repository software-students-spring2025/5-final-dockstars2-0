import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from models import db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_signup_page_loads(client):
    response = client.get('/signup')
    assert response.status_code == 200
    assert b"Sign Up" in response.data

def test_login_page_loads(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b"Login" in response.data

def test_signup_username_taken(client):
    client.post('/signup', data={
        'username': 'dupeuser',
        'password': 'password',
        'email': 'dupeuser@test.com'
    }, follow_redirects=True)

    response = client.post('/signup', data={
        'username': 'dupeuser',
        'password': 'anotherpassword',
        'email': 'anotheremail@test.com'
    }, follow_redirects=True)

    from models import db
    user_count = db.users.count_documents({'username': 'dupeuser'})
    assert user_count == 1


def test_logout(client):
    client.post('/signup', data={
        'username': 'logoutuser',
        'password': 'logoutpass',
        'email': 'logout@test.com'
    }, follow_redirects=True)

    client.post('/login', data={
        'username': 'logoutuser',
        'password': 'logoutpass'
    }, follow_redirects=True)

    response = client.get('/logout', follow_redirects=True)

    # ✅ Instead of flash text, check status and page
    assert response.status_code == 200
    assert b"Login" in response.data







