from fastapi import APIRouter

from . import hello

router = APIRouter(prefix='/hello', tags=['hello'])

hello.setup_router(router)
