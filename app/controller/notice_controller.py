from fastapi import APIRouter, Request
from fastapi import Depends
from config.database import get_db
from app.service.login_service import get_current_user, CurrentUserInfoServiceResponse
from app.service.notice_service import *
from app.entity.vo.notice_vo import *
from utils.response_util import *
from utils.log_util import *
from utils.page_util import get_page_obj
from app.aspect.interface_auth import CheckUserInterfaceAuth
from app.annotation.log_annotation import log_decorator


noticeController = APIRouter(dependencies=[Depends(get_current_user)])


@noticeController.post("/notice/get", dependencies=[Depends(CheckUserInterfaceAuth('system:notice:list'))])
async def get_system_notice_list(request: Request, notice_page_query: NoticePageObject, query_db: Session = Depends(get_db)):
    try:
        notice_query = NoticeQueryModel(**notice_page_query.dict())
        # 获取全量数据
        notice_query_result = NoticeService.get_notice_list_services(query_db, notice_query)
        # 分页操作
        notice_page_query_result = get_page_obj(notice_query_result, notice_page_query.page, notice_page_query.page_size)
        
        return MyResponse(data=notice_page_query_result)
    except Exception as e:
        logger.exception(e)
        return MyResponse(data="", msg=str(e))


@noticeController.post("/notice/add", dependencies=[Depends(CheckUserInterfaceAuth('system:notice:add'))])
@log_decorator(title='通知公告管理', business_type=1)
async def add_system_notice(request: Request, add_notice: NoticeModel, query_db: Session = Depends(get_db), current_user: CurrentUserInfoServiceResponse = Depends(get_current_user)):
    try:
        add_notice.create_by = current_user.user.user_name
        add_notice.create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        add_notice.update_by = current_user.user.user_name
        add_notice.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        add_notice_result = NoticeService.add_notice_services(query_db, add_notice)
        if add_notice_result.is_success:
            logger.log_info(add_notice_result.message)
            return MyResponse(data=add_notice_result, msg=add_notice_result.message)
        else:
            logger.log_warning(add_notice_result.message)
            return MyResponse(data="", msg=add_notice_result.message)
    except Exception as e:
        logger.exception(e)
        return MyResponse(data="", msg=str(e))


@noticeController.patch("/notice/edit", dependencies=[Depends(CheckUserInterfaceAuth('system:notice:edit'))])
@log_decorator(title='通知公告管理', business_type=2)
async def edit_system_notice(request: Request, edit_notice: NoticeModel, query_db: Session = Depends(get_db), current_user: CurrentUserInfoServiceResponse = Depends(get_current_user)):
    try:
        edit_notice.update_by = current_user.user.user_name
        edit_notice.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        edit_notice_result = NoticeService.edit_notice_services(query_db, edit_notice)
        if edit_notice_result.is_success:
            logger.log_info(edit_notice_result.message)
            return MyResponse(data=edit_notice_result, msg=edit_notice_result.message)
        else:
            logger.log_warning(edit_notice_result.message)
            return MyResponse(data="", msg=edit_notice_result.message)
    except Exception as e:
        logger.exception(e)
        return MyResponse(data="", msg=str(e))


@noticeController.post("/notice/delete", dependencies=[Depends(CheckUserInterfaceAuth('system:notice:remove'))])
@log_decorator(title='通知公告管理', business_type=3)
async def delete_system_notice(request: Request, delete_notice: DeleteNoticeModel, query_db: Session = Depends(get_db)):
    try:
        delete_notice_result = NoticeService.delete_notice_services(query_db, delete_notice)
        if delete_notice_result.is_success:
            logger.log_info(delete_notice_result.message)
            return MyResponse(data=delete_notice_result, msg=delete_notice_result.message)
        else:
            logger.log_warning(delete_notice_result.message)
            return MyResponse(data="", msg=delete_notice_result.message)
    except Exception as e:
        logger.exception(e)
        return MyResponse(data="", msg=str(e))


@noticeController.get("/notice/{notice_id}", dependencies=[Depends(CheckUserInterfaceAuth('system:notice:query'))])
async def query_detail_system_post(request: Request, notice_id: int, query_db: Session = Depends(get_db)):
    try:
        detail_notice_result = NoticeService.detail_notice_services(query_db, notice_id)
        logger.log_info(f'获取notice_id为{notice_id}的信息成功')
        return MyResponse(data=detail_notice_result, msg='获取成功')
    except Exception as e:
        logger.exception(e)
        return MyResponse(data="", msg=str(e))
