"""
GAIA Workflow - DSL

工作流 DSL 定义和解析器。
"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import re
import yaml


class StepStatus(str, Enum):
    """步骤状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class TriggerType(str, Enum):
    """触发器类型"""
    MANUAL = "manual"  # 手动触发
    SCHEDULE = "schedule"  # 定时触发
    EVENT = "event"  # 事件触发
    WEBHOOK = "webhook"  # Webhook 触发


@dataclass
class Step:
    """工作流步骤"""
    id: str
    name: str
    action: str  # 要执行的动作
    parameters: Dict[str, Any] = field(default_factory=dict)
    condition: Optional[str] = None  # 执行条件
    continue_on_error: bool = False
    depends_on: List[str] = field(default_factory=list)  # 依赖的步骤 ID

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "action": self.action,
            "parameters": self.parameters,
            "condition": self.condition,
            "continue_on_error": self.continue_on_error,
            "depends_on": self.depends_on,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Step":
        return cls(
            id=data["id"],
            name=data.get("name", data["id"]),
            action=data["action"],
            parameters=data.get("parameters", {}),
            condition=data.get("condition"),
            continue_on_error=data.get("continue_on_error", False),
            depends_on=data.get("depends_on", []),
        )


@dataclass
class Trigger:
    """触发器定义"""
    type: TriggerType
    config: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type.value,
            "config": self.config,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Trigger":
        return cls(
            type=TriggerType(data["type"]),
            config=data.get("config", {}),
        )


@dataclass
class Workflow:
    """工作流定义"""
    id: str
    name: str
    description: str = ""
    version: str = "1.0"
    steps: List[Step] = field(default_factory=list)
    triggers: List[Trigger] = field(default_factory=list)
    variables: Dict[str, Any] = field(default_factory=dict)  # 全局变量
    on_error: Optional[str] = None  # 错误处理策略

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "steps": [s.to_dict() for s in self.steps],
            "triggers": [t.to_dict() for t in self.triggers],
            "variables": self.variables,
            "on_error": self.on_error,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Workflow":
        workflow = cls(
            id=data["id"],
            name=data["name"],
            description=data.get("description", ""),
            version=data.get("version", "1.0"),
            variables=data.get("variables", {}),
            on_error=data.get("on_error"),
        )

        for step_data in data.get("steps", []):
            workflow.steps.append(Step.from_dict(step_data))

        for trigger_data in data.get("triggers", []):
            workflow.triggers.append(Trigger.from_dict(trigger_data))

        return workflow

    def get_step(self, step_id: str) -> Optional[Step]:
        """获取步骤"""
        for step in self.steps:
            if step.id == step_id:
                return step
        return None

    def get_start_steps(self) -> List[Step]:
        """获取起始步骤（无依赖的步骤）"""
        return [s for s in self.steps if not s.depends_on]

    def get_ready_steps(self, completed: set) -> List[Step]:
        """获取可执行的步骤（依赖已完成的步骤）"""
        ready = []
        for step in self.steps:
            if step.id in completed:
                continue

            # 检查依赖是否都已完成
            if all(dep in completed for dep in step.depends_on):
                ready.append(step)

        return ready


class WorkflowParser:
    """工作流 DSL 解析器

    支持 YAML 格式的工作流定义。
    """

    def parse(self, content: str) -> Workflow:
        """解析 YAML 格式的工作流"""
        data = yaml.safe_load(content)
        return Workflow.from_dict(data)

    def parse_file(self, path: str) -> Workflow:
        """从文件解析工作流"""
        with open(path, "r", encoding="utf-8") as f:
            return self.parse(f.read())

    def validate(self, workflow: Workflow) -> List[str]:
        """验证工作流定义"""
        errors = []

        # 检查基本字段
        if not workflow.id:
            errors.append("缺少 workflow.id")

        if not workflow.name:
            errors.append("缺少 workflow.name")

        # 检查步骤
        step_ids = set()
        for step in workflow.steps:
            if not step.id:
                errors.append(f"步骤缺少 id: {step.name}")

            step_ids.add(step.id)

            # 检查依赖是否存在
            for dep in step.depends_on:
                if dep not in step_ids and dep not in [s.id for s in workflow.steps]:
                    errors.append(f"步骤 {step.id} 依赖了不存在的步骤: {dep}")

        # 检查循环依赖
        if self._has_circular_dependency(workflow):
            errors.append("工作流存在循环依赖")

        return errors

    def _has_circular_dependency(self, workflow: Workflow) -> bool:
        """检查是否存在循环依赖"""
        # 构建依赖图
        graph = {step.id: step.depends_on for step in workflow.steps}

        # 使用 DFS 检测环
        visited = set()
        rec_stack = set()

        def dfs(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)

            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True

            rec_stack.remove(node)
            return False

        for step_id in graph:
            if step_id not in visited:
                if dfs(step_id):
                    return True

        return False


class WorkflowBuilder:
    """工作流构建器

    提供流式 API 构建工作流。
    """

    def __init__(self, workflow_id: str, name: str):
        self._workflow = Workflow(
            id=workflow_id,
            name=name,
        )

    def description(self, desc: str) -> "WorkflowBuilder":
        """设置描述"""
        self._workflow.description = desc
        return self

    def variable(self, name: str, value: Any) -> "WorkflowBuilder":
        """添加变量"""
        self._workflow.variables[name] = value
        return self

    def trigger(self, trigger_type: TriggerType, config: Dict[str, Any]) -> "WorkflowBuilder":
        """添加触发器"""
        self._workflow.triggers.append(Trigger(type=trigger_type, config=config))
        return self

    def step(
        self,
        step_id: str,
        action: str,
        name: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
        depends_on: Optional[List[str]] = None,
        condition: Optional[str] = None,
        continue_on_error: bool = False,
    ) -> "WorkflowBuilder":
        """添加步骤"""
        step = Step(
            id=step_id,
            name=name or step_id,
            action=action,
            parameters=parameters or {},
            depends_on=depends_on or [],
            condition=condition,
            continue_on_error=continue_on_error,
        )
        self._workflow.steps.append(step)
        return self

    def build(self) -> Workflow:
        """构建工作流"""
        return self._workflow


# 预定义的动作
class Actions:
    """预定义的工作流动作"""

    # GAIA 相关
    PHASE_GENERATE = "gaia.phase.generate"
    PHASE_ANALYZE = "gaia.phase.analyze"
    PHASE_IMPLEMENT = "gaia.phase.implement"
    PHASE_ACCEPTANCE = "gaia.phase.acceptance"
    PHASE_ADVANCE = "gaia.phase.advance"

    # Skill 相关
    SKILL_INSTALL = "gaia.skill.install"
    SKILL_UPDATE = "gaia.skill.update"
    SKILL_LIST = "gaia.skill.list"

    # 演化相关
    EVOLVE_RECORD = "gaia.evolve.record"
    EVOLVE_EXPORT = "gaia.evolve.export"

    # 通用
    ECHO = "echo"
    SHELL = "shell"
    HTTP_REQUEST = "http.request"
    NOTIFY = "notify"


__all__ = [
    "StepStatus",
    "TriggerType",
    "Step",
    "Trigger",
    "Workflow",
    "WorkflowParser",
    "WorkflowBuilder",
    "Actions",
]
