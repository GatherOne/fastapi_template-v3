from fastapi import status
from fastapi.responses import JSONResponse, Response, StreamingResponse
from fastapi.encoders import jsonable_encoder
from typing import Any
from datetime import datetime
from utils.constant import RET, error_map


def MyResponse(*, data: Any = None, msg: str = error_map[RET.OK]) -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(
            {
                'code': RET.OK,
                'msg': msg,
                'data': data,
                'success': 'true',
                'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        )
    )


def streaming_MyResponse(*, data: Any = None):
    return StreamingResponse(
        status_code=status.HTTP_200_OK,
        content=data,
    )


class AuthException(Exception):
    """
    自定义令牌异常AuthException
    """

    def __init__(self, data: str = None, message: str = None):
        self.data = data
        self.message = message


class PermissionException(Exception):
    """
    自定义权限异常PermissionException
    """

    def __init__(self, data: str = None, message: str = None):
        self.data = data
        self.message = message


class LoginException(Exception):
    """
    自定义登录异常LoginException
    """

    def __init__(self, data: str = None, message: str = None):
        self.data = data
        self.message = message
