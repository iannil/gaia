"""
GAIA Integration - MCP

Model Context Protocol (MCP) 网关实现。
"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import json
from pathlib import Path


class MCPRole(str, Enum):
    """MCP 角色类型"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"


class MCPMessageType(str, Enum):
    """MCP 消息类型"""
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"
    ERROR = "error"


@dataclass
class MCPMessage:
    """MCP 消息"""
    id: str
    type: MCPMessageType
    role: MCPRole
    content: str
    data: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type.value,
            "role": self.role.value,
            "content": self.content,
            "data": self.data,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MCPMessage":
        return cls(
            id=data["id"],
            type=MCPMessageType(data["type"]),
            role=MCRole(data["role"]),
            content=data["content"],
            data=data.get("data", {}),
            timestamp=data.get("timestamp", ""),
        )


@dataclass
class MCPContext:
    """MCP 上下文"""
    project_id: str
    session_id: str
    variables: Dict[str, Any] = field(default_factory=dict)
    history: List[MCPMessage] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_message(self, message: MCPMessage) -> None:
        """添加消息到历史"""
        self.history.append(message)

    def get_variables(self) -> Dict[str, Any]:
        """获取变量"""
        return self.variables.copy()

    def set_variable(self, key: str, value: Any) -> None:
        """设置变量"""
        self.variables[key] = value

    def to_dict(self) -> Dict[str, Any]:
        return {
            "project_id": self.project_id,
            "session_id": self.session_id,
            "variables": self.variables,
            "history": [m.to_dict() for m in self.history],
            "metadata": self.metadata,
        }


class MCPTool:
    """MCP 工具定义"""

    def __init__(
        self,
        name: str,
        description: str,
        handler: Callable,
        parameters: Optional[Dict[str, Any]] = None,
    ):
        self.name = name
        self.description = description
        self.handler = handler
        self.parameters = parameters or {}

    async def execute(self, arguments: Dict[str, Any]) -> Any:
        """执行工具"""
        return await self.handler(**arguments)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }


