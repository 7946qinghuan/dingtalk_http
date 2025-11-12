from fastapi import APIRouter

from config.settings import settings
from schemas.callback import VerificationRequest, VerificationResponse
from middleware.logging_middleware import LoggingRoute


router = APIRouter(tags=["钉钉回调接口"], route_class=LoggingRoute)

path = settings.API_CALLBACK_VERIFY_URL


@router.post(path=path, response_model=VerificationResponse)
async def verify_callback(request: VerificationRequest):
    """验证钉钉回调有效性"""
    if request:
        return {"status": "success"}
