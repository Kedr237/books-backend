from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from core.config import config
from models import BookModel
from schemas import (BookCreationResponseSchema, BookCreationSchema,
                     BookSchema, BookUpdateResponseSchema, BookUpdateSchema)

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
        cover_name = book.cover.filename if book.cover else None
        file_name = book.file.filename

        if cover_name:
            with open(config.IMAGES_DIR / cover_name, 'wb') as f:
                content = await book.cover.read()
                f.write(content)

        with open(config.FILES_DIR / file_name, 'wb') as f:
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
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'An error occurred while creating the book.',
            )

    async def update(self, id: int, book: BookUpdateSchema) -> BookUpdateResponseSchema:
        try:
            old_book = await self.manager.get_by_id(id)
            if not old_book:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'The book with id [{id}] not found.',
                )
            
            data_to_update = {
                col: value for col, value in book.to_dict().items()
                if value
            }

            if isinstance(book.cover, str):
                data_to_update['cover'] = book.cover

            if book.cover:
                old_cover = old_book.cover or None
                if old_cover:
                    old_cover_path = config.IMAGES_DIR / old_cover
                    old_cover_path.unlink()

                cover_name = book.cover.filename
                with open(config.IMAGES_DIR / cover_name, 'wb') as f:
                    content = await book.cover.read()
                    f.write(content)
                data_to_update['cover'] = cover_name

            if book.file:
                old_file_path = config.FILES_DIR / old_book.file
                old_file_path.unlink()

                file_name = book.file.filename
                with open(config.FILES_DIR / file_name, 'wb') as f:
                    content = await book.file.read()
                    f.write(content)
                data_to_update['file'] = file_name

            if not data_to_update:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='No data provided for update.',
                )
            
            await self.manager.update(id, data_to_update)
            return BookUpdateResponseSchema(book_id=id)
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
                detail=f'An error occurred while updating the book.',
            )
