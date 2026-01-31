"""
GAIA Integration - Integration Framework

GAIA 集成框架。

提供:
- MCP: Model Context Protocol 网关
- Adapters: 统一适配器接口
- API: 统一 API 接口
"""

from .mcp import (
    MCPRole,
    MCPMessageType,
    MCPMessage,
    MCPContext,
    MCPTool,
    MCPGateway,
)
from .adapters import (
    Adapter,
    GitHubAdapter,
    GitHubConfig,
    NotionAdapter,
    NotionConfig,
    AdapterFactory,
    UnifiedAPI,
)
from .api import APIResponse, GAIAAPI, get_api

__version__ = "0.1.0"

__all__ = [
    # MCP
    "MCPRole",
    "MCPMessageType",
    "MCPMessage",
    "MCPContext",
    "MCPTool",
    "MCPGateway",
    # Adapters
    "Adapter",
    "GitHubAdapter",
    "GitHubConfig",
    "NotionAdapter",
    "NotionConfig",
    "AdapterFactory",
    "UnifiedAPI",
    # API
    "APIResponse",
    "GAIAAPI",
    "get_api",
]
