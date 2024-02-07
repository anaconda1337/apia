from uuid import UUID

from fastapi import status
from fastapi import Depends
from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.injections import firebase_authentication
from app.schemas.user_monthly_expenses import UserMonthlyExpensesSchema
from app.constants import API_V1_USER_MONTHLY_EXPENSES
from app.database import get_db_session
from app.models.user_monthly_expenses_model import UserMonthlyExpensesModel
from app.utilities import db_insert
from app.utilities import db_query


router = APIRouter()


@router.post(
    path=API_V1_USER_MONTHLY_EXPENSES,
    summary="Insert a UserMonthlyExpenses",
    response_description="Return HTTP Status Code 201 (Created)",
    status_code=status.HTTP_201_CREATED,
    response_model=UserMonthlyExpensesSchema,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Created",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Bearer authentication required",
        },
        status.HTTP_409_CONFLICT: {
            "description": "The item already exists in the database.",
        },
    },
)
async def insert_user_monthly_expenses(
    user_monthly_expense: UserMonthlyExpensesSchema,
    user_id: UUID = Depends(firebase_authentication),
    db_session: Session = Depends(get_db_session),
):
    item = UserMonthlyExpensesModel(**user_monthly_expense.model_dump(), user_id=user_id)  # noqa: E501
    await db_insert(db=db_session, item=item)
    return item


@router.get(
    path=f"{API_V1_USER_MONTHLY_EXPENSES}/{{month}}/{{year}}",
    summary="Get UserMonthlyExpenses",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=UserMonthlyExpensesSchema,
    responses={
        status.HTTP_200_OK: {
            "description": "OK",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Bearer authentication required",
        },
    },
)
async def get_user_monthly_expenses(
    month: int,
    year: int,
    user_id: UUID = Depends(firebase_authentication),
    db_session: Session = Depends(get_db_session),
):
    conditions = {
        "month": month,
        "year": year,
        "user_id": user_id,
    }
    item = await db_query(db=db_session, conditions=conditions, model=UserMonthlyExpensesModel)  # noqa: E501
    return item
