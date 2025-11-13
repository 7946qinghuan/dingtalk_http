import json
from fastapi import HTTPException
from app.utils.DingCallbackCrypto3 import DingCallbackCrypto3
from app.config import settings
import logging

# 获取日志
logger = logging.getLogger(__name__)

try:
    dingcrypto = DingCallbackCrypto3(
        token=settings.token,
        encodingAesKey=settings.ase_key,
        key=settings.Client_ID,
    )
except Exception as e:
    logger.error(f"初始化加解密工具失败，请检查key长度是否正确: {e}")
    dingcrypto = None


def ding_callback(msg_signature: str, timeStamp: str, nonce: str, encrypt_content: str):
    if dingcrypto is None:
        logger.critical("钉钉回调加解密模块未成功初始化!")
        raise HTTPException(status_code=500, detail="服务器内部配置错误")

    try:
        # 1. 验证签名+解密
        decrypted_msg = dingcrypto.getDecryptMsg(
            msg_signature, timeStamp, nonce, encrypt_content
        )
        logger.info(f"解密后的事件明文: {decrypted_msg}")

        # 2. 解析事件数据
        try:
            event_data = json.loads(decrypted_msg)
            event_type = event_data.get("EventType")
            logger.info(f"收到事件类型: {event_type}")
        except json.JSONDecodeError as e:
            logger.error(f"事件明文不是有效的JSON: {e}")
            raise HTTPException(status_code=400, detail="请求数据格式错误")

        # 3. 处理更具体的事件类型 ---

        # A. 处理“验证回调URL有效性”事件
        if event_type == "check_url":
            # 这通常是ISV应用或新版企业应用在后台点击“验证有效性”时收到的
            logger.info(f"收到回调URL验证请求: {event_type}")

        elif event_type in ("check_create_suite_url", "check_update_suite_url"):
            # 这通常是ISV应用或新版企业应用在后台点击“验证有效性”时收到的
            logger.info(f"收到回调URL验证请求: {event_type}")
            # 钉钉文档要求此时返回加密的 "success"

        # # B. 处理“suite_ticket”推送 (ISV应用必须)
        # elif event_type == "suite_ticket":
        #     ticket = event_data.get("SuiteTicket")
        #     logger.info(f"收到 SuiteTicket: {ticket[:10]}...")
        #     # TODO: 你必须在这里将 suite_ticket 持久化存储 (例如存入 Redis 或 数据库)
        #     response_content = "success"

        # C. 处理业务事件 (例如：员工入职)
        elif event_type == "user_add_org":
            user_id = event_data.get("UserId")
            logger.info(f"处理员工入职事件: {user_id}")
            # TODO: 在这里执行你的业务逻辑

        # D. 其他你订阅的事件...

        else:
            logger.info(f"收到未处理的事件类型: {event_type}")
            raise HTTPException(status_code=400, detail=f"未处理事件类型: {event_type}")

        # 3. 生成加密响应
        response_content = "success"
        resp_data = dingcrypto.getEncryptedMap(response_content)

        # 4. 返回响应字典
        return resp_data

    except ValueError as e:
        # 官方工具类抛出的异常（签名失败、key校验错误等）
        logger.warning(f"钉钉回调校验异常：{str(e)}")
        raise HTTPException(status_code=403, detail=f"Forbidden: {str(e)}")
    except HTTPException:
        # 重新抛出已知的HTTP异常
        raise
    except Exception as e:
        # 其他未知异常
        logger.error(f"处理钉钉回调时发生未知异常：{str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="服务器内部错误")
