from fastapi import APIRouter

router = APIRouter(prefix='/tasks', tags=['tasks'])

@router.post(
    '/'
)
def task_create():
    return {'oi'}