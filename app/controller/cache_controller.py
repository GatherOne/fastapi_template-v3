from fastapi import APIRouter
from fastapi import Depends
from app.service.login_service import get_current_user
from app.service.cache_service import *
from utils.response_util import *
from utils.log_util import *
from app.aspect.interface_auth import CheckUserInterfaceAuth


cacheController = APIRouter(prefix='/cache', dependencies=[Depends(get_current_user)])


@cacheController.post("/statisticalInfo", dependencies=[Depends(CheckUserInterfaceAuth('monitor:cache:list'))])
async def get_monitor_cache_info(request: Request):
    try:
        # 获取全量数据
        cache_info_query_result = await CacheService.get_cache_monitor_statistical_info_services(request)
        return MyResponse(data=cache_info_query_result)
    except Exception as e:
        logger.exception(e)
        return MyResponse(data="", msg=str(e))


@cacheController.post("/getNames", dependencies=[Depends(CheckUserInterfaceAuth('monitor:cache:list'))])
async def get_monitor_cache_name(request: Request):
    try:
        # 获取全量数据
        cache_name_list_result = CacheService.get_cache_monitor_cache_name_services()
        
        return MyResponse(data=cache_name_list_result)
    except Exception as e:
        logger.exception(e)
        return MyResponse(data="", msg=str(e))


@cacheController.post("/getKeys/{cache_name}", dependencies=[Depends(CheckUserInterfaceAuth('monitor:cache:list'))])
async def get_monitor_cache_key(request: Request, cache_name: str):
    try:
        # 获取全量数据
        cache_key_list_result = await CacheService.get_cache_monitor_cache_key_services(request, cache_name)
        
        return MyResponse(data=cache_key_list_result)
    except Exception as e:
        logger.exception(e)
        return MyResponse(data="", msg=str(e))


@cacheController.post("/getValue/{cache_name}/{cache_key}", dependencies=[Depends(CheckUserInterfaceAuth('monitor:cache:list'))])
async def get_monitor_cache_value(request: Request, cache_name: str, cache_key: str):
    try:
        # 获取全量数据
        cache_value_list_result = await CacheService.get_cache_monitor_cache_value_services(request, cache_name, cache_key)
        
        return MyResponse(data=cache_value_list_result)
    except Exception as e:
        logger.exception(e)
        return MyResponse(data="", msg=str(e))


@cacheController.post("/clearCacheName/{cache_name}", dependencies=[Depends(CheckUserInterfaceAuth('monitor:cache:list'))])
async def clear_monitor_cache_name(request: Request, cache_name: str):
    try:
        clear_cache_name_result = await CacheService.clear_cache_monitor_cache_name_services(request, cache_name)
        if clear_cache_name_result.is_success:
            logger.log_info(clear_cache_name_result.message)
            return MyResponse(data=clear_cache_name_result, msg=clear_cache_name_result.message)
    except Exception as e:
        logger.exception(e)
        return MyResponse(data="", msg=str(e))


@cacheController.post("/clearCacheKey/{cache_name}/{cache_key}", dependencies=[Depends(CheckUserInterfaceAuth('monitor:cache:list'))])
async def clear_monitor_cache_key(request: Request, cache_name: str, cache_key: str):
    try:
        clear_cache_key_result = await CacheService.clear_cache_monitor_cache_key_services(request, cache_name, cache_key)
        if clear_cache_key_result.is_success:
            logger.log_info(clear_cache_key_result.message)
            return MyResponse(data=clear_cache_key_result, msg=clear_cache_key_result.message)
    except Exception as e:
        logger.exception(e)
        return MyResponse(data="", msg=str(e))


@cacheController.post("/clearCacheAll", dependencies=[Depends(CheckUserInterfaceAuth('monitor:cache:list'))])
async def clear_monitor_cache_all(request: Request):
    try:
        clear_cache_all_result = await CacheService.clear_cache_monitor_all_services(request)
        if clear_cache_all_result.is_success:
            logger.log_info(clear_cache_all_result.message)
            return MyResponse(data=clear_cache_all_result, msg=clear_cache_all_result.message)
    except Exception as e:
        logger.exception(e)
        return MyResponse(data="", msg=str(e))
