"""
GAIA Web - Web Interface

GAIA Web 界面。

提供:
- Backend: FastAPI 后端服务
- Frontend: React 前端应用
"""

from .backend import create_app, app, run_server

__version__ = "0.1.0"

__all__ = [
    "create_app",
    "app",
    "run_server",
]
