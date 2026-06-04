from sqlalchemy.orm import Session

from TS_TP.repositories.task_repo import TaskRepository


class UnitOfWork:
    def __init__(self, session: Session):
        self._session = session

        self.tasks = TaskRepository(session)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type:
            self._session.rollback()
        else:
            self._session.commit()
