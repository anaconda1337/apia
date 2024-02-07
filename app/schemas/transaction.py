from uuid import uuid4, UUID

from pydantic import BaseModel
from pydantic.fields import Field


class TransactionSchema(BaseModel):
    amount: float
    category: int
    description: str

    class Config:
        orm_mode = True
