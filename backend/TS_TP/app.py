from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.orm import Session

from TS_TP.core.database import engine, table_registry
from TS_TP.domain.seeds.seed_users import seed_first_admin_user
from TS_TP.domain.task.task_models import TaskModel  # noqa: F401
from TS_TP.domain.user.user_models import UserModel  # noqa: F401
from TS_TP.domain.users_tasks.users_tasks_models import (
    UserTaskModel,  # noqa: F401
)
from TS_TP.routers import auth_router, task_router, user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    table_registry.metadata.create_all(engine)
    with Session(engine) as session:
        seed_first_admin_user(session)
        session.commit()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(task_router.router)
app.include_router(user_router.router)
app.include_router(auth_router.router)
