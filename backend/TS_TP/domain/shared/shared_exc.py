from http import HTTPStatus


class DomainException(Exception):
    status_code: int = HTTPStatus.BAD_REQUEST
    detail: str = 'An error occurred'


class DomainValidationError(DomainException, ValueError):
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY
    detail = 'Validation error'
