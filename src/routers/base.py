from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from core.config import config


def setup_router(router: APIRouter) -> None:
    @router.get('/', include_in_schema=False)
    async def root() -> RedirectResponse:
        return RedirectResponse(config.DOCS_URL)
