from http import HTTPStatus

from tracko.domain.shared.shared_exc import DomainException


class UserNotFound(DomainException):
    status_code = HTTPStatus.NOT_FOUND
    detail = 'User not found'


class EmailAlreadyInUse(DomainException):
    status_code = HTTPStatus.CONFLICT
    detail = 'Email already in use by another user'


class UserNotActive(DomainException):
    status_code = HTTPStatus.FORBIDDEN
    detail = 'User not active'
