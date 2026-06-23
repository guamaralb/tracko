from uuid import UUID

from tracko.core.security import get_password_hash
from tracko.core.uow import UnitOfWork
from tracko.domain.user.user_exc import UserNotFound
from tracko.domain.user.user_models import UserModel
from tracko.domain.user.user_schemas import (
    FilterUserSchema,
    UserCreateSchema,
    UserReadManySchema,
    UserReadOneSchema,
)


def user_service_create(
    *, uow: UnitOfWork, data: UserCreateSchema
) -> UserReadOneSchema:
    password_hash = get_password_hash(data.password)

    new_user = UserModel(
        email=data.email,
        password_hash=password_hash,
        name=data.name,
    )
    user_db = uow.users.add(new_user)
    return UserReadOneSchema.model_validate(user_db)


def user_service_read_many(
    *, uow: UnitOfWork, current_user: UserModel, filter: FilterUserSchema
) -> UserReadManySchema:
    users_db, total = uow.users.get_many(filter)

    return UserReadManySchema(
        users=[UserReadOneSchema.model_validate(u) for u in users_db],
        total=total,
        offset=filter.offset,
        limit=filter.limit,
    )


def user_service_read_one(
    *, uow: UnitOfWork, current_user: UserModel, user_id: UUID
) -> UserReadOneSchema:
    user_db = uow.users.get_one(user_id)

    if not user_db:
        raise UserNotFound()
    else:
        return UserReadOneSchema.model_validate(user_db)


def user_service_delete(
    *, uow: UnitOfWork, current_user: UserModel, user_id: UUID
) -> None:
    db_user = uow.users.get_one(user_id)
    if not db_user:
        raise UserNotFound()

    uow.users.delete(db_user)
