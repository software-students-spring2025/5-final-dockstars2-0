import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_explore_homepage(client):
    response = client.get('/')
    assert response.status_code == 200

def test_search_page(client):
    client.post('/signup', data={
        'username': 'searchuser',
        'password': 'searchpass',
        'email': 'search@test.com'
    }, follow_redirects=True)

    client.post('/login', data={
        'username': 'searchuser',
        'password': 'searchpass'
    }, follow_redirects=True)

    response = client.get('/search?q=test')


    assert response.status_code == 200



