from .v1.base import BaseSchema, BaseDeleteResponseSchema
from .v1.books.books import (BookCreationResponseSchema, BookCreationSchema,
                             BookSchema)

__all__ = [
    'BaseDeleteResponseSchema',
    'BaseSchema',
    'BookCreationResponseSchema',
    'BookCreationSchema',
    'BookSchema',
]
