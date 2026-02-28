"""
Custom exception handler for REST framework.
"""

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler that returns consistent error format.
    """
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {
            'code': -1,
            'message': str(exc),
            'data': None
        }
        return response

    # Handle unexpected exceptions
    return Response({
        'code': -1,
        'message': '服务器内部错误',
        'data': None
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
