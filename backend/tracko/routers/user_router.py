from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query

from tracko.core.deps import CurrentUserDep, SessionDep
from tracko.core.uow import UnitOfWork
from tracko.domain.user.user_schemas import (
    FilterUserSchema,
    UserCreateSchema,
    UserReadManySchema,
    UserReadOneSchema,
)
from tracko.domain.user.user_services import (
    user_service_create,
    user_service_delete,
    user_service_read_many,
    user_service_read_one,
)

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', status_code=HTTPStatus.CREATED)
def user_route_create(
    session: SessionDep,
    data: UserCreateSchema,
) -> UserReadOneSchema:
    with UnitOfWork(session) as uow:
        return user_service_create(uow=uow, data=data)


@router.get('/', status_code=HTTPStatus.OK)
def user_route_read_many(
    session: SessionDep,
    current_user: CurrentUserDep,
    filter: Annotated[FilterUserSchema, Query()],
) -> UserReadManySchema:
    with UnitOfWork(session) as uow:
        return user_service_read_many(
            uow=uow, current_user=current_user, filter=filter
        )


@router.get('/me', status_code=HTTPStatus.OK)
def user_route_read_me(
    session: SessionDep,
    current_user: CurrentUserDep,
) -> UserReadOneSchema:
    with UnitOfWork(session) as uow:
        return user_service_read_one(
            uow=uow,
            current_user=current_user,
            user_id=current_user.id,
        )


@router.get('/{user_id}', status_code=HTTPStatus.OK)
def user_route_read_one(
    session: SessionDep,
    current_user: CurrentUserDep,
    user_id: UUID,
) -> UserReadOneSchema:
    with UnitOfWork(session) as uow:
        return user_service_read_one(
            uow=uow,
            current_user=current_user,
            user_id=user_id,
        )


@router.delete('/{user_id}', status_code=HTTPStatus.NO_CONTENT)
def team_route_remove_member(
    session: SessionDep,
    current_user: CurrentUserDep,
    user_id: UUID,
) -> None:
    with UnitOfWork(session) as uow:
        user_service_delete(
            uow=uow,
            current_user=current_user,
            user_id=user_id,
        )
