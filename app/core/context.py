# core/context.py
import logging
from app.config import Settings  # 导入 Settings 类定义，而不是实例

# 获取一个日志记录器
logger = logging.getLogger(__name__)


class AppContext:
    """
    应用上下文管理器 (Service Registry)

    统一管理所有异步服务的初始化、持有和关闭。
    这是一个单一实例（Singleton）类，在整个应用生命周期中存在。
    """

    def __init__(self, settings: Settings):
        logger.info("正在创建应用上下文 (AppContext)...")
        self.settings = settings

        # ----------------------------------------------------
        # 1. 注册所有服务状态（初始化为 None）
        # ----------------------------------------------------
        # self.redis: Optional[Redis] = None
        # self.db_pool: Optional[asyncpg.Pool] = None # 如果用 asyncpg
        # 我们这里使用 Tortoise-ORM，它会自己管理连接
        logger.info("服务句柄已初始化为 None。")

    async def startup(self):
        """
        在应用启动时，统一调用所有服务的初始化函数。
        """
        logger.info("执行应用启动任务 (startup)...")
        # 按照你希望的顺序“注册”并初始化服务
        # ... await self._init_...() ...
        logger.info("所有服务均已启动。")

    async def shutdown(self):
        """
        在应用关闭时，统一调用所有服务的关闭函数。
        """
        logger.info("执行应用关闭任务 (shutdown)...")
        # 按照与启动相反的顺序关闭
        # ... await self._close_...() ...
        logger.info("所有服务均已安全关闭。")

    # ----------------------------------------------------
    # 2. 编写每个服务的“注册”（初始化）函数
    # ----------------------------------------------------
    # async def _init_redis(self):
    # async def _init_database(self):

    # ----------------------------------------------------
    # 3. 编写每个服务的“注销”（关闭）函数
    # ----------------------------------------------------
    # async def _close_redis(self):
    # async def _close_database(self):
