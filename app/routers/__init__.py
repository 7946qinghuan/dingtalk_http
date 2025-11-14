from .health_router import router as health_router
from .ding_callback_router import router as callback_router
from .ding_robot_router import router as robot_router

__all__ = ["health_router", "callback_router", "robot_router"]
