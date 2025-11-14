# DingTalk HTTP Callback Service
![image](https://img.shields.io/badge/python-3.11-blue.svg)
![image](https://img.shields.io/badge/Framework-FastAPI-green.svg)
![image](https://img.shields.io/badge/license-MIT-yellow.svg)
![image](https://img.shields.io/badge/code%20style-black-000000.svg)

一个基于 Python 和 FastAPI 的轻量级 Web 服务，专门用于接收和处理钉钉（DingTalk）开放平台通过 HTTP 推送的回调事件。项目内置了钉钉回调消息体签名校验、AES 加解密逻辑，完全遵循钉钉开放平台接口规范，开箱即用。

## ✨ 主要特性

- **高性能**: 基于 FastAPI + Uvicorn 构建，支持异步处理，高并发场景下响应迅速（满足钉钉 1500ms 响应要求）。
- **钉钉原生兼容**: 完美适配钉钉 HTTP 回调机制，支持事件订阅、卡片回调等所有钉钉推送场景。
- **安全合规**: 严格遵循钉钉官方安全规范，内置 SHA1 签名校验（非 SHA256，修正笔误）和 AES-256-CBC 加解密算法。
- **生产级可用**: 提供健康检查接口、结构化日志、异常统一处理，支持生产环境部署。
- **易扩展**: 分层架构设计（路由→服务→工具），业务逻辑与核心依赖解耦，便于扩展自定义事件处理。
- **开发友好**: 自动生成 Swagger 接口文档（`/docs`），支持类型提示，配置简单，测试便捷。
- **代码规范**: 集成 pre-commit 钩子，支持 black、flake8 等代码检查，保持代码风格统一。

## 🛠️ 技术栈

| 类别       | 技术选型                                         |
| ---------- | ------------------------------------------------ |
| Web 框架   | [FastAPI](https://fastapi.tiangolo.com/)         |
| 数据校验   | [Pydantic](https://pydantic-docs.helpmanual.io/) |
| Web 服务器 | [Uvicorn](https://www.uvicorn.org/)              |
| 加解密     | [pycryptodome](https://www.pycryptodome.org/)    |
| 配置管理   | python-dotenv + Pydantic Settings                |
| 依赖管理   | pip /poetry（支持 pyproject.toml）               |
| 测试工具   | [pytest](https://docs.pytest.org/)               |
| 代码规范   | black、flake8、isort                             |


## 📁 项目结构

```plaintext
dingtalk_http/
├── app/
│   ├── main.py                # 应用入口（初始化 FastAPI、注册路由）
│   ├── config/                # 配置模块
│   │   ├── settings.py        # 环境变量加载与配置定义
│   │   └── api_paths.py       # API 路径常量定义
│   ├── core/                  # 核心逻辑
│   │   └── events.py          # 应用生命周期事件（如启动、关闭）
│   ├── middleware/            # 中间件
│   │   ├── logging_middleware.py # 日志中间件（记录请求/响应）
│   │   └── cors_middleware.py    # 跨域中间件（按需启用）
│   ├── routers/               # 路由层（API 端点定义）
│   │   ├── ding_callback_router.py # 钉钉回调接口路由
│   │   └── health_router.py        # 健康检查路由
│   ├── schemas/               # Pydantic 数据模型（请求/响应校验）
│   │   └── callback.py        # 回调相关数据模型
│   ├── services/              # 业务逻辑层
│   │   └── ding_http_callback.py # 回调核心处理（加解密、签名校验）
│   └── utils/                 # 工具类
│       └── DingCallbackCrypto3.py # 钉钉官方适配的加解密工具类
├── tests/                     # 测试用例
│   ├── conftest.py            # 测试夹具（如客户端、配置）
│   └── test_ding_callback.py  # 回调接口测试
├── .env.example               # 环境变量示例（可复制为 .env）
├── .gitignore                 # Git 忽略文件
├── .pre-commit-config.yaml    # pre-commit 配置（代码规范检查）
├── pyproject.toml             # 项目依赖、代码规范配置
├── requirements.txt           # pip 依赖清单
├── run.py                     # 备用启动脚本
└── README.md                  # 项目说明文档
```
