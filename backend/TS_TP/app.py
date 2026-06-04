from contextlib import asynccontextmanager

from fastapi import FastAPI

from TS_TP.core.database import engine, table_registry
from TS_TP.domain.task.task_models import TaskModel  # noqa: F401
from TS_TP.routers import task_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    table_registry.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(task_router.router)
