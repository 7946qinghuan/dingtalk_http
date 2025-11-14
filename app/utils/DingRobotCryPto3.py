import time
import hmac
import hashlib
import base64
import logging

# 获取日志
logger = logging.getLogger(__name__)


class DingRobotCrypto3:
    """
    用于钉钉机器人回调签名的验证类
    """

    def __init__(self, app_secret: str):
        """
        使用不会改变的 'app_secret' 初始化
        """
        if not app_secret:
            raise ValueError("DingRobotCrypto3 初始化失败: app_secret 不能为空")
        self.app_secret = app_secret

    def verify_signature(
        self,
        timestamp: str,
        sign: str,
    ) -> bool:
        """
        根据钉钉机器人文档，验证 HmacSHA256 签名

        :param timestamp: 来自请求 Header 的毫秒时间戳
        :param sign: 来自请求 Header 的签名
        :return: bool - 验证是否通过
        """
        if not timestamp or not sign:
            return False

        # 1. 校验时间戳 (1小时内有效)
        try:
            ts_now = int(time.time() * 1000)  # 当前毫秒
            ts_req = int(timestamp)
            if abs(ts_now - ts_req) > 3600000:  # 1 hour * 60 min * 60 sec * 1000 ms
                logger.warning(
                    f"机器人签名校验失败: 时间戳过期. (Now: {ts_now}, Req: {ts_req})"
                )
                return False
        except ValueError:
            logger.warning("机器人签名校验失败: 时间戳格式错误")
            return False

        # 2. 计算签名
        # 签名字符串 = timestamp + "\n" + 机器人的appSecret
        string_to_sign = f"{timestamp}\n{self.app_secret}"

        # 使用HmacSHA256算法计算签名
        try:
            # 密钥
            secret_bytes = self.app_secret.encode("utf-8")
            # 待签名字符串
            message_bytes = string_to_sign.encode("utf-8")

            hmac_sha256 = hmac.new(
                secret_bytes, message_bytes, digestmod=hashlib.sha256
            ).digest()

            # Base64 编码
            expected_sign = base64.b64encode(hmac_sha256).decode("utf-8")

            # 3. 比较签名
            if expected_sign == sign:
                return True
            else:
                logger.warning(
                    f"机器人签名校验失败: 签名不匹配. (Expected: {expected_sign}, Got: {sign})"
                )
                return False

        except Exception as e:
            logger.error(f"机器人签名计算时发生异常: {e}", exc_info=True)
            return False
