from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel


ErrorCode = Literal[
    "validation_error",
    "not_found",
    "internal_error",
]


class ErrorDetail(BaseModel):
    loc: list[str] | list[int] | list[Any]
    msg: str
    type: str


class ErrorBody(BaseModel):
    code: ErrorCode
    message: str
    details: list[Any] | None = None


class ErrorResponse(BaseModel):
    error: ErrorBody
    request_id: str


