from typing import List, Type

from fastapi import HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import Executable

from models import BaseModel
from schemas import BaseResponseSchema, BaseSchema


class SessionMixin:

    def __init__(self, session: AsyncSession):
        self.session = session


class BaseManager[TModel: BaseModel](SessionMixin):

    def __init__(self, session: AsyncSession, model: Type[TModel]):
        super().__init__(session)
        self.model = model

    async def add_one(self, model: TModel) -> TModel | None:
        try:
            self.session.add(model)
            await self.session.commit()
            await self.session.refresh(model)
            return model
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

    async def update(self, updated_model: TModel) -> TModel | None:
        try:
            model_to_update = self.get_by_id(updated_model.id)

            for col, value in updated_model.to_dict().items():
                if col != 'id':
                    setattr(model_to_update, col, value)

            await self.session.commit()
            await self.session.refresh(model_to_update)
            return model_to_update.to_dict()
        except SQLAlchemyError:
            await self.session.rollback()
            # Add logger.
            raise


class BaseService[TModel: BaseModel, TSchema: BaseSchema](SessionMixin):

    def __init__(self, session, manager: BaseManager[TModel], schema: Type[TSchema]):
        super().__init__(session)
        self.manager = manager
        self.schema = schema

    async def get_by_id(self, id: int) -> TSchema | None:
        model = await self.manager.get_by_id(id)
        model_name = self.manager.model.__name__

        if model:
            return self.schema(**model.to_dict())
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'The entry [{model_name}] with id [{id}] not found.'
        )

    async def delete_by_id(self, id: int) -> BaseResponseSchema:
        model_name = self.manager.model.__name__
        try:
            exists = await self.manager.exists_by_id(id)
            if not exists:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'The entry [{model_name}] with id [{id}] not found.'
                )
            
            is_deleted = await self.manager.delete_by_id(id)
            if not is_deleted:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'Failed to delete {model_name}',
                )
            
            return BaseResponseSchema(
                message=f'The entry [{model_name}] with id [{id}] was successfully deleted.',
            )
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'An error occurred while deleting the entry [{model_name}] with id [{id}].',
            )
