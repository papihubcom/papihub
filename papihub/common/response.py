from fastapi import status
from fastapi.responses import JSONResponse, Response
from typing import Union


def json_200(data: Union[bool, list, dict, str, None] = None, message: Union[str, None] = None) -> Response:
    """
    返回http_status=200的结果
    :param data: 返回结果
    :param message: 消息
    :return:
    """
    if not message:
        message = "success"
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'success': True,
            'errorCode': 0,
            'message': message,
            'data': data,
        }
    )


def json_500(data: Union[bool, list, dict, str, None] = None, message: Union[str, None] = None) -> Response:
    """
    返回http_status=500的结果
    :param data: 返回结果
    :param message: 消息
    :return:
    """
    if not message:
        message = "success"
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            'success': False,
            'errorCode': 1,
            'message': message,
            'data': data,
        }
    )
