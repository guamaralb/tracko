from uuid import UUID

from tracko.core.uow import UnitOfWork
from tracko.domain.auth.auth_exc import PermissionDenied
from tracko.domain.team.team_exc import TeamNotFound
from tracko.domain.team.team_models import TeamModel
from tracko.domain.team.team_schemas import (
    FilterTeamSchema,
    TeamAddMemberSchema,
    TeamCreateSchema,
    TeamMemberReadOneSchema,
    TeamReadManySchema,
    TeamReadOneSchema,
)
from tracko.domain.user.user_enums import UserRoleEnum
from tracko.domain.user.user_exc import UserNotFound
from tracko.domain.user.user_models import UserModel
from tracko.domain.user_team.user_team_exc import (
    UserAlreadyInTeam,
    UserNotInTeam,
)
from tracko.domain.user_team.user_team_models import UserTeamModel


def team_service_create(
    *, uow: UnitOfWork, current_user: UserModel, data: TeamCreateSchema
) -> TeamReadOneSchema:
    new_team = TeamModel(
        name=data.name,
        description=data.description,
        user_id_creator=current_user.id,
    )
    team_db = uow.teams.add(new_team)

    return TeamReadOneSchema.model_validate(team_db)


def team_service_read_many(
    *, uow: UnitOfWork, current_user: UserModel, filter: FilterTeamSchema
) -> TeamReadManySchema:
    teams_db, total = uow.teams.get_many(filter)

    return TeamReadManySchema(
        teams=[TeamReadOneSchema.model_validate(t) for t in teams_db],
        total=total,
        offset=filter.offset,
        limit=filter.limit,
    )


def team_service_read_one(
    *, uow: UnitOfWork, current_user: UserModel, team_id: UUID
) -> TeamReadOneSchema:
    team_db = uow.teams.get_one(team_id)
    if not team_db:
        raise TeamNotFound()
    return TeamReadOneSchema.model_validate(team_db)


def team_service_delete(
    *, uow: UnitOfWork, current_user: UserModel, team_id: UUID
) -> None:
    db_team = uow.users.get_one(team_id)
    if not db_team:
        raise TeamNotFound()

    uow.users.delete(db_team)


##################################################
# UserTeam services
##################################################


def team_service_add_member(
    *,
    uow: UnitOfWork,
    current_user: UserModel,
    team_id: UUID,
    data: TeamAddMemberSchema,
) -> TeamMemberReadOneSchema:
    db_team = uow.teams.get_one(team_id)
    if not db_team:
        raise TeamNotFound()

    db_current_user_team = uow.user_teams.get_one(current_user.id, team_id)
    if (not db_current_user_team) or (
        db_current_user_team.role != UserRoleEnum.MANAGER
    ):
        raise PermissionDenied()

    db_target_user = uow.users.get_one(data.user_id)
    if not db_target_user:
        raise UserNotFound()

    db_target_user_team = uow.user_teams.get_one(data.user_id, team_id)
    if db_target_user_team:
        raise UserAlreadyInTeam()

    new_user_team = UserTeamModel(
        user_id=data.user_id, team_id=team_id, role=data.role
    )

    user_team_db = uow.user_teams.add(new_user_team)
    return TeamMemberReadOneSchema.model_validate(user_team_db)


def team_service_remove_member(
    *,
    uow: UnitOfWork,
    current_user: UserModel,
    team_id: UUID,
    user_id: UUID,
) -> None:
    db_team = uow.teams.get_one(team_id)
    if not db_team:
        raise TeamNotFound()

    db_current_user_team = uow.user_teams.get_one(current_user.id, team_id)
    if (not db_current_user_team) or (
        db_current_user_team.role != UserRoleEnum.MANAGER
    ):
        raise PermissionDenied()

    db_target_user_team = uow.user_teams.get_one(user_id, team_id)
    if not db_target_user_team:
        raise UserNotInTeam()

    uow.user_teams.delete(db_target_user_team)
