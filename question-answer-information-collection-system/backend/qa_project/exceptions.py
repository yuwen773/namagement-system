"""
Custom exception handler for API response format consistency.
"""

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler to ensure consistent API response format.
    Format: { "code": -1, "message": "错误描述", "data": null }
    """
    response = exception_handler(exc, context)

    if response is not None:
        # Get error message
        if hasattr(response, "data"):
            if isinstance(response.data, dict):
                message = response.data.get("detail", str(response.data))
            else:
                message = str(response.data)
        else:
            message = str(exc)

        response.data = {
            "code": response.status_code,
            "message": message,
            "data": None,
        }

    return response
