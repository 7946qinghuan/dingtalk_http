# main.py
from fastapi import FastAPI
from routers import health_router, callback_router
from middleware import add_cors_middleware


app = FastAPI(title="DingTalk HTTP模式 回调接口")

# 注册路由
app.include_router(health_router)
app.include_router(callback_router)

# 添加跨域中间件
add_cors_middleware(app)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=18082, reload=True)  # nosec B104
