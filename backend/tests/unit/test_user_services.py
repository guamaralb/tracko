from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

# Importamos a sua exceção personalizada!
from tracko.domain.user.user_exc import UserNotFound
from tracko.domain.user.user_models import UserModel
from tracko.domain.user.user_schemas import (
    FilterUserSchema,
    UserCreateSchema,
)
from tracko.domain.user.user_services import (
    user_service_create,
    user_service_delete,
    user_service_read_many,
    user_service_read_one,
)


# --- FIXTURES ---
@pytest.fixture
def mock_uow():
    uow = MagicMock()
    uow.users.reset_mock()
    return uow


@pytest.fixture
def dummy_user():
    user = MagicMock(spec=UserModel)
    user.id = uuid4()
    user.name = "username"
    user.email = "name@email.com"
    user.password_hash = "hashed_password"
    return user


# --- TESTES DE CRIAÇÃO ---

# O @patch "sequestra" a função get_password_hash só durante este teste
@patch("tracko.domain.user.user_services.get_password_hash")
def test_user_service_create_success(mock_get_hash, mock_uow, dummy_user):
    # Simula o retorno da função de hash
    mock_get_hash.return_value = "hashed_password"

    schema_in = UserCreateSchema(
        name="username",
        email="name@email.com",
        password="senha123"
    )

    mock_uow.users.add.return_value = dummy_user

    result = user_service_create(uow=mock_uow, data=schema_in)

    # Garante que a senha foi "hasheada" antes de salvar
    mock_get_hash.assert_called_once_with("senha123")
    mock_uow.users.add.assert_called_once()
    assert result.email == "name@email.com"
    assert result.id == dummy_user.id


# --- TESTES DE LEITURA (UM USUÁRIO) ---

def test_user_service_read_one_success(mock_uow, dummy_user):
    mock_uow.users.get_one.return_value = dummy_user

    result = user_service_read_one(
        uow=mock_uow,
        current_user=dummy_user,
        user_id=dummy_user.id
    )

    mock_uow.users.get_one.assert_called_once_with(dummy_user.id)
    assert result.id == dummy_user.id


def test_user_service_read_one_not_found(mock_uow, dummy_user):
    mock_uow.users.get_one.return_value = None

    # Agora esperando exatamente a exceção que você criou: UserNotFound
    with pytest.raises(UserNotFound):
        user_service_read_one(
            uow=mock_uow,
            current_user=dummy_user,
            user_id=uuid4()
        )


# --- TESTES DE LEITURA (VÁRIOS USUÁRIOS) ---

def test_user_service_read_many_success(mock_uow, dummy_user):
    filter_schema = FilterUserSchema(offset=0, limit=10)
    mock_uow.users.get_many.return_value = ([dummy_user], 1)

    result = user_service_read_many(
        uow=mock_uow, current_user=dummy_user, filter=filter_schema
    )

    mock_uow.users.get_many.assert_called_once_with(filter_schema)
    assert result.total == 1
    assert len(result.users) == 1


# --- TESTES DE EXCLUSÃO ---

def test_user_service_delete_success(mock_uow, dummy_user):
    mock_uow.users.get_one.return_value = dummy_user

    user_service_delete(
        uow=mock_uow, current_user=dummy_user, user_id=dummy_user.id)

    mock_uow.users.delete.assert_called_once_with(dummy_user)


def test_user_service_delete_not_found(mock_uow, dummy_user):
    mock_uow.users.get_one.return_value = None

    with pytest.raises(UserNotFound):
        user_service_delete(
            uow=mock_uow, current_user=dummy_user, user_id=uuid4())

    mock_uow.users.delete.assert_not_called()
