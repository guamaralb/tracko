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