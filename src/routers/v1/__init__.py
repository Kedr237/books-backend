from fastapi import APIRouter

from . import base, books

router = APIRouter(prefix='/v1', tags=['v1'])

base.setup_router(router)

MODULES = [
    books,
]


def get_router() -> APIRouter:
    for module in MODULES:
        router.include_router(module.router)

    return router
