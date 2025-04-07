from typing import Type, List

from sqlalchemy import delete, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import Executable

from models import BaseModel
from schemas import BaseSchema


class SessionMixin:

    def __init__(self, session: AsyncSession):
        self.session = session


class BaseService(SessionMixin):
    ...


class BaseManager[TModel: BaseModel, TSchema: BaseSchema](SessionMixin):

    def __init__(self, session: AsyncSession, model: Type[TModel], schema: Type[TSchema]):
        super().__init__(session)
        self.model = model
        self.schema = schema

    async def add_one(self, model: TModel) -> TSchema | None:
        try:
            self.session.add(model)
            await self.session.commit()
            await self.session.refresh(model)
            return self.schema(**model.to_dict())
        except SQLAlchemyError:
            await self.session.rollback()
            # Add logger.
            raise

    async def get_one(self, select_statement: Executable) -> TModel | None:
        try:
            entry = await self.session.execute(select_statement)
            return entry.scalar()
        except SQLAlchemyError:
            # Add logger.
            raise

    async def get_by_id(self, id: int) -> TModel | None:
        statement = select(self.model).where(self.model.id == id)
        return await self.get_one(statement)

    async def get_all(self, select_statement: Executable) -> List[TModel] | None:
        try:
            entries = await self.session.execute(select_statement)
            return entries.scalars().all()
        except SQLAlchemyError:
            # Add logger.
            raise

    async def delete(self, delete_statement: Executable) -> bool:
        try:
            await self.session.execute(delete_statement)
            await self.session.flush()
            await self.session.commit()
            return True
        except SQLAlchemyError:
            await self.session.rollback()
            # Add logger.
            return False

    async def delete_by_id(self, id: int) -> bool:
        statement = delete(self.model).where(self.model.id == id)
        return await self.delete(statement)

    async def exists(self, select_statement: Executable) -> bool:
        try:
            result = await self.session.execute(select_statement)
            return result.scalar() is not None
        except SQLAlchemyError:
            # Add logger.
            return False

    async def exists_by_id(self, id: int) -> bool:
        statement = select(self.model).where(self.model.id == id)
        return await self.exists(statement)

    async def update(self, updated_model: TModel) -> TSchema | None:
        try:
            model_to_update = self.get_by_id(updated_model.id)

            for col, value in updated_model.to_dict().items():
                if col != 'id':
                    setattr(model_to_update, col, value)

            await self.session.commit()
            await self.session.refresh(model_to_update)
            return self.schema(**model_to_update.to_dict())
        except SQLAlchemyError:
            await self.session.rollback()
            # Add logger.
            raise
