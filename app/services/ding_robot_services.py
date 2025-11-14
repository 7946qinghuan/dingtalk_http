import logging
from fastapi import HTTPException, Header

from app.utils.DingRobotCryPto3 import DingRobotCrypto3
from app.config import settings
from app.schemas.ding_robot import (
    DingRobotRequest,
    MsgType,
)

logger = logging.getLogger(__name__)


# --- 初始化 Crypto 实例 ---
try:
    robot_crypto = DingRobotCrypto3(app_secret=settings.Client_Secret)
except Exception as e:
    logger.error(f"DingRobotCrypto3 初始化失败: {e}", exc_info=True)
    robot_crypto = None


# --- 安全验证依赖项 ---
async def verify_robot_security(
    timestamp: str = Header(..., description="毫秒级时间戳"),
    sign: str = Header(..., description="HmacSHA256 签名"),
):
    """
    FastAPI 依赖项，使用 DingRobotCrypto3 实例验证签名
    """
    if robot_crypto is None:
        raise HTTPException(status_code=500, detail="服务器签名验证配置不完整")

    # 2. 调用类的方法
    if not robot_crypto.verify_signature(timestamp, sign):
        logger.error("机器人回调安全验证失败")
        raise HTTPException(status_code=403, detail="Signature verification failed")
    # 验证通过
    return True


# --- 业务逻辑服务 ---
async def handle_robot_logic(body: DingRobotRequest):
    """
    钉钉机器人的核心业务逻辑
    """
    try:
        if body.msgtype == MsgType.TEXT.value:
            received_content = body.text.content.strip()
            logger.info(f"收到来自 {body.senderNick} 的文本消息: {received_content}")

        elif body.msgtype == MsgType.PICTURE.value:
            logger.info(f"收到来自 {body.senderNick} 的图片消息")

        elif body.msgtype == MsgType.AUDIO.value:
            logger.info(f"收到来自 {body.senderNick} 的音频消息")

        elif body.msgtype == MsgType.VIDEO.value:
            logger.info(f"收到来自 {body.senderNick} 的视频消息")

        elif body.msgtype == MsgType.FILE.value:
            logger.info(f"收到来自 {body.senderNick} 的文件消息")

        elif body.msgtype == MsgType.RICH_TEXT.value:
            logger.info(f"收到来自 {body.senderNick} 的富文本消息")
        else:
            logger.info(
                f"收到来自 {body.senderNick} 的其他类型消息: {body.msgtype.value}"
            )

    except Exception as e:
        # 捕获业务逻辑中的未知错误
        logger.error(f"机器人业务逻辑处理失败: {e}", exc_info=True)
        return None
