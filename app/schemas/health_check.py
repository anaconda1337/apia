from pydantic import BaseModel, Field

from app.constants import HealthStatus


class HealthCheckSchema(BaseModel):
    status: str = Field(default=HealthStatus.OK)
    name: str = Field()
    version: str = Field()
    timestamp: str = Field()
