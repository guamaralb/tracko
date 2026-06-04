from http import HTTPStatus

from TS_TP.domain.shared.shared_exc import DomainException


class TaskNotFound(DomainException):
    status_code = HTTPStatus.NOT_FOUND
    detail = 'Task not found'
