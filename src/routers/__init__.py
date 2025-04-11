from fastapi import APIRouter, FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from core.config import config
from routers import v1

from . import base

ROUTER_VERSIONS = [
    v1,
]


def get_all_routers() -> APIRouter:
    router = APIRouter(prefix='/api')
    base.setup_router(router)

    for version in ROUTER_VERSIONS:
        version_router = version.get_router()
        router.include_router(version_router)

    return router


def setup_staticfiles(app: FastAPI) -> None:
    app.mount('/images', StaticFiles(directory=config.IMAGES_DIR))
    app.mount('/files', StaticFiles(directory=config.FILES_DIR))

    @app.get('/images/{filename}', tags=['Static Files'])
    def get_image(filename: str) -> RedirectResponse:
        return RedirectResponse(f'/images/{filename}')
    
    @app.get('/files/{filename}', tags=['Static Files'])
    def get_file(filename: str) -> RedirectResponse:
        return RedirectResponse(f'/files/{filename}')
