from sqlalchemy.orm import Session

from tracko.repositories.task_repo import TaskRepository
from tracko.repositories.team_repo import TeamRepository
from tracko.repositories.user_repo import UserRepository
from tracko.repositories.user_team_repo import UserTeamRepository


class UnitOfWork:
    def __init__(self, session: Session):
        self._session = session

        self.tasks = TaskRepository(session)
        self.users = UserRepository(session)
        self.teams = TeamRepository(session)
        self.user_teams = UserTeamRepository(session)

    def __enter__(self) -> 'UnitOfWork':
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if exc_type:
            self._session.rollback()
        else:
            self._session.commit()
