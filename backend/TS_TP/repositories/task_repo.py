from sqlalchemy.orm import Session

from TS_TP.domain.task.task_models import TaskModel


class TaskRepository:
    def __init__(self, session: Session):
        self._session = session

    def add(self, new_task: TaskModel):
        self._session.add(new_task)
        self._session.flush()
        return new_task
