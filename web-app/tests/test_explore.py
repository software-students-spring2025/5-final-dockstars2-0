import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_explore_homepage(client):
    response = client.get('/')
    assert response.status_code == 200

def test_search_no_query_redirects(client):
    response = client.get('/search', follow_redirects=True)
    assert response.status_code == 200
