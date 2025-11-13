# core/__init__.py
import logging
from .lifespan import lifespan

# 配置日志，以便在初始化时就能看到输出
logging.basicConfig(level=logging.INFO)

__all__ = ["lifespan"]
