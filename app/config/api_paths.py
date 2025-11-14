# config/api_paths.py


class APIPaths:
    # 基础URL前缀
    API_ROOT = "/"

    # 版本编号
    API_VERSION = "v1"

    # 版本接口
    API_PREFIX = f"{API_ROOT}{API_VERSION}"

    # 健康检查接口
    HEALTH_CHECK = f"{API_PREFIX}/health"

    # 钉钉回调接口
    CALLBACK_VERIFY = f"{API_PREFIX}/callback"
