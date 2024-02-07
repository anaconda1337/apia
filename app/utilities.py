from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.query import Query
from app.models.alembic_base import Base

from app.exceptions import DatabaseIntegrityError


async def db_insert(
    db: Session,
    item: BaseModel,
):
    try:
        db.add(item)
        db.commit()
        db.refresh(item)
    except IntegrityError:
        raise DatabaseIntegrityError(
            status_code=409,
            detail="The item already exists in the database.",
        )


async def db_query(
    db: Session,
    conditions: dict,
    model: Base
):
    query: Query = db.query(model).filter_by(**conditions)
    return query.scalar()
