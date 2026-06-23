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


def test_team_service_create():
    uow = MagicMock()

    uow.teams.add.side_effect = lambda team: team

    user = MagicMock()
    user.id = uuid4()

    data = TeamCreateSchema(name='Team A', description='desc')

    result = team_service_create(uow=uow, current_user=user, data=data)

    uow.teams.add.assert_called_once()

    assert result.name == 'Team A'
    assert result.description == 'desc'


def test_team_service_read_many():
    limit = 10
    uow = MagicMock()

    team = TeamModel(
        name='Team A', description='desc', user_id_creator=uuid4()
    )

    uow.teams.get_many.return_value = ([team], 1)

    filter = FilterTeamSchema(offset=0, limit=limit)
    user = MagicMock()

    result = team_service_read_many(uow=uow, current_user=user, filter=filter)

    uow.teams.get_many.assert_called_once_with(filter)

    assert result.total == 1
    assert len(result.teams) == 1
    assert result.offset == 0
    assert result.limit == limit


def test_team_service_read_one_success():
    uow = MagicMock()

    team = TeamModel(
        name='Team A', description='desc', user_id_creator=uuid4()
    )

    team_id = uuid4()
    uow.teams.get_one.return_value = team

    user = MagicMock()

    result = team_service_read_one(uow=uow, current_user=user, team_id=team_id)

    uow.teams.get_one.assert_called_once_with(team_id)

    assert result.name == 'Team A'


def test_team_service_read_one_not_found():
    uow = MagicMock()
    uow.teams.get_one.return_value = None

    user = MagicMock()

    with pytest.raises(TeamNotFound):
        team_service_read_one(uow=uow, current_user=user, team_id=uuid4())


def test_team_service_add_member_success():
    uow = MagicMock()

    uow.teams.get_one.return_value = MagicMock()

    current_user = MagicMock()
    current_user.id = uuid4()

    uow.user_teams.get_one.side_effect = [
        MagicMock(role=UserRoleEnum.MANAGER),  # current user in team
        None,  # target user not in team
    ]

    uow.users.get_one.return_value = MagicMock()

    uow.user_teams.add.side_effect = lambda x: x

    data = TeamAddMemberSchema(user_id=uuid4(), role=UserRoleEnum.COLLABORATOR)

    result = team_service_add_member(
        uow=uow, current_user=current_user, team_id=uuid4(), data=data
    )

    uow.user_teams.add.assert_called_once()
    assert result is not None


def test_team_service_add_member_permission_denied():
    uow = MagicMock()

    uow.teams.get_one.return_value = MagicMock()

    current_user = MagicMock()
    current_user.id = uuid4()

    uow.user_teams.get_one.return_value = None  # não é manager

    data = TeamAddMemberSchema(user_id=uuid4(), role=UserRoleEnum.COLLABORATOR)

    with pytest.raises(PermissionDenied):
        team_service_add_member(
            uow=uow, current_user=current_user, team_id=uuid4(), data=data
        )


def test_team_service_add_member_user_not_found():
    uow = MagicMock()

    uow.teams.get_one.return_value = MagicMock()

    current_user = MagicMock()
    current_user.id = uuid4()

    uow.user_teams.get_one.return_value = MagicMock(role=UserRoleEnum.MANAGER)

    uow.users.get_one.return_value = None

    data = TeamAddMemberSchema(user_id=uuid4(), role=UserRoleEnum.COLLABORATOR)

    with pytest.raises(UserNotFound):
        team_service_add_member(
            uow=uow, current_user=current_user, team_id=uuid4(), data=data
        )


def test_team_service_remove_member_not_in_team():
    uow = MagicMock()

    uow.teams.get_one.return_value = MagicMock()

    current_user = MagicMock()
    current_user.id = uuid4()

    uow.user_teams.get_one.side_effect = [
        MagicMock(role=UserRoleEnum.MANAGER),  # current user
        None,  # target user not in team
    ]

    with pytest.raises(UserNotInTeam):
        team_service_remove_member(
            uow=uow,
            current_user=current_user,
            team_id=uuid4(),
            user_id=uuid4(),
        )


def test_add_member_team_not_found():
    uow = MagicMock()

    uow.teams.get_one.return_value = None

    current_user = MagicMock()
    current_user.id = uuid4()

    data = TeamAddMemberSchema(user_id=uuid4(), role=UserRoleEnum.COLLABORATOR)

    with pytest.raises(TeamNotFound):
        team_service_add_member(
            uow=uow,
            current_user=current_user,
            team_id=uuid4(),
            data=data
        )


def test_team_service_create_sets_creator():
    uow = MagicMock()

    captured = {}

    def fake_add(team):
        captured["team"] = team
        return team

    uow.teams.add.side_effect = fake_add

    current_user = MagicMock()
    current_user.id = uuid4()

    data = TeamCreateSchema(name="Team A", description="desc")

    team_service_create(uow=uow, current_user=current_user, data=data)

    assert captured["team"].user_id_creator == current_user.id
