from datetime import datetime

from pydantic import BaseModel
from pydantic.fields import Field


class UserMonthlyExpensesSchema(BaseModel):
    transaction_count: int = Field(default=0)
    total_expenses: float = Field(default=0.0)
    month: int = Field(default=datetime.now().month)
    year: int = Field(default=datetime.now().year)
