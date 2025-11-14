from fastapi import APIRouter, Depends
import logging


from app.schemas.ding_robot import (
    DingRobotRequest,
)


from app.services import ding_robot_services
from app.config import api_paths

# 获取日志
logger = logging.getLogger(__name__)
router = APIRouter(tags=["钉钉机器人回调"])


@router.post(
    path=api_paths.API_ROOT,
    # 3. 依赖项从 service 模块导入
    dependencies=[Depends(ding_robot_services.verify_robot_security)],
)
async def handle_robot_message(body: DingRobotRequest):
    """
    接收并处理来自钉钉机器人的@消息。
    安全校验已通过依赖项 (verify_robot_security) 自动完成。
    业务逻辑已委托给 service.
    """

    # 4. 路由层现在只负责调用服务层
    return await ding_robot_services.handle_robot_logic(body)
