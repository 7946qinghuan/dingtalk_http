import logging
from fastapi import Request, Response
from fastapi.routing import APIRoute
from time import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger("fastapi.middleware.logging")


class LoggingRoute(APIRoute):
    """自定义路由类：记录每个请求的详细信息（方法、路径、耗时、状态码）"""

    def get_route_handler(self):
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            # 记录请求开始时间
            start_time = time()
            # 记录请求信息
            logger.info(
                f"REQUEST - Method: {request.method}, Path: {request.url.path}, "
                f"Query: {dict(request.query_params)}, Client: {request.client.host}"
            )
            try:
                # 执行原路由逻辑（处理请求）
                response = await original_route_handler(request)
            except Exception as e:
                # 记录异常
                logger.error(f"ERROR - Path: {request.url.path}, Error: {str(e)}")
                raise e  # 重新抛出异常，让FastAPI处理
            # 记录响应信息
            process_time = time() - start_time
            logger.info(
                f"RESPONSE - Path: {request.url.path}, Status Code: {response.status_code}, "
                f"Process Time: {process_time:.4f}s"
            )
            return response

        return custom_route_handler
