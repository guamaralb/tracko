from http import HTTPStatus

from tracko.domain.shared.shared_exc import DomainException


class WrongCredentials(DomainException):
    status_code = HTTPStatus.UNAUTHORIZED
    detail = 'Wrong email or password'


class PermissionDenied(DomainException):
    status_code = HTTPStatus.FORBIDDEN
    detail = 'Not enough permissions'
