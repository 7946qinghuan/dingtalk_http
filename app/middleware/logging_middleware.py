import json
import logging
from typing import Awaitable, Callable
from fastapi import Request, Response
from fastapi.routing import APIRoute
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response as StarletteResponse
from fastapi import FastAPI


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.handlers.RotatingFileHandler(
            "fastapi.log", maxBytes=1024 * 1024 * 10, backupCount=5
        ),
    ],
)

logger = logging.getLogger("fastapi.middleware.logging")


async def parse_request_body(request: Request) -> tuple[str, str]:
    """
    安全解析请求体（封装重复逻辑，避免代码冗余）
    返回：(body_type: 类型标识, body_content: 解析后的内容)
    """
    try:
        body_bytes = await request.body()
        if not body_bytes:
            return ("无", "无")

        body_str = body_bytes.decode(
            "utf-8", errors="replace"
        )  # 容错：非法UTF-8字符替换
        # 尝试解析JSON
        try:
            body_json = json.loads(body_str)
            return (
                "解析后（JSON）",
                json.dumps(body_json, ensure_ascii=False, indent=2),
            )
        except json.JSONDecodeError:
            # 非JSON格式（如表单、纯文本）
            return ("原始（非JSON）", body_str)  # 限制长度：避免大请求体刷屏
    except Exception as e:
        logger.error(f"解析请求体失败：{str(e)}")
        return ("解析失败", str(e))


class LoggingRoute(APIRoute):
    """自定义路由类：仅记录特定路由的业务日志（与中间件分工，避免重复）"""

    def get_route_handler(self):
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            start_time = time.time()
            route_path = request.url.path

            try:
                # 仅记录路由核心信息（详细请求体交给中间件）
                logger.info(f"ROUTE - 开始处理：{request.method} {route_path}")
                response = await original_route_handler(request)
                process_time = time.time() - start_time
                logger.info(
                    f"ROUTE - 处理完成：{route_path} | 耗时：{process_time:.4f}s | 状态码：{response.status_code}"
                )
                return response
            except Exception as e:
                logger.error(
                    f"ROUTE - 处理失败：{route_path} | 错误：{str(e)}", exc_info=True
                )  # 新增：打印异常堆栈
                raise e

        return custom_route_handler


# ------------------- 日志中间件（类形式，支持函数式注册）-------------------
class LogAllRequestsMiddleware(BaseHTTPMiddleware):
    """全局日志中间件：记录所有请求的完整上下文（请求头、请求体、响应信息）"""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[StarletteResponse]],
    ) -> StarletteResponse:
        start_time = time.time()
        request_id = str(id(request))[:8]

        # 1. 记录请求基础信息（优化：添加请求ID，方便关联请求-响应）
        logger.info(f"\n{'='*80}")
        logger.info(f"【请求ID：{request_id}】【请求信息】")
        logger.info(f"路径: {request.url.path}")
        logger.info(f"方法: {request.method}")
        logger.info(f"查询参数: {dict(request.query_params)}")
        logger.info(f"客户端: {request.client.host}:{request.client.port}")
        logger.info(
            f"请求头: {json.dumps(dict(request.headers), ensure_ascii=False, indent=2)}"
        )

        # 2. 解析并记录请求体（优化：调用工具函数，安全无副作用）
        body_type, body_content = await parse_request_body(request)
        logger.info(f"请求体（{body_type}）: {body_content}")

        # 3. 处理请求（优化：不修改 request._body，避免破坏原始请求）
        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(
                f"【请求ID：{request_id}】【请求处理异常】: {str(e)}", exc_info=True
            )
            raise e

        # 4. 记录响应信息（优化：关联请求ID，补充响应头摘要）
        process_time = time.time() - start_time
        logger.info(f"\n【请求ID：{request_id}】【响应信息】")
        logger.info(f"状态码: {response.status_code}")
        logger.info(
            f"响应头: {json.dumps(dict(response.headers), ensure_ascii=False, indent=2)}"
        )  # 限制长度
        logger.info(f"处理时间: {process_time:.2f}s")
        logger.info(f"{'='*80}")

        return response


# ------------------- 注册函数（优化：统一接口，支持灵活开关）-------------------
def add_log_middleware(app: FastAPI, use_logging_route: bool = False):
    """
    添加日志组件（中间件+可选路由类）
    :param use_logging_route: 是否启用路由级日志（默认关闭，避免重复）
    """
    # 注册全局中间件（必选：记录完整请求上下文）
    app.add_middleware(LogAllRequestsMiddleware)

    # 可选：注册路由级日志（仅在需要特定路由详细日志时启用）
    if use_logging_route:
        app.router.route_class = LoggingRoute
