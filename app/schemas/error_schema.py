from typing import Any, List, Optional

from pydantic import BaseModel, Field

class ErrorDetail(BaseModel):
    """
    Detail error validasi.
    """

    field: Optional[str] = Field(
        default=None,
        description="Nama field yang menyebabkan error.",
        example="RSI",
    )

    message: str = Field(
        ...,
        description="Pesan error.",
        example="Input should be less than or equal to 100.",
    )

    value: Optional[Any] = Field(
        default=None,
        description="Nilai input yang menyebabkan error.",
        example=150,
    )

class ErrorResponse(BaseModel):
    """
    Format standar response error API.
    """
    status: str = Field(
        default="error",
        description="Status response API.",
        example="error",
    )

    message: str = Field(
        ...,
        description="Ringkasan error.",
        example="Invalid request input.",
    )

    errors: Optional[List[ErrorDetail]] = Field(
        default=None,
        description="Daftar detail error.",
    )