from sqlalchemy.orm import Session

from tracko.repositories.task_repo import TaskRepository
from tracko.repositories.user_repo import UserRepository


class UnitOfWork:
    def __init__(self, session: Session):
        self._session = session

        self.tasks = TaskRepository(session)
        self.users = UserRepository(session)

    def __enter__(self) -> 'UnitOfWork':
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if exc_type:
            self._session.rollback()
        else:
            self._session.commit()
