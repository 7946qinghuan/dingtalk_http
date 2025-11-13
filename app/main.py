from fastapi import FastAPI

from app.core import lifespan
from app.middleware.cors_middleware import add_cors_middleware
from app.routers import health_router, callback_router

# 创建FastAPI应用
app = FastAPI(lifespan=lifespan, title="DingTalk HTTP模式 回调接口")

# 注册路由
app.include_router(health_router)
app.include_router(callback_router)

# 添加跨域中间件
add_cors_middleware(app)
