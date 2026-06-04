from fastapi import FastAPI

from TS_TP.routers import task_router

app = FastAPI()

app.include_router(task_router.router)
