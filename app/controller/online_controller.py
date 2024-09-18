from fastapi import APIRouter
from fastapi import Depends
from config.database import get_db
from app.service.login_service import get_current_user, Session
from app.service.online_service import *
from utils.response_util import *
from utils.log_util import *
from utils.page_util import get_page_obj
from app.aspect.interface_auth import CheckUserInterfaceAuth
from app.annotation.log_annotation import log_decorator


onlineController = APIRouter(prefix='/online', dependencies=[Depends(get_current_user)])


@onlineController.post("/get", dependencies=[Depends(CheckUserInterfaceAuth('monitor:online:list'))])
async def get_monitor_online_list(request: Request, online_page_query: OnlinePageObject):
    try:
        # 获取全量数据
        online_query_result = await OnlineService.get_online_list_services(request, online_page_query)
        # 分页操作
        online_page_query_result = get_page_obj(online_query_result, online_page_query.page, online_page_query.page_size)
        
        return MyResponse(data=online_page_query_result)
    except Exception as e:
        logger.exception(e)
        return MyResponse(data="", msg=str(e))


@onlineController.post("/forceLogout", dependencies=[Depends(CheckUserInterfaceAuth('monitor:online:forceLogout'))])
@log_decorator(title='在线用户', business_type=7)
async def delete_monitor_online(request: Request, delete_online: DeleteOnlineModel, query_db: Session = Depends(get_db)):
    try:
        delete_online_result = await OnlineService.delete_online_services(request, delete_online)
        if delete_online_result.is_success:
            logger.log_info(delete_online_result.message)
            return MyResponse(data=delete_online_result, msg=delete_online_result.message)
        else:
            logger.log_warning(delete_online_result.message)
            return MyResponse(data="", msg=delete_online_result.message)
    except Exception as e:
        logger.exception(e)
        return MyResponse(data="", msg=str(e))


@onlineController.post("/batchLogout", dependencies=[Depends(CheckUserInterfaceAuth('monitor:online:batchLogout'))])
@log_decorator(title='在线用户', business_type=7)
async def delete_monitor_online(request: Request, delete_online: DeleteOnlineModel, query_db: Session = Depends(get_db)):
    try:
        delete_online_result = await OnlineService.delete_online_services(request, delete_online)
        if delete_online_result.is_success:
            logger.log_info(delete_online_result.message)
            return MyResponse(data=delete_online_result, msg=delete_online_result.message)
        else:
            logger.log_warning(delete_online_result.message)
            return MyResponse(data="", msg=delete_online_result.message)
    except Exception as e:
        logger.exception(e)
        return MyResponse(data="", msg=str(e))
