# /app/main.py
import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.config import settings  # 导入全局唯一的 settings 实例
from app.core.context import AppContext  # 导入 AppContext 类

# 获取日志
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用的生命周期管理器
    """
    logger.info("应用开始启动...")
    context = AppContext(settings=settings)
    # 统一调用 AppContext 的 startup
    await context.startup()

    # 关键一步：将 context 实例挂在 app.state 上
    # 这样, 在请求处理函数中就可以通过 request.app.state.context 访问它
    app.state.context = context

    logger.info("应用启动完毕，准备就绪。")
    yield  # <-- 应用在这里运行

    logger.info("应用开始关闭...")
    # 统一调用 AppContext 的 shutdown
    await context.shutdown()
    logger.info("应用已安全关闭。")
