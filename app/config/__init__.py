# config/__init__.py
from .settings import Settings
from .api_paths import APIPaths

settings = Settings()
api_paths = APIPaths()

# 我们只导出这个实例，隐藏类的定义
__all__ = ["settings", "api_paths"]
