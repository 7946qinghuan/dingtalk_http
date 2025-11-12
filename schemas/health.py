from pydantic import BaseModel, Field
from datetime import datetime


class HealthCheckResponse(BaseModel):
    status: str = Field(default="healthy", description="服务状态")
    version: str = Field(default="1.0.0", description="服务版本")
    datetime: str = Field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        description="当前时间",
    )
