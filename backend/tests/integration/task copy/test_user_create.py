from http import HTTPStatus

from fastapi.testclient import TestClient

from tests.utils import is_valid_datetime


def test_create_user_returns_created(client: TestClient):
    response = client.post(
        '/users/',
        headers={},
        json={
            'email': 'email@test.com',
            'pwd_hash': 'Test Hash',
            'name': 'Test Name',
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    data = response.json()

    assert data['email'] == 'email@test.com'
    assert data['pwd_hash'] == 'Test Hash'
    assert data['name'] == 'Test Name'
    assert data['is_active']
    assert is_valid_datetime(data['created_at'])
    assert is_valid_datetime(data['modified_at'])
