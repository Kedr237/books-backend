from datetime import datetime
from typing import Any, Dict

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()


class BaseModelSchema(BaseSchema):

    id: int
    is_available: bool
    created_at: datetime
    updated_at: datetime


class BaseCreationSchema(BaseSchema):
    ...


class BaseUpdateSchema(BaseSchema):

    id: int
    is_available: bool | None = None


class BaseResponseSchema(BaseSchema):

    success: bool = True
    message: str = 'Successful request.'
