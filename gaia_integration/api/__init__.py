"""
GAIA Integration - API

统一 API 接口。
"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
import asyncio

from ..adapters import UnifiedAPI, Adapter, AdapterFactory
from ..mcp import MCPGateway, MCPContext, MCPMessage


@dataclass
class APIResponse:
    """API 响应"""
    success: bool
    data: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "metadata": self.metadata or {},
        }


class GAIAAPI:
    """GAIA 统一 API

    提供统一的编程接口访问 GAIA 框架的所有功能。
    """

    def __init__(self):
        self.mcp = MCPGateway()
        self.integrations = UnifiedAPI()
        self._setup_integrations()

    def _setup_integrations(self) -> None:
        """设置集成"""
        # 设置 MCP 工具
        self.mcp.setup_gaia_tools()
        self.mcp.setup_skill_tools()
        self.mcp.setup_knowledge_tools()

    # ========== Phase API ==========

    def phase_generate(
        self,
        project: str,
        problem: str,
        path: str = "market",
    ) -> APIResponse:
        """启动 Phase G"""
        from gaia_core import GAIAEngine, GeneratePath

        path_map = {
            "market": GeneratePath.MARKET_FIRST,
            "github": GeneratePath.GITHUB_FIRST,
            "masters": GeneratePath.MASTERS_FIRST,
        }

        try:
            engine = GAIAEngine(project)
            success, error = engine.start_generate(problem, path_map.get(path, GeneratePath.MARKET_FIRST))

            if success:
                return APIResponse(success=True, data={"phase": "G", "engine": str(engine.current_phase)})
            else:
                return APIResponse(success=False, error=error)

        except Exception as e:
            return APIResponse(success=False, error=str(e))

    def phase_advance(self, project: str) -> APIResponse:
        """推进到下一阶段"""
        from gaia_core import GAIAEngine

        try:
            engine = GAIAEngine(project)
            success, error = engine.advance_phase()

            if success:
                return APIResponse(success=True, data={"current_phase": str(engine.current_phase)})
            else:
                return APIResponse(success=False, error=error)

        except Exception as e:
            return APIResponse(success=False, error=str(e))

    def phase_status(self, project: str) -> APIResponse:
        """获取阶段状态"""
        from gaia_core import GAIAEngine

        try:
            engine = GAIAEngine(project)
            return APIResponse(success=True, data=engine.get_status())

        except Exception as e:
            return APIResponse(success=False, error=str(e))

    # ========== Skill API ==========

    def skill_install(
        self,
        source: str,
        skill_id: Optional[str] = None,
    ) -> APIResponse:
        """安装 Skill"""
        from gaia_skills import SkillManager

        try:
            manager = SkillManager()

            if source.startswith("http"):
                success, message = manager.install_from_git(source, skill_id)
            elif "/" in source:
                success, message = manager.install_from_github(source, skill_id)
            else:
                return APIResponse(success=False, error="无效的来源")

            if success:
                return APIResponse(success=True, data={"message": message})
            else:
                return APIResponse(success=False, error=message)

        except Exception as e:
            return APIResponse(success=False, error=str(e))

    def skill_list(
        self,
        category: Optional[str] = None,
        tag: Optional[str] = None,
    ) -> APIResponse:
        """列出 Skills"""
        from gaia_skills import SkillManager

        try:
            manager = SkillManager()
            skills = manager.list_skills(category=category, tag=tag)

            return APIResponse(success=True, data={"skills": skills, "count": len(skills)})

        except Exception as e:
            return APIResponse(success=False, error=str(e))

    def skill_search(self, query: str) -> APIResponse:
        """搜索 Skills"""
        from gaia_skills import SkillManager

        try:
            manager = SkillManager()
            results = manager.search_skills(query)

            return APIResponse(success=True, data={"results": results, "count": len(results)})

        except Exception as e:
            return APIResponse(success=False, error=str(e))

    # ========== Knowledge API ==========

    def knowledge_search(self, query: str, limit: int = 10) -> APIResponse:
        """搜索知识库"""
        from gaia_knowledge import SemanticSearch

        try:
            search = SemanticSearch()
            results = search.search(query, limit=limit)

            return APIResponse(success=True, data={"results": [r.to_dict() for r in results]})

        except Exception as e:
            return APIResponse(success=False, error=str(e))

    def patterns_list(self, category: Optional[str] = None) -> APIResponse:
        """列出模式"""
        from gaia_knowledge import PatternLibrary

        try:
            library = PatternLibrary()
            library.load_builtin_patterns()

            if category:
                patterns = library.list_by_category(category)
            else:
                patterns = library.list_by_type("best_practice")

            return APIResponse(success=True, data={"patterns": [p.to_dict() for p in patterns]})

        except Exception as e:
            return APIResponse(success=False, error=str(e))

    # ========== Template API ==========

    def template_render(
        self,
        template_id: str,
        values: Dict[str, Any],
    ) -> APIResponse:
        """渲染模板"""
        from gaia_templates import TemplateEngine

        try:
            engine = TemplateEngine()
            engine.load_builtin_templates()

            result = engine.render(template_id, values)

            if result is not None:
                return APIResponse(success=True, data={"content": result})
            else:
                return APIResponse(success=False, error=f"模板未找到: {template_id}")

        except Exception as e:
            return APIResponse(success=False, error=str(e))

    def template_list(self, category: Optional[str] = None) -> APIResponse:
        """列出模板"""
        from gaia_templates import TemplateEngine

        try:
            engine = TemplateEngine()
            engine.load_builtin_templates()

            templates = engine.list_templates(category=category)

            return APIResponse(success=True, data={"templates": [t.to_dict() for t in templates]})

        except Exception as e:
            return APIResponse(success=False, error=str(e))

    # ========== Integration API ==========

    def integration_register(
        self,
        service: str,
        config: Dict[str, Any],
    ) -> APIResponse:
        """注册集成服务"""
        try:
            adapter = AdapterFactory.create(service, config)
            self.integrations.register_adapter(service, adapter)

            return APIResponse(success=True, data={"service": service})

        except Exception as e:
            return APIResponse(success=False, error=str(e))

    def integration_call(
        self,
        service: str,
        action: str,
        **kwargs,
    ) -> APIResponse:
        """调用集成服务"""
        try:
            result = self.integrations.call(service, action, **kwargs)

            return APIResponse(success=True, data=result)

        except Exception as e:
            return APIResponse(success=False, error=str(e))

    # ========== Workflow API ==========

    def workflow_execute(
        self,
        workflow: Dict[str, Any],
        variables: Optional[Dict[str, Any]] = None,
    ) -> APIResponse:
        """执行工作流"""
        from gaia_workflow import Workflow, WorkflowExecutor

        try:
            workflow_obj = Workflow.from_dict(workflow)
            executor = WorkflowExecutor()
            execution = executor.execute_sync(workflow_obj, variables)

            return APIResponse(
                success=execution.status.value == "completed",
                data=execution.to_dict(),
            )

        except Exception as e:
            return APIResponse(success=False, error=str(e))

    # ========== Utility API ==========

    def status(self) -> APIResponse:
        """获取 API 状态"""
        return APIResponse(
            success=True,
            data={
                "mcp_tools": len(self.mcp.get_tools()),
                "integrations": self.integrations.get_services(),
                "version": "0.1.0",
            },
        )


# 全局 API 实例
_api_instance: Optional[GAIAAPI] = None


def get_api() -> GAIAAPI:
    """获取全局 API 实例"""
    global _api_instance
    if _api_instance is None:
        _api_instance = GAIAAPI()
    return _api_instance


__all__ = [
    "APIResponse",
    "GAIAAPI",
    "get_api",
]
