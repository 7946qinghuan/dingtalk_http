from fastapi import APIRouter

from app.schemas.health import HealthCheckResponse
from app.middleware.logging_middleware import LoggingRoute
from app.config import api_paths

router = APIRouter(tags=["健康检查"], route_class=LoggingRoute)


# 健康检查接口
@router.get(path=api_paths.HEALTH_CHECK, response_model=HealthCheckResponse)
async def health_check():
    """检查服务是否正常运行"""
    return HealthCheckResponse()
