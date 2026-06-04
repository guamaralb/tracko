from http import HTTPStatus

from TS_TP.domain.shared.shared_exc import DomainException


class UserNotFound(DomainException):
    status_code = HTTPStatus.NOT_FOUND
    detail = 'User not found'
