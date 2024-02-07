from enum import StrEnum


class HealthStatus(StrEnum):
    OK = "OK"


API_V1_PREFIX = "/api/v1"
API_V1_HEALTH_CHECK = "/health_check"
API_V1_TRANSACTION = "/transaction"
API_V1_USER_MONTHLY_EXPENSES = "/user_monthly_expenses"
