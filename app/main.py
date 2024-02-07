from dotenv import load_dotenv
from firebase_admin import credentials
from firebase_admin import initialize_app
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app import exceptions
from app.constants import API_V1_PREFIX
from app.settings import get_firebase_settings
from app.routers.v1 import health_check_router
from app.routers.v1 import transaction_router
from app.routers.v1 import user_monthly_expenses_router
from app.database import create_database_connection


def create_app():
    load_dotenv()

    app = FastAPI()

    firebase_settings = get_firebase_settings()
    firebase = credentials.Certificate(firebase_settings.model_dump())
    app.state.firebase_app = initialize_app(firebase)

    app.include_router(
        health_check_router.router,
        prefix=API_V1_PREFIX,
        tags=["v1"],
    )
    app.include_router(
        transaction_router.router,
        prefix=API_V1_PREFIX,
        tags=["v1"],
    )
    app.include_router(
        user_monthly_expenses_router.router,
        prefix=API_V1_PREFIX,
        tags=["v1"],
    )

    @app.on_event("startup")
    async def startup_event():
        app.state.db = create_database_connection()

    # Register exception handlers
    @app.exception_handler(exceptions.BearerAuthenticationRequiredError)
    async def bearer_authentication_required_error_handler(request, exc):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=exc.headers,
        )

    @app.exception_handler(exceptions.InvalidIdTokenError)
    async def invalid_id_token_error_handler(request, exc):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=exc.headers,
        )

    @app.exception_handler(exceptions.ExpiredIdTokenError)
    async def expired_id_token_error_handler(request, exc):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=exc.headers,
        )

    @app.exception_handler(exceptions.UserMonthlyExpensesNotFoundError)
    async def user_monthly_expenses_not_found_error_handler(request, exc):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @app.exception_handler(exceptions.DatabaseIntegrityError)
    async def user_monthly_expenses_already_exists_error_handler(request, exc):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    return app
