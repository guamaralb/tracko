from http import HTTPStatus

from fastapi.testclient import TestClient

from tests.utils import is_valid_datetime


def test_create_user_returns_created(client: TestClient, token_admin: str):
    response = client.post(
        '/users/',
        headers={'Authorization': f'Bearer {token_admin}'},
        json={
            'email': 'email@test.com',
            'role': 'admin',
            'name': 'Test Name',
            'password': 'test password',
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    data = response.json()

    assert data['email'] == 'email@test.com'
    assert 'password_hash' not in data
    assert data['name'] == 'Test Name'
    assert data['is_active']
    assert is_valid_datetime(data['created_at'])
    assert is_valid_datetime(data['modified_at'])
