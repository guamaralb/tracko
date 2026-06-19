from enum import Enum


class TaskStatusEnum(str, Enum):
    TODO = 'todo'
    IN_PROGESS = 'in_progress'
    CANCELLED = 'cancelled'
    DONE = 'done'
