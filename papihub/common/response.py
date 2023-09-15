import json

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from typing import Union

from starlette.responses import PlainTextResponse

from papihub.common.customjsonencoder import CustomJSONEncoder


def json_200(data: Union[bool, list, dict, str, None] = None, message: Union[str, None] = None) -> Response:
    """
    返回http_status=200的结果
    :param data: 返回结果
    :param message: 消息
    :return:
    """
    if not message:
        message = "success"
    if data:
        if isinstance(data, list):
            if len(data) > 0 and 'to_dict' in dir(data[0]):
                data = [i.to_dict() for i in data]
        elif 'to_dict' in dir(data):
            data = data.to_dict()
    return PlainTextResponse(
        media_type="application/json",
        status_code=status.HTTP_200_OK,
        content=json.dumps({
            'success': True,
            'errorCode': 0,
            'message': message,
            'data': data,
        }, cls=CustomJSONEncoder),
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


def json_with_status(status_code: int, data: Union[bool, list, dict, str, None] = None,
                     message: Union[str, None] = None) -> Response:
    """
    返回自定义statuscode的结果
    :param data: 返回结果
    :param message: 消息
    :return:
    """
    if not message:
        message = "success"
    return JSONResponse(
        status_code=status_code,
        content={
            'success': False,
            'errorCode': 1,
            'message': message,
            'data': data,
        }
    )
