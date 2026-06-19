from http import HTTPStatus

from tracko.domain.shared.shared_exc import DomainException


class UserAlreadyInTeam(DomainException):
    status_code = HTTPStatus.CONFLICT
    detail = 'User is already a member of this team'


class UserNotInTeam(DomainException):
    status_code = HTTPStatus.NOT_FOUND
    detail = 'User is not a member of this team'
