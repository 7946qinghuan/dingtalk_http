from fastapi import APIRouter
from config.settings import settings
from schemas.health import HealthCheckResponse
from middleware.logging_middleware import LoggingRoute


router = APIRouter(tags=["健康检查"], route_class=LoggingRoute)

# 健康检查接口
path = settings.API_HEALTH_CHECK_URL


@router.get(path=path, response_model=HealthCheckResponse)
async def health_check():
    """检查服务是否正常运行"""
    return HealthCheckResponse()
