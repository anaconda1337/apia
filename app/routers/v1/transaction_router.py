from fastapi import status
from fastapi import Depends
from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.injections import firebase_authentication
from app.schemas.transaction import TransactionSchema
from app.constants import API_V1_TRANSACTION
from app.database import get_db_session
from app.models.transaction_model import TransactionModel
from app.utilities import db_insert


router = APIRouter()


@router.post(
    path=API_V1_TRANSACTION,
    summary="Insert a Transaction",
    response_description="Return HTTP Status Code 201 (Created)",
    status_code=status.HTTP_201_CREATED,
    response_model=TransactionSchema,
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
async def insert_transaction(
    transaction: TransactionSchema,
    user_id: str = Depends(firebase_authentication),
    db_session: Session = Depends(get_db_session),
):
    item = TransactionModel(**transaction.model_dump(), user_id=user_id)
    await db_insert(db=db_session, item=item)
    return item
