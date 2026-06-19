import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from tracko.app import app
from tracko.core.database import get_session, table_registry
from tracko.core.security import get_password_hash
from tracko.core.settings import settings
from tracko.domain.user.user_enums import UserRoleEnum
from tracko.domain.user.user_models import UserModel


@pytest.fixture
def test_engine():
    engine = create_engine(
        settings.TEST_DATABASE_URL,
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)
    yield engine
    table_registry.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def session(test_engine: Engine):
    with Session(test_engine) as session:
        yield session


@pytest.fixture
def client(
    session: Session, test_engine: Engine, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.setattr('tracko.core.database.engine', test_engine)
    monkeypatch.setattr('tracko.app.engine', test_engine)
    monkeypatch.setattr('tracko.app.seed_first_admin_user', lambda _: None)

    def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


# Users
@pytest.fixture
def user_admin(session: Session) -> UserModel:
    password = 'senhadoadmin'

    user_db = UserModel(
        email='test_admin@test.com',
        name='Test Admin',
        role=UserRoleEnum.ADMIN,
        password_hash=get_password_hash(password),
    )

    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    user_db.clean_password = password  # type: ignore[attr-defined]

    return user_db


@pytest.fixture
def token_admin(client: TestClient, user_admin: UserModel) -> str:
    response = client.post(
        '/auth/token',
        data={
            'username': user_admin.email,
            'password': user_admin.clean_password,  # type: ignore[attr-defined]
        },
    )

    token = response.json()['access_token']

    return token
