from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from tracko.domain.user.user_models import UserModel
from tracko.domain.user.user_schemas import FilterUserSchema


class UserRepository:
    def __init__(self, _session: Session):
        self._session = _session

    def add(self, new_user: UserModel) -> UserModel:
        self._session.add(new_user)
        self._session.flush()
        return new_user

    def get_many(
        self, filter: FilterUserSchema
    ) -> tuple[Sequence[UserModel], int]:
        query = select(UserModel)

        if filter.name is not None:
            query = query.where(UserModel.name.contains(filter.name))

        if filter.email is not None:
            query = query.where(UserModel.email.contains(filter.email))

        total = self._session.scalar(
            select(func.count()).select_from(query.subquery())
        )

        users = self._session.scalars(
            query.offset(filter.offset).limit(filter.limit)
        )

        return users.all(), total or 0

    def get_one(self, user_id: UUID) -> UserModel | None:
        user = self._session.scalar(
            select(UserModel).where(UserModel.id == user_id)
        )
        return user

    def delete(self, db_user: UserModel) -> None:
        self._session.delete(db_user)
        self._session.flush()
