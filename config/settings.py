import os
from pydantic import Field, BaseModel
from dotenv import load_dotenv

load_dotenv(override=True, verbose=True)


class Settings(BaseModel):
    """全局配置类：统一管理所有配置，从环境变量读取"""

    # 钉钉机器人配置
    RobotCode: str = Field(
        default=os.getenv("RobotCode"), description="钉钉机器人的RobotCode"
    )
    AppID: str = Field(default=os.getenv("AppID"), description="钉钉机器人的AppID")
    AgentID: str = Field(
        default=os.getenv("AgentID"), description="钉钉机器人的AgentID"
    )
    Client_ID: str = Field(
        default=os.getenv("Client_ID"), description="钉钉机器人的Client_ID"
    )
    Client_Secret: str = Field(
        default=os.getenv("Client_Secret"), description="钉钉机器人的Client_Secret"
    )
    ase_key: str = Field(
        default=os.getenv("ase_key"), description="钉钉机器人的ase_key"
    )
    token: str = Field(default=os.getenv("token"), description="钉钉机器人的token")
    CorpID: str = Field(default=os.getenv("CorpID"), description="钉钉机器人的CorpID")
    API_Token: str = Field(
        default=os.getenv("API_Token"), description="钉钉机器人的API_Token"
    )

    # 钉钉项目API配置
    API_HEALTH_CHECK_URL: str = Field(
        default=os.getenv("API_HEALTH_CHECK_URL"),
        description="钉钉项目API的健康检查URL",
    )
    API_CALLBACK_VERIFY_URL: str = Field(
        default=os.getenv("API_CALLBACK_VERIFY_URL"), description="钉钉项目API的验证URL"
    )


# 创建配置实例（全局唯一，其他模块直接导入使用）
settings = Settings()
