import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    """Test the home endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['message'] == "Welcome to DevSecOps Python Application"
    assert json_data['status'] == "running"

def test_health(client):
    """Test the health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == "healthy"

def test_get_users(client):
    """Test GET request to /api/user"""
    response = client.get('/api/user')
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'users' in json_data
    assert len(json_data['users']) > 0

def test_create_user(client):
    """Test POST request to /api/user"""
    response = client.post('/api/user', 
                          json={'username': 'testuser'},
                          content_type='application/json')
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data['message'] == "User created"
    assert json_data['user'] == "testuser"

def test_get_data(client):
    """Test the data endpoint"""
    response = client.get('/api/data')
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'data' in json_data
    assert len(json_data['data']) == 3
    assert json_data['data'][0]['id'] == 1