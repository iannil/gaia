"""
Type stubs for gaia_workflow
"""

from typing import Optional, Dict, Any, List, Callable, Awaitable
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

class TriggerType(str, Enum):
    """Workflow trigger types"""
    MANUAL: "manual"
    SCHEDULE: "schedule"
    WEBHOOK: "webhook"
    EVENT: "event"

class StepStatus(str, Enum):
    """Step execution status"""
    PENDING: "pending"
    RUNNING: "running"
    COMPLETED: "completed"
    FAILED: "failed"
    SKIPPED: "skipped"

class ExecutionStatus(str, Enum):
    """Workflow execution status"""
    PENDING: "pending"
    RUNNING: "running"
    COMPLETED: "completed"
    FAILED: "failed"
    CANCELLED: "cancelled"

class Trigger:
    """Workflow trigger"""
    type: TriggerType
    config: Dict[str, Any]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Trigger": ...
    def to_dict(self) -> Dict[str, Any]: ...

class Step:
    """Workflow step"""
    id: str
    name: Optional[str]
    action: str
    parameters: Dict[str, Any]
    depends_on: Optional[List[str]]
    condition: Optional[str]
    continue_on_error: bool
    timeout: Optional[int]
    retry: Optional[Dict[str, Any]]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Step": ...
    def to_dict(self) -> Dict[str, Any]: ...
    def is_ready(self, completed: set) -> bool: ...

class Workflow:
    """Workflow definition"""
    id: str
    name: str
    description: Optional[str]
    version: str
    variables: Dict[str, Any]
    on_error: Optional[str]
    triggers: List[Trigger]
    steps: List[Step]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Workflow": ...
    def to_dict(self) -> Dict[str, Any]: ...

    def get_step(self, step_id: str) -> Optional[Step]: ...
    def get_start_steps(self) -> List[Step]: ...
    def get_ready_steps(self, completed: set) -> List[Step]: ...
    def validate(self) -> List[str]: ...

class WorkflowParser:
    """Workflow DSL parser"""
    def parse(self, content: str) -> Workflow: ...
    def parse_file(self, path: str) -> Workflow: ...
    def validate(self, workflow: Workflow) -> List[str]: ...

class WorkflowBuilder:
    """Workflow builder"""
    def __init__(self, workflow_id: str, name: str) -> None: ...
    def description(self, desc: str) -> "WorkflowBuilder": ...
    def variable(self, name: str, value: Any) -> "WorkflowBuilder": ...
    def trigger(self, trigger_type: TriggerType, config: Dict[str, Any]) -> "WorkflowBuilder": ...
    def step(
        self,
        step_id: str,
        action: str,
        name: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
        depends_on: Optional[List[str]] = None,
        condition: Optional[str] = None,
        continue_on_error: bool = False
    ) -> "WorkflowBuilder": ...
    def build(self) -> Workflow: ...

class StepResult:
    """Step execution result"""
    step_id: str
    status: StepStatus
    output: Optional[Any]
    error: Optional[str]
    started_at: datetime
    completed_at: Optional[datetime]

    @property
    def success(self) -> bool: ...
    @property
    def duration(self) -> Optional[float]: ...

class WorkflowExecution:
    """Workflow execution context"""
    workflow: Workflow
    status: ExecutionStatus
    variables: Dict[str, Any]
    step_results: Dict[str, StepResult]
    started_at: datetime
    completed_at: Optional[datetime]
    error: Optional[str]

    @property
    def is_complete(self) -> bool: ...
    @property
    def duration(self) -> Optional[float]: ...

class ActionRegistry:
    """Registry of workflow actions"""
    _actions: Dict[str, Callable]

    @classmethod
    def register(cls, name: str, handler: Callable) -> None: ...
    @classmethod
    def get(cls, name: str) -> Optional[Callable]: ...
    @classmethod
    def list_actions(cls) -> List[str]: ...

class WorkflowExecutor:
    """Workflow executor"""
    def __init__(
        self,
        actions: Optional[Dict[str, Callable]] = None,
        max_parallel: int = ...
    ) -> None: ...

    async def execute(
        self,
        workflow: Workflow,
        variables: Optional[Dict[str, Any]] = None
    ) -> WorkflowExecution: ...
    def cancel(self, execution: WorkflowExecution) -> None: ...

__all__ = [
    "TriggerType",
    "StepStatus",
    "ExecutionStatus",
    "Trigger",
    "Step",
    "Workflow",
    "WorkflowParser",
    "WorkflowBuilder",
    "StepResult",
    "WorkflowExecution",
    "ActionRegistry",
    "WorkflowExecutor",
]
