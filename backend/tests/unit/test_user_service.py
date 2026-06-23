from unittest.mock import MagicMock
from uuid import uuid4

import pytest

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

def test_user_service_create():
    uow = MagicMock()

    uow.users.add.side_effect = lambda user: user

    data = UserCreateSchema(
        email='test@test.com', password='123456', name='Test User'
    )

    current_user = MagicMock()

    result = user_service_create(uow=uow, current_user=current_user, data=data)

    uow.users.add.assert_called_once()

    assert result.email == 'test@test.com'
    assert result.name == 'Test User'


def test_user_service_read_many():
    limit = 10
    uow = MagicMock()

    user = UserModel(email='a@a.com', name='User A', password_hash='hash')

    uow.users.get_many.return_value = ([user], 1)

    filter = FilterUserSchema(offset=0, limit=limit)
    current_user = MagicMock()

    result = user_service_read_many(
        uow=uow, current_user=current_user, filter=filter
    )

    uow.users.get_many.assert_called_once_with(filter)

    assert result.total == 1
    assert len(result.users) == 1
    assert result.offset == 0
    assert result.limit == limit

def test_user_service_read_one_success():
    uow = MagicMock()

    user = UserModel(email='a@a.com', name='User A', password_hash='hash')

    user_id = uuid4()
    uow.users.get_one.return_value = user

    current_user = MagicMock()

    result = user_service_read_one(
        uow=uow, current_user=current_user, user_id=user_id
    )

    uow.users.get_one.assert_called_once_with(user_id)

    assert result.email == 'a@a.com'


def test_user_service_read_one_not_found():
    uow = MagicMock()
    uow.users.get_one.return_value = None

    current_user = MagicMock()

    with pytest.raises(UserNotFound):
        user_service_read_one(
            uow=uow, current_user=current_user, user_id=uuid4()
        )