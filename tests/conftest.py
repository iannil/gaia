"""
Pytest 配置和 fixtures
"""

import pytest
import tempfile
from pathlib import Path
from typing import Generator

from gaia_core import GAIAState
from gaia_skills import SkillManager, EvolutionManager
from gaia_knowledge import KnowledgeGraph, PatternLibrary
from gaia_templates import TemplateEngine
from gaia_workflow import WorkflowBuilder
from gaia_integration import MCPGateway


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """临时目录 fixture"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_state() -> GAIAState:
    """示例状态 fixture"""
    state = GAIAState(
        project_id="test-project",
        project_name="Test Project",
    )
    state.add_task("P0 Task", Priority.P0)
    state.add_task("P1 Task", Priority.P1)
    return state


@pytest.fixture
def sample_graph() -> KnowledgeGraph:
    """示例知识图谱 fixture"""
    from gaia_knowledge import Node, Edge

    graph = KnowledgeGraph()
    graph.add_node(Node(id="skill1", type="skill", label="Git"))
    graph.add_node(Node(id="skill2", type="skill", label="GitHub"))
    graph.add_edge(Edge(id="edge1", source="skill1", target="skill2", relation="similar_to"))
    return graph


@pytest.fixture
def sample_template_engine() -> TemplateEngine:
    """示例模板引擎 fixture"""
    engine = TemplateEngine()
    engine.load_builtin_templates()
    return engine


@pytest.fixture
def sample_workflow() -> dict:
    """示例工作流 fixture"""
    builder = WorkflowBuilder("test-workflow", "Test Workflow")
    builder.step("step1", "echo", parameters={"message": "Hello"})
    builder.step("step2", "echo", parameters={"message": "World"}, depends_on=["step1"])
    return builder.build().to_dict()


@pytest.fixture
def mcp_gateway() -> MCPGateway:
    """MCP 网关 fixture"""
    gateway = MCPGateway()
    gateway.setup_gaia_tools()
    gateway.setup_skill_tools()
    return gateway
