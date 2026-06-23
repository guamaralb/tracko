from unittest.mock import MagicMock

import pytest

from tracko.domain.auth.auth_exc import WrongCredentials
from tracko.domain.auth.auth_schemas import TokenSchema
from tracko.domain.auth.auth_services import login_for_access_token_service
from tracko.domain.user.user_models import UserModel


def test_login_success(monkeypatch):
    session = MagicMock()

    user = UserModel(
        email='test@test.com', password_hash='any_hash', name='Test'
    )

    session.scalar.return_value = user

    form_data = MagicMock()
    form_data.username = 'test@test.com'
    form_data.password = '123456'

    monkeypatch.setattr(
        'tracko.domain.auth.auth_services.verify_password', lambda p, h: True
    )

    monkeypatch.setattr(
        'tracko.domain.auth.auth_services.create_access_token',
        lambda data: 'fake_token',
    )

    result = login_for_access_token_service(form_data, session)

    assert isinstance(result, TokenSchema)
    assert result.access_token == 'fake_token'
    assert result.token_type == 'bearer'

    session.scalar.assert_called_once()


def test_login_user_not_found():
    session = MagicMock()
    session.scalar.return_value = None

    form_data = MagicMock()
    form_data.username = 'notfound@test.com'
    form_data.password = '123456'

    with pytest.raises(WrongCredentials):
        login_for_access_token_service(form_data, session)


def test_login_wrong_password(monkeypatch):
    session = MagicMock()

    user = UserModel(
        email='test@test.com', password_hash='hashed_password', name='Test'
    )

    session.scalar.return_value = user

    form_data = MagicMock()
    form_data.username = 'test@test.com'
    form_data.password = 'wrong'

    monkeypatch.setattr(
        'tracko.domain.auth.auth_services.verify_password', lambda p, h: False
    )

    with pytest.raises(WrongCredentials):
        login_for_access_token_service(form_data, session)
