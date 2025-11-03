from typing import Literal

from pydantic import BaseModel, Field

Status = Literal["UP", "DOWN"]


class HealthResponseModel(BaseModel):
    """
    Represents the health of the system
    """

    status: Status = Field(description="Represents the health status")
