from http import HTTPStatus
from uuid import uuid4


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "email": "newuser@test.com",
            "password": "123456",
            "name": "New User",
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    data = response.json()

    assert data["id"] is not None
    assert data["email"] == "newuser@test.com"
    assert data["name"] == "New User"


def test_read_users(client, token_admin):
    response = client.get(
        "/users/",
        headers={"Authorization": f"Bearer {token_admin}"},
        params={"offset": 0, "limit": 10},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert "users" in data
    assert "total" in data
    assert "offset" in data
    assert "limit" in data


def test_read_me(client, token_admin):
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token_admin}"},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data["email"] is not None


def test_read_one_user(client, token_admin):
    # cria usuario
    create_response = client.post(
        "/users/",
        json={
            "email": "test2@test.com",
            "password": "123456",
            "name": "User Test",
        },
    )

    user_id = create_response.json()["id"]

    # busca usuario
    response = client.get(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {token_admin}"},
    )

    assert response.status_code == 200
    assert response.json()["email"] == "test2@test.com"


def test_delete_user(client, token_admin):
    # cria usuario
    response = client.post(
        "/users/",
        json={
            "email": "delete@test.com",
            "password": "123456",
            "name": "Delete User",
        },
    )

    user_id = response.json()["id"]

    # deleta usuario
    delete_response = client.delete(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {token_admin}"},
    )

    assert delete_response.status_code == 204