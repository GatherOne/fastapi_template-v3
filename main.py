from fastapi import FastAPI, Request
import uvicorn
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.controller.login_controller import loginController
from app.controller.captcha_controller import captchaController
from app.controller.user_controller import userController
from app.controller.menu_controller import menuController
from app.controller.dept_controller import deptController
from app.controller.role_controller import roleController
from app.controller.post_controler import postController
from app.controller.dict_controller import dictController
from app.controller.config_controller import configController
from app.controller.notice_controller import noticeController
from app.controller.log_controller import logController
from app.controller.online_controller import onlineController
from app.controller.job_controller import jobController
from app.controller.server_controller import serverController
from app.controller.cache_controller import cacheController
from app.controller.common_controller import commonController
from config.env import AppConfig
from utils.redis_util import RedisUtil
from config.database import init_create_table
from config.scheduler import SchedulerUtil
from utils.response_util import *
from utils.log_util import logger
from utils.common_util import worship

app = FastAPI(
    title=AppConfig.app_name,
    description=f'{AppConfig.app_name}接口文档',
    version=AppConfig.app_version,
    root_path=AppConfig.app_root_path,
)

# 前端页面url
origins = [
    "http://localhost:8088",
    "http://127.0.0.1:8088",
]

# 后台api允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    logger.log_info(f"{AppConfig.app_name}开始启动")
    worship()
    # await init_create_table()
    app.state.redis = await RedisUtil.create_redis_pool()
    # await RedisUtil.init_sys_dict(app.state.redis)
    # await RedisUtil.init_sys_config(app.state.redis)
    # await SchedulerUtil.init_system_scheduler()
    logger.log_info(f"{AppConfig.app_name}启动成功")


@app.on_event("shutdown")
async def shutdown_event():
    await RedisUtil.close_redis_pool(app)
    await SchedulerUtil.close_system_scheduler()


# 自定义token检验异常
@app.exception_handler(AuthException)
async def auth_exception_handler(request: Request, exc: AuthException):
    return MyResponse(data=exc.data, msg=exc.message)


# 自定义权限检验异常
@app.exception_handler(PermissionException)
async def permission_exception_handler(request: Request, exc: PermissionException):
    return MyResponse(data=exc.data, msg=exc.message)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        content=jsonable_encoder({"message": exc.detail, "code": exc.status_code}),
        status_code=exc.status_code
    )


app.include_router(loginController, prefix="/login", tags=['登录模块'])
app.include_router(captchaController, prefix="/captcha", tags=['验证码模块'])
app.include_router(userController, prefix="/system", tags=['系统管理-用户管理'])
app.include_router(menuController, prefix="/system", tags=['系统管理-菜单管理'])
app.include_router(deptController, prefix="/system", tags=['系统管理-部门管理'])
app.include_router(roleController, prefix="/system", tags=['系统管理-角色管理'])
app.include_router(postController, prefix="/system", tags=['系统管理-岗位管理'])
app.include_router(dictController, prefix="/system", tags=['系统管理-字典管理'])
app.include_router(configController, prefix="/system", tags=['系统管理-参数管理'])
app.include_router(noticeController, prefix="/system", tags=['系统管理-通知公告管理'])
app.include_router(logController, prefix="/system", tags=['系统管理-日志管理'])
app.include_router(onlineController, prefix="/monitor", tags=['系统监控-在线用户'])
app.include_router(jobController, prefix="/monitor", tags=['系统监控-定时任务'])
app.include_router(serverController, prefix="/monitor", tags=['系统监控-服务监控'])
app.include_router(cacheController, prefix="/monitor", tags=['系统监控-缓存监控'])
app.include_router(commonController, prefix="/common", tags=['通用模块'])

if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        host=AppConfig.app_host,
        port=AppConfig.app_port,
        reload=AppConfig.app_reload
    )
