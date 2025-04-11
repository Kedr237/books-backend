from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from core.config import config
from models import BookModel
from schemas import BookCreationResponseSchema, BookCreationSchema, BookSchema

from ..base import BaseService
from .manager import BookManager


class BookService(BaseService[BookModel, BookSchema]):

    def __init__(self, session):
        super().__init__(
            session,
            manager=BookManager(session),
            schema=BookSchema,
        )

    async def create(
            self,
            book: BookCreationSchema,
        ) -> BookCreationResponseSchema:
        cover_name = book.cover.filename
        file_name = book.file.filename

        cover_path = str(config.IMAGES_DIR / cover_name) if book.cover else None
        file_path = str(config.FILES_DIR / file_name)

        if cover_path:
            with open(cover_path, 'wb') as f:
                content = await book.cover.read()
                f.write(content)

        with open(file_path, 'wb') as f:
            content = await book.file.read()
            f.write(content)

        book_model = BookModel(
            title=book.title,
            description=book.description,
            cover=cover_name,
            file=file_name,
        )

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
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'An error occurred while creating the book. {e}',
            )