class MCPGateway:
    """MCP 网关

    实现 Model Context Protocol，连接 AI 助手和 GAIA 框架。
    """

    def __init__(self):
        self._tools: Dict[str, MCPTool] = {}
        self._contexts: Dict[str, MCPContext] = {}
        self._handlers: Dict[str, Callable] = {}

    # ========== 工具管理 ==========

    def register_tool(
        self,
        name: str,
        description: str,
        handler: Callable,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> None:
        """注册工具"""
        tool = MCPTool(name, description, handler, parameters)
        self._tools[name] = tool

    def unregister_tool(self, name: str) -> bool:
        """取消注册工具"""
        if name in self._tools:
            del self._tools[name]
            return True
        return False

    def get_tools(self) -> List[Dict[str, Any]]:
        """获取所有工具"""
        return [tool.to_dict() for tool in self._tools.values()]

    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """调用工具"""
        tool = self._tools.get(name)
        if not tool:
            raise ValueError(f"工具不存在: {name}")

        return await tool.execute(arguments)

    # ========== 上下文管理 ==========

    def create_context(
        self,
        project_id: str,
        session_id: str,
    ) -> MCPContext:
        """创建上下文"""
        context = MCPContext(
            project_id=project_id,
            session_id=session_id,
        )
        key = f"{project_id}:{session_id}"
        self._contexts[key] = context
        return context

    def get_context(self, project_id: str, session_id: str) -> Optional[MCPContext]:
        """获取上下文"""
        key = f"{project_id}:{session_id}"
        return self._contexts.get(key)

    def remove_context(self, project_id: str, session_id: str) -> bool:
        """删除上下文"""
        key = f"{project_id}:{session_id}"
        if key in self._contexts:
            del self._contexts[key]
            return True
        return False

    # ========== 消息处理 ==========

    def register_handler(self, event_type: str, handler: Callable) -> None:
        """注册事件处理器"""
        self._handlers[event_type] = handler

    async def process_message(
        self,
        message: MCPMessage,
        context: Optional[MCPContext] = None,
    ) -> MCPMessage:
        """处理消息"""
        if context:
            context.add_message(message)

        # 根据消息类型处理
        if message.type == MCPMessageType.REQUEST:
            return await self._handle_request(message, context)
        elif message.type == MCPMessageType.NOTIFICATION:
            await self._handle_notification(message, context)
            return message

        return message

    async def _handle_request(
        self,
        message: MCPMessage,
        context: Optional[MCPContext],
    ) -> MCPMessage:
        """处理请求消息"""
        # 解析请求
        data = message.data
        action = data.get("action", "")

        if action == "call_tool":
            tool_name = data.get("tool")
            arguments = data.get("arguments", {})
            result = await self.call_tool(tool_name, arguments)

            return MCPMessage(
                id=f"resp_{message.id}",
                type=MCPMessageType.RESPONSE,
                role=MCPRole.TOOL,
                content=str(result),
                data={"result": result},
            )

        elif action == "get_tools":
            tools = self.get_tools()

            return MCPMessage(
                id=f"resp_{message.id}",
                type=MCPMessageType.RESPONSE,
                role=MCPRole.ASSISTANT,
                content="可用工具列表",
                data={"tools": tools},
            )

        return MCPMessage(
            id=f"resp_{message.id}",
            type=MCPMessageType.RESPONSE,
            role=MCPRole.ASSISTANT,
            content="未知请求",
        )

    async def _handle_notification(
        self,
        message: MCPMessage,
        context: Optional[MCPContext],
    ) -> None:
        """处理通知消息"""
        event_type = message.data.get("event", "")
        handler = self._handlers.get(event_type)

        if handler:
            await handler(message, context)

    # ========== GAIA 集成 ==========

    def setup_gaia_tools(self) -> None:
        """设置 GAIA 相关工具"""
        from gaia_core import GAIAEngine, Phase, Priority

        # gaia.phase.generate
        async def phase_generate(problem_statement: str, path: str = "market") -> Dict[str, Any]:
            from gaia_core import GeneratePath
            path_map = {
                "market": GeneratePath.MARKET_FIRST,
                "github": GeneratePath.GITHUB_FIRST,
                "masters": GeneratePath.MASTERS_FIRST,
            }

            engine = GAIAEngine("default")
            success, error = engine.start_generate(problem_statement, path_map.get(path, GeneratePath.MARKET_FIRST))

            return {"success": success, "error": error}

        self.register_tool(
            "gaia.phase.generate",
            "启动 GAIA Phase G: 生成阶段",
            phase_generate,
            parameters={
                "problem_statement": {"type": "string", "description": "问题陈述"},
                "path": {"type": "string", "description": "解决方案路径 (market/github/masters)", "default": "market"},
            },
        )

        # gaia.phase.advance
        async def phase_advance(project: str = "default") -> Dict[str, Any]:
            engine = GAIAEngine(project)
            success, error = engine.advance_phase()
            return {"success": success, "error": error, "current_phase": str(engine.current_phase)}

        self.register_tool(
            "gaia.phase.advance",
            "推进到下一 GAIA 阶段",
            phase_advance,
            parameters={
                "project": {"type": "string", "description": "项目名称", "default": "default"},
            },
        )

        # gaia.status
        async def gaia_status(project: str = "default") -> Dict[str, Any]:
            engine = GAIAEngine(project)
            return engine.get_status()

        self.register_tool(
            "gaia.status",
            "获取 GAIA 项目状态",
            gaia_status,
            parameters={
                "project": {"type": "string", "description": "项目名称", "default": "default"},
            },
        )

    def setup_skill_tools(self) -> None:
        """设置 Skill 相关工具"""
        from gaia_skills import SkillManager

        manager = SkillManager()

        # skill.list
        async def skill_list(category: Optional[str] = None, tag: Optional[str] = None) -> List[Dict[str, Any]]:
            return manager.list_skills(category=category, tag=tag)

        self.register_tool(
            "skill.list",
            "列出已安装的 Skills",
            skill_list,
            parameters={
                "category": {"type": "string", "description": "分类筛选"},
                "tag": {"type": "string", "description": "标签筛选"},
            },
        )

        # skill.search
        async def skill_search(query: str) -> List[Dict[str, Any]]:
            return manager.search_skills(query)

        self.register_tool(
            "skill.search",
            "搜索 Skills",
            skill_search,
            parameters={
                "query": {"type": "string", "description": "搜索关键词"},
            },
        )

    def setup_knowledge_tools(self) -> None:
        """设置知识相关工具"""
        from gaia_knowledge import PatternLibrary

        # patterns.list
        async def patterns_list(category: Optional[str] = None) -> List[Dict[str, Any]]:
            library = PatternLibrary()
            library.load_builtin_patterns()

            if category:
                patterns = library.list_by_category(category)
            else:
                patterns = library.list_by_type("best_practice")

            return [p.to_dict() for p in patterns]

        self.register_tool(
            "patterns.list",
            "获取最佳实践模式",
            patterns_list,
            parameters={
                "category": {"type": "string", "description": "分类筛选"},
            },
        )

        # patterns.search
        async def patterns_search(query: str) -> List[Dict[str, Any]]:
            library = PatternLibrary()
            library.load_builtin_patterns()

            patterns = library.search(query)
            return [p.to_dict() for p in patterns]

        self.register_tool(
            "patterns.search",
            "搜索模式",
            patterns_search,
            parameters={
                "query": {"type": "string", "description": "搜索关键词"},
            },
        )


__all__ = [
    "MCPRole",
    "MCPMessageType",
    "MCPMessage",
    "MCPContext",
    "MCPTool",
    "MCPGateway",
]
