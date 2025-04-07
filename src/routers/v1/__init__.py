from fastapi import APIRouter

from . import base, hello

router = APIRouter(prefix='/v1', tags=['v1'])

base.setup_router(router)

MODULES = [
    hello,
]


def get_router() -> APIRouter:
    for module in MODULES:
        router.include_router(module.router)

    return router
