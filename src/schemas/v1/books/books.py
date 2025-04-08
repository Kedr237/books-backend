from fastapi import File, Form, UploadFile

from ..base import BaseCreationSchema, BaseModelSchema, BaseResponseSchema


class BookSchema(BaseModelSchema):

    title: str
    description: str | None = None
    cover: str | None = None
    file: str


class BookCreationSchema(BaseCreationSchema):

    title: str = Form(...)
    description: str | None = Form(None)
    file: UploadFile = File(...)
    cover: UploadFile | str | None = File(None)


class BookCreationResponseSchema(BaseResponseSchema):

    book_id: int
    success: bool = True
    message: str = 'The book was successfully created.'
