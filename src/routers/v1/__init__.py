from fastapi import APIRouter

from . import books

router = APIRouter(prefix='/v1')

MODULES = [
    books,
]


def get_router() -> APIRouter:
    for module in MODULES:
        router.include_router(module.router)

    return router
