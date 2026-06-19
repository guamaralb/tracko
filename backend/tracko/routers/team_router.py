from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query

from tracko.core.deps import CurrentUserDep, SessionDep
from tracko.core.uow import UnitOfWork
from tracko.domain.team.team_schemas import (
    FilterTeamSchema,
    TeamAddMemberSchema,
    TeamCreateSchema,
    TeamMemberReadOneSchema,
    TeamReadManySchema,
    TeamReadOneSchema,
)
from tracko.domain.team.team_services import (
    team_service_add_member,
    team_service_create,
    team_service_read_many,
    team_service_read_one,
    team_service_remove_member,
)

router = APIRouter(prefix='/teams', tags=['teams'])


@router.post('/', status_code=HTTPStatus.CREATED)
def team_route_create(
    session: SessionDep,
    current_user: CurrentUserDep,
    data: TeamCreateSchema,
) -> TeamReadOneSchema:
    with UnitOfWork(session) as uow:
        return team_service_create(
            uow=uow, current_user=current_user, data=data
        )


@router.get('/', status_code=HTTPStatus.OK)
def team_route_read_many(
    session: SessionDep,
    current_user: CurrentUserDep,
    filter: Annotated[FilterTeamSchema, Query()],
) -> TeamReadManySchema:
    with UnitOfWork(session) as uow:
        return team_service_read_many(
            uow=uow, current_user=current_user, filter=filter
        )


@router.get('/{team_id}', status_code=HTTPStatus.OK)
def team_route_read_one(
    session: SessionDep,
    current_user: CurrentUserDep,
    team_id: UUID,
) -> TeamReadOneSchema:
    with UnitOfWork(session) as uow:
        return team_service_read_one(
            uow=uow, current_user=current_user, team_id=team_id
        )


##################################################
# UserTeam routes
##################################################


@router.post('/{team_id}/members', status_code=HTTPStatus.CREATED)
def team_route_add_member(
    session: SessionDep,
    current_user: CurrentUserDep,
    team_id: UUID,
    data: TeamAddMemberSchema,
) -> TeamMemberReadOneSchema:
    with UnitOfWork(session) as uow:
        return team_service_add_member(
            uow=uow, current_user=current_user, team_id=team_id, data=data
        )


@router.delete(
    '/{team_id}/members/{user_id}', status_code=HTTPStatus.NO_CONTENT
)
def team_route_remove_member(
    session: SessionDep,
    current_user: CurrentUserDep,
    team_id: UUID,
    user_id: UUID,
) -> None:
    with UnitOfWork(session) as uow:
        team_service_remove_member(
            uow=uow,
            current_user=current_user,
            team_id=team_id,
            user_id=user_id,
        )
