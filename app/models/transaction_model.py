from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime
from sqlalchemy import event
import sqlalchemy as sa

from app.models.alembic_base import Base
from app.models.user_monthly_expenses_model import UserMonthlyExpensesModel
from app.exceptions import UserMonthlyExpensesNotFoundError


class TransactionModel(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, server_default=func.now())
    user_id = Column(String(255), primary_key=True)
    amount = Column(Float)
    category = Column(Integer)
    description = Column(String(255))
    month = Column(Integer, server_default=func.extract('month', func.now()))
    year = Column(Integer, server_default=func.extract('year', func.now()))
    day = Column(Integer, server_default=func.extract('day', func.now()))


@event.listens_for(TransactionModel, 'after_insert')
def after_insert_listener(mapper, connection, target):
    session = sa.orm.Session(bind=connection)
    user_monthly_expenses = (
        session.query(UserMonthlyExpensesModel)
        .filter(
            UserMonthlyExpensesModel.user_id == target.user_id,
            UserMonthlyExpensesModel.month == target.month,
            UserMonthlyExpensesModel.year == target.year
        )
        .first()
    )

    if user_monthly_expenses:
        user_monthly_expenses.transaction_count += 1
        user_monthly_expenses.total_expenses += target.amount
        session.commit()
    else:
        raise UserMonthlyExpensesNotFoundError(target.month, target.year)
