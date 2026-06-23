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
