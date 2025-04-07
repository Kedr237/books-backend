from sqlalchemy.ext.asyncio import AsyncSession

from models import BookModel

from ..base import BaseManager


class BookManager(BaseManager[BookModel]):

    def __init__(self, session: AsyncSession):
        super().__init__(session, model=BookModel)
