def test_home(client):
    response = client.get('/')
    assert response.status_code == 200


def test_add(client):
    response = client.get('/catalog')
    assert response.status_code == 200
