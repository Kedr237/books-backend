from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db_session
from schemas import (BaseDeleteResponseSchema, BookCreationResponseSchema,
                     BookCreationSchema, BookSchema)
from services import BookService


def setup_router(router: APIRouter) -> None:
    @router.post('/')
    async def create_book(
        book: BookCreationSchema = Depends(),
        db_session: AsyncSession = Depends(get_db_session),
    ) -> BookCreationResponseSchema:
        service = BookService(db_session)
        return await service.create(book)

    @router.get('/{id}')
    async def get_book_by_id(
        id: int,
        db_session: AsyncSession = Depends(get_db_session),
    ) -> BookSchema:
        service = BookService(db_session)
        return await service.get_by_id(id)

    @router.delete('/{id}')
    async def delete_book_by_id(
        id: int,
        db_session: AsyncSession = Depends(get_db_session),
    ) -> BaseDeleteResponseSchema:
        service = BookService(db_session)
        return await service.delete_by_id(id)
