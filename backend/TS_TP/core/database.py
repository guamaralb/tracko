from sqlalchemy import create_engine
from sqlalchemy.orm import Session, registry

from TS_TP.core.settings import settings

table_registry = registry()
engine = create_engine(settings.DATABASE_URL, echo=False)


def get_session():  # pragma: no cover
    with Session(engine) as session:
        yield session
