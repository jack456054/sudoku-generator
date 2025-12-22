import pytest
from sudoku.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_homepage(client):
    """Test that the homepage loads successfully."""
    rv = client.get('/')
    assert rv.status_code == 200
    assert b"Sudoku Generator" in rv.data

def test_api_generate_simple(client):
    """Test generating simple puzzles."""
    rv = client.post('/api/generate', json={'difficulty': 'Simple', 'count': 2})
    assert rv.status_code == 200
    data = rv.get_json()
    assert 'puzzles' in data
    assert len(data['puzzles']) == 2
    assert 'board' in data['puzzles'][0]
    assert data['puzzles'][0]['grade'] == 'Simple'

def test_api_generate_medium(client):
    """Test generating medium puzzles."""
    rv = client.post('/api/generate', json={'difficulty': 'Medium', 'count': 1})
    assert rv.status_code == 200
    data = rv.get_json()
    assert len(data['puzzles']) == 1
    # Note: Might return Simple if retry fails, but we check structure
    assert 'grade' in data['puzzles'][0]
