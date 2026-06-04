from datetime import datetime
from uuid import UUID


def is_valid_uuid(value: str, version: int = 4):
    try:
        UUID(value, version=version)
        return True
    except ValueError:
        return False


def is_valid_datetime(value: str) -> bool:
    """
    Verifica se a string é um datetime ISO 8601 válido.
    Retorna True se válido, False caso contrário.
    """
    try:
        datetime.fromisoformat(value)
        return True
    except ValueError:
        return False
