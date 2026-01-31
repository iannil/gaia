"""
GAIA Workflow - Executor

工作流执行器，负责执行定义好的工作流。
"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
import asyncio
import subprocess
import json

from ..dsl import Workflow, Step, StepStatus, Trigger, TriggerType


@dataclass
class StepResult:
    """步骤执行结果"""
    step_id: str
    status: StepStatus
    output: Any = None
    error: Optional[str] = None
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None
    duration: float = 0.0  # 执行时长（秒）

    def to_dict(self) -> Dict[str, Any]:
        return {
            "step_id": self.step_id,
            "status": self.status.value,
            "output": self.output,
            "error": self.error,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "duration": self.duration,
        }


@dataclass
class WorkflowExecution:
    """工作流执行记录"""
    workflow_id: str
    workflow_name: str
    execution_id: str
    status: StepStatus = StepStatus.PENDING
    results: Dict[str, StepResult] = field(default_factory=dict)
    variables: Dict[str, Any] = field(default_factory=dict)
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None
    triggered_by: str = "manual"  # 触发方式

    def to_dict(self) -> Dict[str, Any]:
        return {
            "workflow_id": self.workflow_id,
            "workflow_name": self.workflow_name,
            "execution_id": self.execution_id,
            "status": self.status.value,
            "results": {k: v.to_dict() for k, v in self.results.items()},
            "variables": self.variables,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "triggered_by": self.triggered_by,
        }


class ActionHandler:
    """动作处理器基类"""

    async def execute(self, step: Step, context: Dict[str, Any]) -> Any:
        """执行动作"""
        raise NotImplementedError

    @staticmethod
    def substitute_vars(text: str, variables: Dict[str, Any]) -> str:
        """替换变量"""
        for key, value in variables.items():
            text = text.replace(f"${key}", str(value))
        return text


class GAIAActionHandler(ActionHandler):
    """GAIA 相关动作处理器"""

    def __init__(self):
        # 延迟导入，避免循环依赖
        self._engine = None
        self._skill_manager = None

    def _get_engine(self):
        if self._engine is None:
            from gaia_core import GAIAEngine
            project = self._variables.get("project", "default")
            self._engine = GAIAEngine(project)
        return self._engine

    def _get_skill_manager(self):
        if self._skill_manager is None:
            from gaia_skills import SkillManager
            self._skill_manager = SkillManager()
        return self._skill_manager

    async def execute(self, step: Step, context: Dict[str, Any]) -> Any:
        action = step.action
        params = step.parameters

        # 替换变量
        for key, value in params.items():
            if isinstance(value, str):
                params[key] = self.substitute_vars(value, context.get("variables", {}))

        if action == "gaia.phase.generate":
            engine = self._get_engine()
            success, error = engine.start_generate(
                params.get("problem", ""),
                params.get("path", "market"),
            )
            return {"success": success, "error": error}

        elif action == "gaia.phase.analyze":
            engine = self._get_engine()
            success, error = engine.start_analyze(params.get("mvp"))
            return {"success": success, "error": error}

        elif action == "gaia.phase.implement":
            engine = self._get_engine()
            success, error = engine.start_implement()
            return {"success": success, "error": error}

        elif action == "gaia.phase.acceptance":
            engine = self._get_engine()
            success, error = engine.start_acceptance(params.get("criteria"))
            return {"success": success, "error": error}

        elif action == "gaia.phase.advance":
            engine = self._get_engine()
            success, error = engine.advance_phase()
            return {"success": success, "error": error, "current_phase": str(engine.current_phase)}

        elif action == "gaia.skill.install":
            manager = self._get_skill_manager()
            success, message = manager.install_from_github(params.get("repo"))
            return {"success": success, "message": message}

        elif action == "gaia.evolve.record":
            engine = self._get_engine()
            engine.record_evolution(params.get("key"), params.get("value"))
            return {"success": True}

        elif action == "gaia.evolve.export":
            engine = self._get_engine()
            path = engine.export_evolution()
            return {"success": True, "path": str(path)}

        else:
            return {"success": False, "error": f"未知动作: {action}"}


class ShellActionHandler(ActionHandler):
    """Shell 命令处理器"""

    async def execute(self, step: Step, context: Dict[str, Any]) -> Any:
        if step.action == "shell":
            cmd = step.parameters.get("command", "")
            cmd = self.substitute_vars(cmd, context.get("variables", {}))

            try:
                result = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=step.parameters.get("timeout", 300),
                )
                return {
                    "success": result.returncode == 0,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "returncode": result.returncode,
                }
            except subprocess.TimeoutExpired:
                return {"success": False, "error": "命令执行超时"}
            except Exception as e:
                return {"success": False, "error": str(e)}

        elif step.action == "echo":
            message = step.parameters.get("message", "")
            message = self.substitute_vars(message, context.get("variables", {}))
            print(message)
            return {"success": True, "message": message}

        return {"success": False, "error": f"未知动作: {action}"}


class WorkflowExecutor:
    """工作流执行器

    负责执行工作流定义。
    """

    def __init__(self):
        self._handlers: Dict[str, ActionHandler] = {}
        self._register_default_handlers()

    def _register_default_handlers(self) -> None:
        """注册默认动作处理器"""
        self.register_handler("gaia.", GAIAActionHandler())
        self.register_handler("shell", ShellActionHandler())
        self.register_handler("echo", ShellActionHandler())

    def register_handler(self, prefix: str, handler: ActionHandler) -> None:
        """注册动作处理器"""
        self._handlers[prefix] = handler

    def _get_handler(self, action: str) -> Optional[ActionHandler]:
        """获取动作处理器"""
        # 精确匹配
        if action in self._handlers:
            return self._handlers[action]

        # 前缀匹配
        for prefix, handler in self._handlers.items():
            if action.startswith(prefix):
                return handler

        return None

    async def execute(
        self,
        workflow: Workflow,
        variables: Optional[Dict[str, Any]] = None,
        triggered_by: str = "manual",
    ) -> WorkflowExecution:
        """执行工作流"""
        import uuid
        execution_id = str(uuid.uuid4())

        execution = WorkflowExecution(
            workflow_id=workflow.id,
            workflow_name=workflow.name,
            execution_id=execution_id,
            variables=variables or {},
            triggered_by=triggered_by,
        )

        # 合并全局变量
        all_vars = {**workflow.variables, **execution.variables}

        execution.status = StepStatus.RUNNING

        try:
            completed = set()

            while True:
                # 获取可执行的步骤
                ready = workflow.get_ready_steps(completed)

                if not ready:
                    break

                # 并行执行无依赖的步骤
                tasks = [
                    self._execute_step(step, all_vars, execution)
                    for step in ready
                ]

                results = await asyncio.gather(*tasks, return_exceptions=True)

                for result in results:
                    if isinstance(result, Exception):
                        # 处理异常
                        continue
                    if result.status == StepStatus.COMPLETED:
                        completed.add(result.step_id)

            # 检查是否所有步骤都完成
            if len(completed) == len(workflow.steps):
                execution.status = StepStatus.COMPLETED
            else:
                execution.status = StepStatus.FAILED

        except Exception as e:
            execution.status = StepStatus.FAILED

        finally:
            execution.completed_at = datetime.now().isoformat()

        return execution

    async def _execute_step(
        self,
        step: Step,
        variables: Dict[str, Any],
        execution: WorkflowExecution,
    ) -> StepResult:
        """执行单个步骤"""
        import time
        start_time = time.time()

        result = StepResult(
            step_id=step.id,
            status=StepStatus.RUNNING,
        )

        # 检查条件
        if step.condition:
            if not self._evaluate_condition(step.condition, variables):
                result.status = StepStatus.SKIPPED
                execution.results[step.id] = result
                return result

        try:
            # 获取处理器
            handler = self._get_handler(step.action)

            if handler:
                output = await handler.execute(step, {"variables": variables})
                result.output = output
                result.status = StepStatus.COMPLETED

                # 更新变量
                if isinstance(output, dict) and "variables" in output:
                    variables.update(output["variables"])
            else:
                result.status = StepStatus.FAILED
                result.error = f"未找到处理器: {step.action}"

        except Exception as e:
            result.status = StepStatus.FAILED
            result.error = str(e)

            if not step.continue_on_error:
                raise

        finally:
            result.duration = time.time() - start_time
            result.completed_at = datetime.now().isoformat()
            execution.results[step.id] = result

        return result

    def _evaluate_condition(self, condition: str, variables: Dict[str, Any]) -> bool:
        """评估条件表达式"""
        # 简单实现：支持变量存在性检查
        condition = condition.strip()

        # $var exists 类型
        if " exists" in condition:
            var_name = condition.replace(" exists", "").strip().replace("$", "")
            return var_name in variables

        # 简单的相等检查
        if "==" in condition:
            parts = condition.split("==", 1)
            left = parts[0].strip().replace("$", "")
            right = parts[1].strip().strip('"\'')
            return str(variables.get(left, "")) == right

        return True

    def execute_sync(
        self,
        workflow: Workflow,
        variables: Optional[Dict[str, Any]] = None,
    ) -> WorkflowExecution:
        """同步执行工作流"""
        return asyncio.run(self.execute(workflow, variables))


__all__ = [
    "StepResult",
    "WorkflowExecution",
    "ActionHandler",
    "GAIAActionHandler",
    "ShellActionHandler",
    "WorkflowExecutor",
]
