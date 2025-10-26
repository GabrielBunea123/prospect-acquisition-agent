from typing import List

from pydantic import BaseModel, Field


class ApiResponseItemModel(BaseModel):
    """
    Represents a single validation or error detail item.

    Used to provide specific information about individual field errors
    or validation issues in API responses.
    """

    field: str = Field(
        description="The field path where the error occurred (e.g., 'body.content')"
    )
    value: str = Field(
        description="The value that caused the error or validation issue"
    )
    info: str = Field(
        description="Human-readable error message or additional information"
    )


class ApiResponseModel(BaseModel):
    """
    Standard API error response model.

    This model is used for structured error responses, particularly for
    validation errors and other client errors (4xx status codes).
    """

    message: str = Field(description="High-level error message")
    details: List[ApiResponseItemModel] = Field(
        description="List of specific error details"
    )
