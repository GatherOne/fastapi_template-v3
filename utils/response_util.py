from fastapi import status
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from typing import Any
from utils.constant import RET, error_map


def MyResponse(*, code: str = RET.OK, msg: str = error_map[RET.OK], total: int = None, data: Any = None, ) -> Response:
    result = {
        'code': code,
        'msg': msg
    }
    if total is not None:
        result['total'] = total
    if data is not None:
        result['data'] = data
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(result)
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
