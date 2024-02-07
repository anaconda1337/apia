import datetime

from fastapi import status
from fastapi import Depends
from fastapi import APIRouter

from app.settings import AppSettings
from app.settings import get_app_settings
from app.constants import HealthStatus
from app.constants import API_V1_HEALTH_CHECK
from app.injections import firebase_authentication
from app.schemas.health_check import HealthCheckSchema


router = APIRouter()


@router.get(
    path=API_V1_HEALTH_CHECK,
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheckSchema,
    dependencies=[Depends(firebase_authentication)],
    responses={
        status.HTTP_200_OK: {
            "description": "OK",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Bearer authentication required",
        },
    },
)
async def health_check(
    app_settings: AppSettings = Depends(get_app_settings),
) -> HealthCheckSchema:
    return HealthCheckSchema(
        status=HealthStatus.OK,
        name=app_settings.NAME,
        version=app_settings.VERSION,
        timestamp=str(datetime.datetime.now(datetime.UTC)),
    )
