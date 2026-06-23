from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from tracko.domain.auth.auth_exc import PermissionDenied
from tracko.domain.team.team_exc import TeamNotFound
from tracko.domain.team.team_models import TeamModel
from tracko.domain.team.team_schemas import (
    FilterTeamSchema,
    TeamAddMemberSchema,
    TeamCreateSchema,
)
from tracko.domain.team.team_services import (
    team_service_add_member,
    team_service_create,
    team_service_read_many,
    team_service_read_one,
    team_service_remove_member,
)
from tracko.domain.user.user_enums import UserRoleEnum
from tracko.domain.user.user_exc import UserNotFound
from tracko.domain.user_team.user_team_exc import (
    UserNotInTeam,
)