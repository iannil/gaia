"""
GAIA Core - Execution Engine

GAIA 执行框架的核心引擎模块。

提供:
- State: 状态管理和数据模型
- Phases: 四阶段执行器
- Engine: 流程编排引擎
"""

from .state import (
    Phase,
    PhaseStatus,
    Priority,
    GeneratePath,
    Task,
    GAIAState,
    StateStore,
)
from .phases import (
    PhaseExecutor,
    GeneratePhase,
    AnalyzePhase,
    ImplementPhase,
    AcceptancePhase,
    PhaseFactory,
)
from .engine import GAIAEngine

__version__ = "0.1.0"

__all__ = [
    # State
    "Phase",
    "PhaseStatus",
    "Priority",
    "GeneratePath",
    "Task",
    "GAIAState",
    "StateStore",
    # Phases
    "PhaseExecutor",
    "GeneratePhase",
    "AnalyzePhase",
    "ImplementPhase",
    "AcceptancePhase",
    "PhaseFactory",
    # Engine
    "GAIAEngine",
]
