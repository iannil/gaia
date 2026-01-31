"""
Type stubs for gaia_core
"""

from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass

class Phase(str):
    """GAIA Phase enum"""
    GENERATE: "G"
    ANALYZE: "A"
    IMPLEMENT: "I"
    ACCEPTANCE: "A2"

    def __str__(self) -> str: ...
    @property
    def label(self) -> str: ...
    @property
    def mindset(self) -> str: ...
    @classmethod
    def flow(cls) -> List["Phase"]: ...

class PhaseStatus(str):
    """Phase status enum"""
    PENDING: "pending"
    IN_PROGRESS: "in_progress"
    COMPLETED: "completed"
    FAILED: "failed"
    SKIPPED: "skipped"

class Priority(str):
    """Task priority enum"""
    P0: "P0"
    P1: "P1"
    P2: "P2"

class GeneratePath(str):
    """Generate path enum"""
    MARKET_FIRST: "search-skill"
    GITHUB_FIRST: "skill-from-github"
    MASTERS_FIRST: "skill-from-masters"

class Task:
    """Task model"""
    id: str
    title: str
    description: Optional[str]
    priority: Priority
    phase: Optional[Phase]
    status: PhaseStatus
    dependencies: List[str]
    completed_at: Optional[datetime]
    metadata: Dict[str, Any]

class GAIAState:
    """GAIA execution state"""
    project_id: str
    project_name: str
    created_at: datetime
    updated_at: datetime
    current_phase: Phase
    phase_status: PhaseStatus
    phase_states: Dict[Phase, PhaseStatus]
    generate_path: Optional[GeneratePath]
    problem_statement: Optional[str]
    solution_outline: Optional[str]
    tasks: List[Task]
    mvp_definition: Optional[str]
    used_skills: List[str]
    implementation_notes: List[str]
    acceptance_criteria: List[str]
    acceptance_results: Dict[str, bool]
    retrospective_notes: Optional[str]
    evolution_data: Dict[str, Any]
    context: Dict[str, Any]

    def transition_to(self, phase: Phase) -> bool: ...
    def mark_phase_completed(self, phase: Phase) -> None: ...
    def mark_phase_failed(self, phase: Phase, reason: str) -> None: ...
    def add_task(self, title: str, priority: Priority, **kwargs) -> Task: ...
    def get_tasks_by_priority(self, priority: Priority) -> List[Task]: ...
    def update_context(self, key: str, value: Any) -> None: ...
    def to_dict(self) -> Dict[str, Any]: ...

class StateStore:
    """State storage interface"""
    def __init__(self, base_path: Optional[Path]) -> None: ...
    def save(self, state: GAIAState) -> None: ...
    def load(self, project_id: str) -> Optional[GAIAState]: ...
    def exists(self) -> bool: ...

class PhaseExecutor:
    """Phase executor base class"""
    phase: Phase
    state: GAIAState
    outputs: Dict[str, Any]

    def validate_preconditions(self) -> Tuple[bool, Optional[str]]: ...
    def execute(self) -> None: ...
    def validate_outputs(self) -> Tuple[bool, Optional[str]]: ...
    def run(self) -> Tuple[bool, Optional[str]]: ...

class GeneratePhase(PhaseExecutor):
    """Phase G: Generate"""
    phase: Phase

class AnalyzePhase(PhaseExecutor):
    """Phase A: Analyze"""
    phase: Phase

class ImplementPhase(PhaseExecutor):
    """Phase I: Implement"""
    phase: Phase

class AcceptancePhase(PhaseExecutor):
    """Phase A2: Acceptance"""
    phase: Phase

class PhaseFactory:
    """Phase factory"""
    @classmethod
    def create(cls, phase: Phase, state: GAIAState) -> PhaseExecutor: ...
    @classmethod
    def create_current(cls, state: GAIAState) -> PhaseExecutor: ...

class GAIAEngine:
    """GAIA execution engine"""
    project_name: str
    base_path: Path
    state: GAIAState

    def __init__(self, project_name: str, base_path: Optional[Path] = None) -> None: ...

    @property
    def current_phase(self) -> Phase: ...
    @property
    def is_complete(self) -> bool: ...

    def save(self) -> None: ...

    def start_generate(
        self,
        problem_statement: str,
        path: GeneratePath = ...
    ) -> Tuple[bool, Optional[str]]: ...
    def set_solution_outline(self, outline: str) -> None: ...

    def start_analyze(
        self,
        mvp_definition: Optional[str] = None
    ) -> Tuple[bool, Optional[str]]: ...
    def add_task(
        self,
        title: str,
        priority: Priority = ...,
        description: Optional[str] = None
    ) -> None: ...
    def set_mvp_definition(self, definition: str) -> None: ...

    def start_implement(self) -> Tuple[bool, Optional[str]]: ...
    def mark_task_completed(self, task_id: str) -> bool: ...
    def record_skill_usage(self, skill_name: str) -> None: ...
    def add_implementation_note(self, note: str) -> None: ...

    def start_acceptance(
        self,
        acceptance_criteria: Optional[List[str]] = None
    ) -> Tuple[bool, Optional[str]]: ...
    def verify_criterion(self, criterion: str, passed: bool) -> None: ...
    def set_retrospective(self, notes: str) -> None: ...

    def advance_phase(self) -> Tuple[bool, Optional[str]]: ...
    def get_status(self) -> Dict[str, Any]: ...

    def record_evolution(self, key: str, value: Any) -> None: ...
    def get_evolution_data(self) -> Dict[str, Any]: ...
    def export_evolution(self, path: Optional[Path] = None) -> Path: ...

__all__ = [
    "Phase",
    "PhaseStatus",
    "Priority",
    "GeneratePath",
    "Task",
    "GAIAState",
    "StateStore",
    "PhaseExecutor",
    "GeneratePhase",
    "AnalyzePhase",
    "ImplementPhase",
    "AcceptancePhase",
    "PhaseFactory",
    "GAIAEngine",
]
