def test_user_authentication(client):
    response = client.post('/auth/login', json={'username': 'test', 'password': 'test'})
    assert response.status_code == 200
    assert 'token' in response.json

def test_invalid_auth(client):
    response = client.post('/auth/login', json={'username': 'wrong', 'password': 'wrong'})
    assert response.status_code == 401
    assert 'error' in response.json