from sqlalchemy.orm import Mapped, mapped_column

from ..base import BaseModel


class BookModel(BaseModel):

    __tablename__ = 'books'

    title: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=True)
    cover: Mapped[str] = mapped_column(nullable=True)
    file: Mapped[str] = mapped_column(nullable=False)
