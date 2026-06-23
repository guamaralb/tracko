from unittest.mock import MagicMock

import pytest

from tracko.domain.auth.auth_exc import WrongCredentials
from tracko.domain.auth.auth_schemas import TokenSchema
from tracko.domain.auth.auth_services import login_for_access_token_service
from tracko.domain.user.user_models import UserModel
