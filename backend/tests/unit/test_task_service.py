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


def test_task_service_read_many():
    uow = MagicMock()
    limit = 10

    task = TaskModel(
        title='Task 1',
        user_id_creator=uuid4(),
        description='desc',
        start_date=None,
        end_date=None,
    )

    uow.tasks.get_many.return_value = ([task], 1)

    filter = FilterTaskSchema(offset=0, limit=limit)
    user = MagicMock()

    result = task_service_read_many(uow=uow, current_user=user, filter=filter)

    uow.tasks.get_many.assert_called_once_with(filter)

    assert result.total == 1
    assert len(result.tasks) == 1
    assert result.offset == 0
    assert result.limit == limit


def test_task_service_read_one_success():
    uow = MagicMock()

    task = TaskModel(
        title='Task 1',
        user_id_creator=uuid4(),
        description='desc',
        start_date=None,
        end_date=None,
    )

    task_id = uuid4()
    uow.tasks.get_one.return_value = task

    user = MagicMock()

    result = task_service_read_one(uow=uow, current_user=user, task_id=task_id)

    uow.tasks.get_one.assert_called_once_with(task_id)
    assert result.title == 'Task 1'


def test_task_service_read_one_not_found():
    uow = MagicMock()
    uow.tasks.get_one.return_value = None

    user = MagicMock()

    with pytest.raises(TaskNotFound):
        task_service_read_one(uow=uow, current_user=user, task_id=uuid4())