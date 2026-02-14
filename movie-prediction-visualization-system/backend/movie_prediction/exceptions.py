from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    自定义异常处理器，统一错误响应格式
    """
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {
            'code': -1,
            'message': str(exc),
            'data': None
        }

    return response
