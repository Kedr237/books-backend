from fastapi import APIRouter


def setup_router(router: APIRouter) -> None:
    @router.get('/')
    async def hello() -> str:
        return 'Hello world!'
