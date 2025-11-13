# config/api_paths.py


class APIPaths:
    # 基础URL前缀（统一管理版本，后续升级只需改这里）
    API_PREFIX = "/v1"

    # 健康检查接口
    HEALTH_CHECK = f"{API_PREFIX}/health"

    # 钉钉回调接口
    CALLBACK_VERIFY = f"{API_PREFIX}/callback"
