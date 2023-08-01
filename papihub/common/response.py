from fastapi import status
from fastapi.responses import JSONResponse, Response
from typing import Union


def json_200(data: Union[bool, list, dict, str, None] = None, message: Union[str, None] = None) -> Response:
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
