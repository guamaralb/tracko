from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from tracko.core.database import engine, table_registry
from tracko.domain.seeds.seed_users import seed_first_admin_user
from tracko.domain.task.task_models import TaskModel  # noqa: F401
from tracko.domain.team.team_models import TeamModel  # noqa: F401
from tracko.domain.user.user_models import UserModel  # noqa: F401
from tracko.domain.users_tasks.users_tasks_models import (
    UserTaskModel,  # noqa: F401
)
from tracko.routers import auth_router, task_router, team_router, user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    table_registry.metadata.create_all(engine)
    with Session(engine) as session:
        seed_first_admin_user(session)
        session.commit()
    yield


app = FastAPI(lifespan=lifespan)

# 1. Defina a lista de origens permitidas (quem pode chamar sua API)
origins = [
    'http://localhost:5173',  # Sua aplicação frontend Vite local
    'http://127.0.0.1:5173',  # Variação comum do localhost
    # "https://seu-dominio.com",
]

# 2. Adicione o middleware do CORS na aplicação
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# 3. Inclua seus roteadores normalmente
app.include_router(auth_router.router)
app.include_router(task_router.router)
app.include_router(team_router.router)
app.include_router(user_router.router)


@app.get('/')
def read_root():
    return {'message': 'Tracko API is running'}
