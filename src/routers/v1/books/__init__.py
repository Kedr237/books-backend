from fastapi import APIRouter

from . import books

router = APIRouter(prefix='/books', tags=['books'])

books.setup_router(router)
