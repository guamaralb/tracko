from http import HTTPStatus


def test_login_success(client, user_admin):
    response = client.post(
        '/auth/token',
        data={
            'username': user_admin.email,
            'password': user_admin.clean_password,
        },
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert 'access_token' in data
    assert data['token_type'] == 'bearer'
    assert isinstance(data['access_token'], str)
    assert len(data['access_token']) > 0


def test_login_user_not_found(client):
    response = client.post(
        '/auth/token',
        data={
            'username': 'notfound@test.com',
            'password': '123456',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED

    data = response.json()
    assert data['detail'] == 'Credenciais inválidas. Verifique seu usuário e senha.'


def test_login_wrong_password(client, user_admin):
    response = client.post(
        '/auth/token',
        data={
            'username': user_admin.email,
            'password': 'wrong_password',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED

    data = response.json()
    assert data['detail'] == 'Credenciais inválidas. Verifique seu usuário e senha.'
