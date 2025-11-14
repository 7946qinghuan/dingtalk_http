from fastapi import APIRouter, HTTPException, Query
import logging

from app.schemas.callback import DingCallbackRequest, DingCallbackResponse
from app.config import api_paths
from app.services.ding_http_callback_services import ding_callback

logger = logging.getLogger(__name__)


router = APIRouter(tags=["钉钉回调接口"])


@router.post(
    path=api_paths.CALLBACK_VERIFY,
    response_model=DingCallbackResponse,
    description="接收钉钉回调推送，返回加密响应",
)
async def verify_dingtalk_callback(
    body: DingCallbackRequest,
    msg_signature: str = Query(..., alias="signature"),
    timestamp: str = Query(..., alias="timestamp"),
    nonce: str = Query(..., alias="nonce"),
):
    """
    接收并处理钉钉的回调。
    - 从 Query 中提取 signature, timestamp, nonce
    - 从 Body 中提取 encrypt
    - 调用服务层处理
    - 返回标准加密响应
    """
    try:
        logger.debug(
            f"收到回调请求: sig={msg_signature}, ts={timestamp}, nonce={nonce}"
        )
        # 2. 调用服务层处理回调事件
        resp_data = ding_callback(msg_signature, timestamp, nonce, body.encrypt)
        logger.debug(f"回调处理成功, 返回数据: {resp_data}")
        return resp_data

    except HTTPException:
        # 重新抛出已知的HTTP异常 (来自服务层)
        raise
    except Exception as e:
        # 捕获其他未知异常
        logger.error(f"处理回调时发生未知错误: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"处理回调时发生错误: {str(e)}")
