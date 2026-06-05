from http import HTTPStatus

from TS_TP.domain.shared.shared_exc import DomainException


class InvalidToken(DomainException):
    status_code = HTTPStatus.UNAUTHORIZED
    detail = 'Invalid token'
