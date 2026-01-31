"""
GAIA Web - Backend

FastAPI 后端服务。
"""

from typing import Dict, List, Any, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from gaia_integration.api import GAIAAPI, get_api


# ========== 请求/响应模型 ==========

class PhaseGenerateRequest(BaseModel):
    """Phase G 请求"""
    project: str
    problem: str
    path: str = "market"


class PhaseAdvanceRequest(BaseModel):
    """Phase 推进请求"""
    project: str


class SkillInstallRequest(BaseModel):
    """Skill 安装请求"""
    source: str
    skill_id: Optional[str] = None


class TemplateRenderRequest(BaseModel):
    """模板渲染请求"""
    template_id: str
    values: Dict[str, Any]


class IntegrationRegisterRequest(BaseModel):
    """集成注册请求"""
    service: str
    config: Dict[str, Any]


class IntegrationCallRequest(BaseModel):
    """集成调用请求"""
    service: str
    action: str
    parameters: Dict[str, Any] = {}


class WorkflowExecuteRequest(BaseModel):
    """工作流执行请求"""
    workflow: Dict[str, Any]
    variables: Dict[str, Any] = {}


# ========== FastAPI 应用 ==========

def create_app() -> FastAPI:
    """创建 FastAPI 应用"""
    app = FastAPI(
        title="GAIA API",
        description="GAIA AI 协作框架 API",
        version="0.1.0",
    )

    # CORS 中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 获取 API 实例
    api = get_api()

    # ========== 健康检查 ==========

    @app.get("/")
    def read_root() -> Dict[str, Any]:
        """根路径"""
        return {
            "name": "GAIA API",
            "version": "0.1.0",
            "status": "running",
            "docs": "/docs",
        }

    @app.get("/health")
    def health_check() -> Dict[str, Any]:
        """健康检查"""
        return {"status": "healthy"}

    @app.get("/status")
    def api_status() -> Dict[str, Any]:
        """API 状态"""
        return api.status().to_dict()

    # ========== Phase 端点 ==========

    @app.post("/api/v1/phase/generate")
    def phase_generate(req: PhaseGenerateRequest) -> Dict[str, Any]:
        """启动 Phase G"""
        result = api.phase_generate(req.project, req.problem, req.path)
        raise_if_error(result)
        return result.to_dict()

    @app.post("/api/v1/phase/advance")
    def phase_advance(req: PhaseAdvanceRequest) -> Dict[str, Any]:
        """推进阶段"""
        result = api.phase_advance(req.project)
        raise_if_error(result)
        return result.to_dict()

    @app.get("/api/v1/phase/status")
    def get_phase_status(project: str) -> Dict[str, Any]:
        """获取阶段状态"""
        result = api.phase_status(project)
        raise_if_error(result)
        return result.to_dict()

    # ========== Skill 端点 ==========

    @app.get("/api/v1/skills")
    def list_skills(
        category: Optional[str] = None,
        tag: Optional[str] = None,
    ) -> Dict[str, Any]:
        """列出 Skills"""
        result = api.skill_list(category=category, tag=tag)
        raise_if_error(result)
        return result.to_dict()

    @app.get("/api/v1/skills/search")
    def search_skills(query: str) -> Dict[str, Any]:
        """搜索 Skills"""
        result = api.skill_search(query)
        raise_if_error(result)
        return result.to_dict()

    @app.post("/api/v1/skills/install")
    def install_skill(req: SkillInstallRequest) -> Dict[str, Any]:
        """安装 Skill"""
        result = api.skill_install(req.source, req.skill_id)
        raise_if_error(result)
        return result.to_dict()

    @app.get("/api/v1/skills/{skill_id}")
    def get_skill_info(skill_id: str) -> Dict[str, Any]:
        """获取 Skill 信息"""
        from gaia_skills import SkillManager
        manager = SkillManager()
        info = manager.get_skill_info(skill_id)
        if info:
            return {"success": True, "data": info}
        raise HTTPException(status_code=404, detail=f"Skill 未找到: {skill_id}")

    # ========== Knowledge 端点 ==========

    @app.get("/api/v1/knowledge/search")
    def search_knowledge(
        query: str,
        limit: int = 10,
    ) -> Dict[str, Any]:
        """搜索知识库"""
        result = api.knowledge_search(query, limit=limit)
        raise_if_error(result)
        return result.to_dict()

    @app.get("/api/v1/patterns")
    def list_patterns(
        category: Optional[str] = None,
    ) -> Dict[str, Any]:
        """列出模式"""
        result = api.patterns_list(category=category)
        raise_if_error(result)
        return result.to_dict()

    # ========== Template 端点 ==========

    @app.get("/api/v1/templates")
    def list_templates(
        category: Optional[str] = None,
    ) -> Dict[str, Any]:
        """列出模板"""
        result = api.template_list(category=category)
        raise_if_error(result)
        return result.to_dict()

    @app.post("/api/v1/templates/render")
    def render_template(req: TemplateRenderRequest) -> Dict[str, Any]:
        """渲染模板"""
        result = api.template_render(req.template_id, req.values)
        raise_if_error(result)
        return result.to_dict()

    # ========== Integration 端点 ==========

    @app.post("/api/v1/integrations")
    def register_integration(req: IntegrationRegisterRequest) -> Dict[str, Any]:
        """注册集成"""
        result = api.integration_register(req.service, req.config)
        raise_if_error(result)
        return result.to_dict()

    @app.post("/api/v1/integrations/{service}/call")
    def call_integration(
        service: str,
        req: IntegrationCallRequest,
    ) -> Dict[str, Any]:
        """调用集成"""
        result = api.integration_call(service, req.action, **req.parameters)
        raise_if_error(result)
        return result.to_dict()

    @app.get("/api/v1/integrations")
    def list_integrations() -> Dict[str, Any]:
        """列出集成"""
        status = api.status()
        return {
            "success": True,
            "data": {"services": status.to_dict()["data"]["integrations"]},
        }

    # ========== Workflow 端点 ==========

    @app.post("/api/v1/workflows/execute")
    def execute_workflow(req: WorkflowExecuteRequest) -> Dict[str, Any]:
        """执行工作流"""
        result = api.workflow_execute(req.workflow, req.variables)
        raise_if_error(result)
        return result.to_dict()

    return app


def raise_if_error(result) -> None:
    """如果结果有错误则抛出 HTTP 异常"""
    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)


# ========== 应用实例 ==========

app = create_app()


def run_server(
    host: str = "0.0.0.0",
    port: int = 8000,
    reload: bool = False,
) -> None:
    """运行服务器

    Args:
        host: 监听地址
        port: 监听端口
        reload: 是否自动重载
    """
    uvicorn.run(
        "gaia_web.backend:app",
        host=host,
        port=port,
        reload=reload,
    )


__all__ = [
    "create_app",
    "app",
    "run_server",
]
