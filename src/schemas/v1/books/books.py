from fastapi import File, Form, HTTPException, UploadFile, status
from pydantic import field_validator

from ..base import (BaseCreationSchema, BaseModelSchema, BaseResponseSchema,
                    BaseUpdateSchema)
from ..handlers import (handle_file, handle_form_bool, handle_form_int,
                        handle_form_str)


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

    @field_validator('description', mode='before')
    @classmethod
    def validate_form_str(cls, value):
        return handle_form_str(value)

    @field_validator('cover', mode='before')
    @classmethod
    def validate_file(cls, value):
        return handle_file(value)


class BookCreationResponseSchema(BaseResponseSchema):

    book_id: int
    success: bool = True
    message: str = 'The book was successfully created.'


class BookUpdateSchema(BaseUpdateSchema):
    
    id: int | str = Form(...)
    is_available: bool | str | None = Form(None)
    title: str | None = Form(None)
    description: str | None = Form(None)
    cover: UploadFile | str | None = File(None)
    file: UploadFile | str | None = File(None)

    @field_validator('id', mode='before')
    @classmethod
    def validate_id(cls, value):
        handled_id = handle_form_int(value)
        if not handled_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='The field [id] cannot be empty and must contain only digits.',
            )
        return handled_id

    @field_validator('is_available', mode='before')
    @classmethod
    def validate_form_bool(cls, value):
        return handle_form_bool(value)

    @field_validator('title', 'description', mode='before')
    @classmethod
    def validate_form_str(cls, value):
        return handle_form_str(value)

    @field_validator('cover', 'file', mode='before')
    @classmethod
    def validate_file(cls, value):
        return handle_file(value)
