from fastapi import APIRouter, Request
from fastapi import Depends
from app.service.login_service import get_current_user
from app.service.server_service import *
from utils.response_util import *
from utils.log_util import *
from app.aspect.interface_auth import CheckUserInterfaceAuth


serverController = APIRouter(prefix='/server', dependencies=[Depends(get_current_user)])


@serverController.post("/statisticalInfo", response_model=ServerMonitorModel, dependencies=[Depends(CheckUserInterfaceAuth('monitor:server:list'))])
async def get_monitor_server_info(request: Request):
    try:
        # 获取全量数据
        server_info_query_result = ServerService.get_server_monitor_info()
        logger.log_info('获取成功')
        return MyResponse(data=server_info_query_result, msg="获取成功")
    except Exception as e:
        logger.exception(e)
        return MyResponse(data="", msg=str(e))
