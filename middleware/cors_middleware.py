from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI


def add_cors_middleware(app: FastAPI):
    """添加跨域中间件：允许前端（如Vue、React）跨域请求"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "*"
        ],  # 生产环境替换为具体前端域名（如["http://localhost:3000"]）
        allow_credentials=True,
        allow_methods=["*"],  # 允许所有HTTP方法
        allow_headers=["*"],  # 允许所有HTTP头
    )
