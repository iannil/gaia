"""
GAIA Workflow - Workflow Orchestration

GAIA 工作流编排系统。

提供:
- DSL: 工作流定义语言
- Executor: 工作流执行器
- Triggers: 触发器管理
"""

from .dsl import (
    StepStatus,
    TriggerType,
    Step,
    Trigger,
    Workflow,
    WorkflowParser,
    WorkflowBuilder,
    Actions,
)
from .executor import (
    StepResult,
    WorkflowExecution,
    WorkflowExecutor,
)

__version__ = "0.1.0"

__all__ = [
    # DSL
    "StepStatus",
    "TriggerType",
    "Step",
    "Trigger",
    "Workflow",
    "WorkflowParser",
    "WorkflowBuilder",
    "Actions",
    # Executor
    "StepResult",
    "WorkflowExecution",
    "WorkflowExecutor",
]
