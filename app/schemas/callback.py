from pydantic import BaseModel, Field


class DingCallbackRequest(BaseModel):
    """钉钉回调验证有效性请求体"""

    encrypt: str = Field(description="加密后的请求体")


class DingCallbackResponse(BaseModel):
    """钉钉回调响应体（严格匹配钉钉字段名）"""

    msg_signature: str = Field(description="消息体签名")
    timeStamp: str = Field(description="时间戳（钉钉要求大写S）")
    nonce: str = Field(description="随机字符串")
    encrypt: str = Field(description="加密后的响应内容（如success）")
