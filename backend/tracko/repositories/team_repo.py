from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from tracko.domain.team.team_models import TeamModel
from tracko.domain.team.team_schemas import FilterTeamSchema


class TeamRepository:
    def __init__(self, session: Session):
        self._session = session

    def add(self, new_team: TeamModel) -> TeamModel:
        self._session.add(new_team)
        self._session.flush()
        return new_team

    def get_many(
        self, filter: FilterTeamSchema
    ) -> tuple[Sequence[TeamModel], int]:
        query = select(TeamModel)

        if filter.name is not None:
            query = query.where(TeamModel.name.contains(filter.name))

        if filter.description is not None:
            query = query.where(
                TeamModel.description.contains(filter.description)
            )

        total = self._session.scalar(
            select(func.count()).select_from(query.subquery())
        )

        teams = self._session.scalars(
            query.offset(filter.offset).limit(filter.limit)
        )

        return teams.all(), total or 0

    def get_one(self, team_id: UUID) -> TeamModel | None:
        team = self._session.scalar(
            select(TeamModel).where(TeamModel.id == team_id)
        )
        return team
