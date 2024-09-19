from fastapi import APIRouter, Request
from fastapi import Depends
from starlette.responses import StreamingResponse

from config.get_db import get_db
from app.service.login_service import get_current_user, CurrentUserInfoServiceResponse
from app.service.post_service import *
from app.entity.vo.post_vo import *
from utils.response_util import *
from utils.log_util import *
from utils.page_util import get_page_obj
from utils.common_util import bytes2file_response
from app.aspect.interface_auth import CheckUserInterfaceAuth
from app.annotation.log_annotation import log_decorator


postController = APIRouter(dependencies=[Depends(get_current_user)])


@postController.post("/post/forSelectOption", dependencies=[Depends(CheckUserInterfaceAuth('common'))])
async def get_system_post_select(request: Request, query_db: Session = Depends(get_db)):
    try:
        role_query_result = PostService.get_post_select_option_services(query_db)
        
        return MyResponse(data=role_query_result)
    except Exception as e:
        logger.exception(e)
        return MyResponse(data="", msg=str(e))


@postController.post("/post/get", dependencies=[Depends(CheckUserInterfaceAuth('system:post:list'))])
async def get_system_post_list(request: Request, post_page_query: PostPageObject, query_db: Session = Depends(get_db)):
    try:
        post_query = PostModel(**post_page_query.dict())
        # 获取全量数据
        post_query_result = PostService.get_post_list_services(query_db, post_query)
        # 分页操作
        post_page_query_result = get_page_obj(post_query_result, post_page_query.page, post_page_query.page_size)
        
        return MyResponse(data=post_page_query_result)
    except Exception as e:
        logger.exception(e)
        return MyResponse(data="", msg=str(e))


@postController.post("/post/add", dependencies=[Depends(CheckUserInterfaceAuth('system:post:add'))])
@log_decorator(title='岗位管理', business_type=1)
async def add_system_post(request: Request, add_post: PostModel, query_db: Session = Depends(get_db), current_user: CurrentUserInfoServiceResponse = Depends(get_current_user)):
    try:
        add_post.create_by = current_user.user.user_name
        add_post.create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        add_post.update_by = current_user.user.user_name
        add_post.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        add_post_result = PostService.add_post_services(query_db, add_post)
        if add_post_result.is_success:
            logger.log_info(add_post_result.message)
            return MyResponse(data=add_post_result, msg=add_post_result.message)
        else:
            logger.log_warning(add_post_result.message)
            return MyResponse(data="", msg=add_post_result.message)
    except Exception as e:
        logger.exception(e)
        return MyResponse(data="", msg=str(e))


@postController.patch("/post/edit", dependencies=[Depends(CheckUserInterfaceAuth('system:post:edit'))])
@log_decorator(title='岗位管理', business_type=2)
async def edit_system_post(request: Request, edit_post: PostModel, query_db: Session = Depends(get_db), current_user: CurrentUserInfoServiceResponse = Depends(get_current_user)):
    try:
        edit_post.update_by = current_user.user.user_name
        edit_post.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        edit_post_result = PostService.edit_post_services(query_db, edit_post)
        if edit_post_result.is_success:
            logger.log_info(edit_post_result.message)
            return MyResponse(data=edit_post_result, msg=edit_post_result.message)
        else:
            logger.log_warning(edit_post_result.message)
            return MyResponse(data="", msg=edit_post_result.message)
    except Exception as e:
        logger.exception(e)
        return MyResponse(data="", msg=str(e))


@postController.post("/post/delete", dependencies=[Depends(CheckUserInterfaceAuth('system:post:remove'))])
@log_decorator(title='岗位管理', business_type=3)
async def delete_system_post(request: Request, delete_post: DeletePostModel, query_db: Session = Depends(get_db)):
    try:
        delete_post_result = PostService.delete_post_services(query_db, delete_post)
        if delete_post_result.is_success:
            logger.log_info(delete_post_result.message)
            return MyResponse(data=delete_post_result, msg=delete_post_result.message)
        else:
            logger.log_warning(delete_post_result.message)
            return MyResponse(data="", msg=delete_post_result.message)
    except Exception as e:
        logger.exception(e)
        return MyResponse(data="", msg=str(e))


@postController.get("/post/{post_id}", dependencies=[Depends(CheckUserInterfaceAuth('system:post:query'))])
async def query_detail_system_post(request: Request, post_id: int, query_db: Session = Depends(get_db)):
    try:
        detail_post_result = PostService.detail_post_services(query_db, post_id)
        logger.log_info(f'获取post_id为{post_id}的信息成功')
        return MyResponse(data=detail_post_result, msg='获取成功')
    except Exception as e:
        logger.exception(e)
        return MyResponse(data="", msg=str(e))


@postController.post("/post/export", dependencies=[Depends(CheckUserInterfaceAuth('system:post:export'))])
@log_decorator(title='岗位管理', business_type=5)
async def export_system_post_list(request: Request, post_query: PostModel, query_db: Session = Depends(get_db)):
    try:
        # 获取全量数据
        post_query_result = PostService.get_post_list_services(query_db, post_query)
        post_export_result = PostService.export_post_list_services(post_query_result)
        logger.log_info('导出成功')
        return StreamingResponse(content=bytes2file_response(post_export_result))
    except Exception as e:
        logger.exception(e)
        return MyResponse(data="", msg=str(e))
