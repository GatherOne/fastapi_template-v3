from fastapi import APIRouter, Request
from fastapi import Depends
from config.database import get_db
from app.service.login_service import get_current_user, CurrentUserInfoServiceResponse
from app.service.dept_service import *
from app.entity.vo.dept_vo import *
from app.dao.dept_dao import *
from utils.response_util import *
from utils.log_util import *
from app.aspect.interface_auth import CheckUserInterfaceAuth
from app.aspect.data_scope import GetDataScope
from app.annotation.log_annotation import log_decorator


deptController = APIRouter(dependencies=[Depends(get_current_user)])


@deptController.post("/dept/tree", dependencies=[Depends(CheckUserInterfaceAuth('common'))])
async def get_system_dept_tree(request: Request, dept_query: DeptModel, query_db: Session = Depends(get_db), data_scope_sql: str = Depends(GetDataScope('SysDept'))):
    try:
        dept_query_result = DeptService.get_dept_tree_services(query_db, dept_query, data_scope_sql)
        
        return MyResponse(data=dept_query_result)
    except Exception as e:
        logger.exception(e)
        return MyResponse(data="", msg=str(e))


@deptController.post("/dept/forEditOption", dependencies=[Depends(CheckUserInterfaceAuth('common'))])
async def get_system_dept_tree_for_edit_option(request: Request, dept_query: DeptModel, query_db: Session = Depends(get_db), data_scope_sql: str = Depends(GetDataScope('SysDept'))):
    try:
        dept_query_result = DeptService.get_dept_tree_for_edit_option_services(query_db, dept_query, data_scope_sql)
        
        return MyResponse(data=dept_query_result)
    except Exception as e:
        logger.exception(e)
        return MyResponse(data="", msg=str(e))


@deptController.post("/dept/get", dependencies=[Depends(CheckUserInterfaceAuth('system:dept:list'))])
async def get_system_dept_list(request: Request, dept_query: DeptModel, query_db: Session = Depends(get_db), data_scope_sql: str = Depends(GetDataScope('SysDept'))):
    try:
        dept_query_result = DeptService.get_dept_list_services(query_db, dept_query, data_scope_sql)
        
        return MyResponse(data=dept_query_result)
    except Exception as e:
        logger.exception(e)
        return MyResponse(data="", msg=str(e))


@deptController.post("/dept/add", dependencies=[Depends(CheckUserInterfaceAuth('system:dept:add'))])
@log_decorator(title='部门管理', business_type=1)
async def add_system_dept(request: Request, add_dept: DeptModel, query_db: Session = Depends(get_db), current_user: CurrentUserInfoServiceResponse = Depends(get_current_user)):
    try:
        add_dept.create_by = current_user.user.user_name
        add_dept.create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        add_dept.update_by = current_user.user.user_name
        add_dept.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        add_dept_result = DeptService.add_dept_services(query_db, add_dept)
        if add_dept_result.is_success:
            logger.log_info(add_dept_result.message)
            return MyResponse(data=add_dept_result, msg=add_dept_result.message)
        else:
            logger.log_warning(add_dept_result.message)
            return MyResponse(data="", msg=add_dept_result.message)
    except Exception as e:
        logger.exception(e)
        return MyResponse(data="", msg=str(e))


@deptController.patch("/dept/edit", dependencies=[Depends(CheckUserInterfaceAuth('system:dept:edit'))])
@log_decorator(title='部门管理', business_type=2)
async def edit_system_dept(request: Request, edit_dept: DeptModel, query_db: Session = Depends(get_db), current_user: CurrentUserInfoServiceResponse = Depends(get_current_user)):
    try:
        edit_dept.update_by = current_user.user.user_name
        edit_dept.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        edit_dept_result = DeptService.edit_dept_services(query_db, edit_dept)
        if edit_dept_result.is_success:
            logger.log_info(edit_dept_result.message)
            return MyResponse(data=edit_dept_result, msg=edit_dept_result.message)
        else:
            logger.log_warning(edit_dept_result.message)
            return MyResponse(data="", msg=edit_dept_result.message)
    except Exception as e:
        logger.exception(e)
        return MyResponse(data="", msg=str(e))


@deptController.post("/dept/delete", dependencies=[Depends(CheckUserInterfaceAuth('system:dept:remove'))])
@log_decorator(title='部门管理', business_type=3)
async def delete_system_dept(request: Request, delete_dept: DeleteDeptModel, query_db: Session = Depends(get_db), current_user: CurrentUserInfoServiceResponse = Depends(get_current_user)):
    try:
        delete_dept.update_by = current_user.user.user_name
        delete_dept.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        delete_dept_result = DeptService.delete_dept_services(query_db, delete_dept)
        if delete_dept_result.is_success:
            logger.log_info(delete_dept_result.message)
            return MyResponse(data=delete_dept_result, msg=delete_dept_result.message)
        else:
            logger.log_warning(delete_dept_result.message)
            return MyResponse(data="", msg=delete_dept_result.message)
    except Exception as e:
        logger.exception(e)
        return MyResponse(data="", msg=str(e))


@deptController.get("/dept/{dept_id}", dependencies=[Depends(CheckUserInterfaceAuth('system:dept:query'))])
async def query_detail_system_dept(request: Request, dept_id: int, query_db: Session = Depends(get_db)):
    try:
        detail_dept_result = DeptService.detail_dept_services(query_db, dept_id)
        logger.log_info(f'获取dept_id为{dept_id}的信息成功')
        return MyResponse(data=detail_dept_result, msg='获取成功')
    except Exception as e:
        logger.exception(e)
        return MyResponse(data="", msg=str(e))
