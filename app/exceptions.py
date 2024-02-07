from fastapi import status
from fastapi import HTTPException


class InvalidIdTokenError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials. {detail}",
            headers={"WWW-Authenticate": 'Bearer error="invalid_token"'},
        )


class BearerAuthenticationRequiredError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer authentication required",
            headers={"WWW-Authenticate": 'Bearer realm="auth_required"'},
        )


class ExpiredIdTokenError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials. {detail}",
            headers={"WWW-Authenticate": 'Bearer error="invalid_token"'},
        )


class UserMonthlyExpensesNotFoundError(HTTPException):
    def __init__(self, month: int, year: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User Monthly Expenses not found. month={month}, year={year}",  # noqa: E501
        )


class DatabaseIntegrityError(HTTPException):
    def __init__(self, detail: str, status_code: int):
        super().__init__(
            status_code=status_code,
            detail=detail,
        )
