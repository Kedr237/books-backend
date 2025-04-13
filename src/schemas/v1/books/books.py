from fastapi import File, Form, HTTPException, UploadFile, status
from pydantic import field_validator

from ..base import (BaseCreationSchema, BaseModelSchema, BaseResponseSchema,
                    BaseUpdateSchema)


class BookSchema(BaseModelSchema):

    title: str
    description: str | None = None
    cover: str | None = None
    file: str


class BookCreationSchema(BaseCreationSchema):

    title: str = Form(...)
    description: str | None = Form(None)
    cover: UploadFile | str | None = File(None)
    file: UploadFile = File(...)


class BookCreationResponseSchema(BaseResponseSchema):

    book_id: int
    success: bool = True
    message: str = 'The book was successfully created.'


class BookUpdateSchema(BaseUpdateSchema):
    
    is_available: bool | str | None = Form(None)
    title: str | None = Form(None)
    description: str | None = Form(None)
    cover: UploadFile | str | None = File(None)
    file: UploadFile | str | None = File(None)


class BookUpdateResponseSchema(BaseResponseSchema):

    book_id: int
    success: bool = True
    message: str = 'The book was successfully updated.'
