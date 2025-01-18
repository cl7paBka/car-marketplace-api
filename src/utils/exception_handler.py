from fastapi import HTTPException
from typing import Any
from pydantic import BaseModel


def handle_exception(status_code: int, custom_message: str):
    """
    Handles exceptions and raises an HTTPException with a status code.
    """
    raise HTTPException( # TODO: maybe add status? For example "error" in some cases may be useful or other
        status_code=status_code,
        detail=custom_message
    )


def handle_exception_default_500(error: Exception):
    """
    Handles unexpected errors and raises an HTTPException with a 500 status code.
    """
    raise HTTPException(
        status_code=500,
        detail=f"An unexpected error occurred: {str(error)}"
    )


def validate_payload(payload: Any) -> None:
    """
    Validates that the provided payload is not empty.
    If the payload is a Pydantic model, it will automatically convert it to a dictionary
    using `model_dump(exclude_unset=True)`. Raises an HTTPException if the resulting dictionary is empty.
    """
    # If the payload is a Pydantic model, converts it to a dictionary
    if isinstance(payload, BaseModel):
        payload = payload.model_dump(exclude_unset=True)

    # Validate that the payload is not empty
    if not payload:  # Check for an empty dictionary like '{}' or None
        raise HTTPException(status_code=400, detail="Payload cannot be empty.")
