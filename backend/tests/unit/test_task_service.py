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