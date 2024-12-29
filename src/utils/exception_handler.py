from fastapi import HTTPException


def handle_exception(status_code: int, custom_message: str):
    """
    Handles exceptions and raises an HTTPException with a status code.
    """
    raise HTTPException(
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
