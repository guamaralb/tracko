from http import HTTPStatus

from tracko.domain.shared.shared_exc import DomainException


class InvalidToken(DomainException):
    status_code = HTTPStatus.UNAUTHORIZED
    detail = 'Invalid token'
