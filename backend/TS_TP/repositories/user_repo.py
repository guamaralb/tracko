from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from TS_TP.domain.user.user_models import UserModel


class UserRepository:
    def __init__(self, session: Session):
        self._session = session

    def add(self, new_user: UserModel):
        self._session.add(new_user)
        self._session.flush()
        return new_user

    def get_one(self, user_id: UUID):
        user = self._session.scalar(
            select(UserModel).where(UserModel.id == user_id)
        )
        return user
