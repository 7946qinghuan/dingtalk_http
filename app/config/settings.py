# config/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """
    全局配置类：统一管理所有配置。
    pydantic-settings会自动从环境变量和.env文件读取。
    """

    # model_config用于配置.env文件的加载
    # 告诉BaseSettings去查找.env文件
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # 钉钉机器人配置
    # 你不再需要 default=os.getenv("...") 这样的写法了
    # BaseSettings 会自动根据字段名（不区分大小写）去环境变量里找
    RobotCode: str = Field(description="钉钉机器人的RobotCode")
    AppID: str = Field(description="钉钉机器人的AppID")
    AgentID: str = Field(description="钉钉机器人的AgentID")
    Client_ID: str = Field(description="钉钉机器人的Client_ID (原 AppKey 和 SuiteKey)")
    Client_Secret: str = Field(
        description="钉钉机器人的Client_Secret (原 AppSecret 和 SuiteSecret)"
    )
    ase_key: str = Field(description="钉钉机器人的ase_key")
    token: str = Field(description="钉钉机器人的token")
    CorpID: str = Field(description="钉钉机器人的CorpID")
    API_Token: str = Field(description="钉钉机器人的API_Token")

    # 服务器配置
    SERVER_HOST: str = Field(description="服务器主机地址")
    SERVER_PORT: int = Field(description="服务器端口号")
