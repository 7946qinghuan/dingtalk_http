from pydantic import BaseModel, Field


class VerificationRequest(BaseModel):
    """钉钉回调验证有效性请求体"""

    encrypt: str = Field(description="加密后的请求体")


class VerificationResponse(BaseModel):
    """钉钉回调验证有效性响应体"""

    msg_signature: str = Field(description="消息体签名")
    timestamp: str = Field(description="时间戳")
    nonce: str = Field(description="随机字符串")
    encrypt: str = Field(description="success加密字符串")
