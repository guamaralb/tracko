from http import HTTPStatus

from tracko.domain.shared.shared_exc import DomainException


class TaskNotFound(DomainException):
    status_code = HTTPStatus.NOT_FOUND
    detail = 'Task not found'
