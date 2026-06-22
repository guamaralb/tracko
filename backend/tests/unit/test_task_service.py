from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from tracko.domain.task.task_exc import TaskNotFound
from tracko.domain.task.task_models import TaskModel
from tracko.domain.task.task_schemas import (
    FilterTaskSchema,
    TaskCreateSchema,
)
from tracko.domain.task.task_services import (
    task_service_create,
    task_service_delete,
    task_service_read_many,
    task_service_read_one,
)


def test_task_service_create():
    uow = MagicMock()

    uow.tasks.add.side_effect = lambda task: task  # simula salvar e retornar

    user = MagicMock()
    user.id = uuid4()

    data = TaskCreateSchema(
        title='Test Task',
        description='desc',
        start_date=None,
        end_date=None,
    )

    result = task_service_create(uow=uow, current_user=user, data=data)

    uow.tasks.add.assert_called_once()

    assert result.title == 'Test Task'
    assert result.description == 'desc'