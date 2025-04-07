from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from models import BookModel
from schemas import BookSchema, BookCreationResponseSchema, BookCreationSchema

from ..base import BaseService
from .manager import BookManager


class BookService(BaseService[BookModel, BookSchema]):

    def __init__(self, session):
        super().__init__(
            session,
            manager=BookManager(session),
            schema=BookSchema,
        )

    async def create(self, book: BookCreationSchema) -> BookCreationResponseSchema:
        book_model = BookModel(**book.to_dict())

        try:
            book_created = await self.manager.add_one(book_model)
            response = BookCreationResponseSchema(book_id=book_created.id)
            return response
        except IntegrityError as e:
            if 'books_title_key' in str(e):
                # Add logger.
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'A book with title [{book.title}] already exists.',
                )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='An error occurred while creating the book.',
            )
