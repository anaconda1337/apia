from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime
from sqlalchemy import PrimaryKeyConstraint

from app.models.alembic_base import Base


class UserMonthlyExpensesModel(Base):
    __tablename__ = "user_monthly_expenses"

    user_id = Column(String(255), nullable=False)
    transaction_count = Column(Integer)
    total_expenses = Column(Float)
    timestamp = Column(DateTime, server_default=func.now())
    month = Column(Integer, server_default=func.extract('month', func.now()))
    year = Column(Integer, server_default=func.extract('year', func.now()))

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'month', 'year'),
    )
