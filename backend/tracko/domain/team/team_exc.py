from http import HTTPStatus

from tracko.domain.shared.shared_exc import DomainException


class TeamNotFound(DomainException):
    status_code = HTTPStatus.NOT_FOUND
    detail = 'Team not found'
