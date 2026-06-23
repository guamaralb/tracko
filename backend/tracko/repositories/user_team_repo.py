from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from tracko.domain.team.team_models import UserTeamModel
from tracko.domain.user_team.user_team_schemas import FilterUserTeamSchema


class UserTeamRepository:
    def __init__(self, session: Session):
        self._session = session

    def add(self, new_team: UserTeamModel) -> UserTeamModel:
        self._session.add(new_team)
        self._session.flush()
        return new_team

    def get_many(self, filter: FilterUserTeamSchema) -> tuple[Sequence[UserTeamModel], int]:
        query = select(UserTeamModel)

        if filter.user_id is not None:
            query = query.where(UserTeamModel.user_id == filter.user_id)

        if filter.team_id is not None:
            query = query.where(UserTeamModel.team_id == filter.team_id)

        if filter.role is not None:
            query = query.where(UserTeamModel.role == filter.role)

        total = self._session.scalar(select(func.count()).select_from(query.subquery()))

        teams = self._session.scalars(query.offset(filter.offset).limit(filter.limit))

        return teams.all(), total or 0

    def get_one(self, user_id: UUID, team_id: UUID) -> UserTeamModel | None:
        return self._session.scalar(
            select(UserTeamModel).where(
                UserTeamModel.user_id == user_id,
                UserTeamModel.team_id == team_id,
            )
        )

    def delete(self, user_team: UserTeamModel) -> None:
        self._session.delete(user_team)
        self._session.flush()
