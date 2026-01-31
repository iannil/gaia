"""
GAIA Core - State Management

状态管理模块，定义 GAIA 框架的核心数据结构和状态模型。
"""

from enum import Enum
from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from pathlib import Path


class Phase(str, Enum):
    """GAIA 四阶段枚举"""

    GENERATE = "G"  # 生成 - 专家思维
    ANALYZE = "A"  # 分析 - 架构师思维
    IMPLEMENT = "I"  # 实现 - 工匠思维
    ACCEPTANCE = "A2"  # 验收 - 质检员思维 (A2 与 A 区分)

    def __str__(self) -> str:
        return self.value

    @property
    def label(self) -> str:
        """阶段显示名称"""
        labels = {
            Phase.GENERATE: "生成",
            Phase.ANALYZE: "分析",
            Phase.IMPLEMENT: "实现",
            Phase.ACCEPTANCE: "验收",
        }
        return labels[self]

    @property
    def mindset(self) -> str:
        """阶段思维模式"""
        mindsets = {
            Phase.GENERATE: "专家思维 - 定义'做什么'与'怎么做'",
            Phase.ANALYZE: "架构师思维 - 分解与规划",
            Phase.IMPLEMENT: "工匠思维 - 构建与记录",
            Phase.ACCEPTANCE: "质检员思维 - 验证与复盘",
        }
        return mindsets[self]

    @classmethod
    def flow(cls) -> List["Phase"]:
        """获取标准执行流程"""
        return [cls.GENERATE, cls.ANALYZE, cls.IMPLEMENT, cls.ACCEPTANCE]


class PhaseStatus(str, Enum):
    """阶段状态"""

    PENDING = "pending"  # 待开始
    IN_PROGRESS = "in_progress"  # 进行中
    COMPLETED = "completed"  # 已完成
    FAILED = "failed"  # 失败
    SKIPPED = "skipped"  # 跳过


class Priority(str, Enum):
    """任务优先级"""

    P0 = "P0"  # 核心 - 必须完成
    P1 = "P1"  # 重要 - 应该完成
    P2 = "P2"  # 可选 - 有时间再做


class GeneratePath(str, Enum):
    """Phase G 的三条路径"""

    MARKET_FIRST = "search-skill"  # 市场优先 - 搜索现成 Skills
    GITHUB_FIRST = "skill-from-github"  # 原理优先 - 从 GitHub 学习
    MASTERS_FIRST = "skill-from-masters"  # 方法论优先 - 综合专家理论


class Task(BaseModel):
    """任务模型"""

    model_config = ConfigDict(extra="allow")

    id: str
    title: str
    description: Optional[str] = None
    priority: Priority = Priority.P2
    phase: Optional[Phase] = None
    status: PhaseStatus = PhaseStatus.PENDING
    dependencies: List[str] = Field(default_factory=list)
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class GAIAState(BaseModel):
    """GAIA 执行状态"""

    model_config = ConfigDict(extra="allow")

    # 基本信息
    project_id: str
    project_name: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # 当前状态
    current_phase: Phase = Phase.GENERATE
    phase_status: PhaseStatus = PhaseStatus.PENDING

    # 各阶段状态
    phase_states: Dict[Phase, PhaseStatus] = Field(
        default_factory=lambda: {
            Phase.GENERATE: PhaseStatus.PENDING,
            Phase.ANALYZE: PhaseStatus.PENDING,
            Phase.IMPLEMENT: PhaseStatus.PENDING,
            Phase.ACCEPTANCE: PhaseStatus.PENDING,
        }
    )

    # Phase G: 生成
    generate_path: Optional[GeneratePath] = None
    problem_statement: Optional[str] = None
    solution_outline: Optional[str] = None

    # Phase A: 分析
    tasks: List[Task] = Field(default_factory=list)
    mvp_definition: Optional[str] = None

    # Phase I: 实现
    used_skills: List[str] = Field(default_factory=list)
    implementation_notes: List[str] = Field(default_factory=list)

    # Phase A: 验收
    acceptance_criteria: List[str] = Field(default_factory=list)
    acceptance_results: Dict[str, bool] = Field(default_factory=dict)
    retrospective_notes: Optional[str] = None

    # 演化记录
    evolution_data: Dict[str, Any] = Field(default_factory=dict)

    # 上下文传递
    context: Dict[str, Any] = Field(default_factory=dict)

    def transition_to(self, phase: Phase) -> bool:
        """转换到指定阶段"""
        current_idx = Phase.flow().index(self.current_phase)
        target_idx = Phase.flow().index(phase)

        if target_idx < current_idx:
            return False  # 不能回退

        self.current_phase = phase
        self.phase_status = PhaseStatus.PENDING
        self.updated_at = datetime.now()
        return True

    def mark_phase_completed(self, phase: Phase) -> None:
        """标记阶段完成"""
        self.phase_states[phase] = PhaseStatus.COMPLETED
        self.updated_at = datetime.now()

    def mark_phase_failed(self, phase: Phase, reason: str) -> None:
        """标记阶段失败"""
        self.phase_states[phase] = PhaseStatus.FAILED
        self.context[f"{phase.value}_failure_reason"] = reason
        self.updated_at = datetime.now()

    def add_task(self, title: str, priority: Priority = Priority.P2, **kwargs) -> Task:
        """添加任务"""
        task = Task(
            id=f"task_{len(self.tasks) + 1}",
            title=title,
            priority=priority,
            **kwargs,
        )
        self.tasks.append(task)
        self.updated_at = datetime.now()
        return task

    def get_tasks_by_priority(self, priority: Priority) -> List[Task]:
        """按优先级获取任务"""
        return [t for t in self.tasks if t.priority == priority]

    def update_context(self, key: str, value: Any) -> None:
        """更新上下文"""
        self.context[key] = value
        self.updated_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return self.model_dump()


class StateStore:
    """状态存储接口"""

    def __init__(self, base_path: Optional[Path] = None):
        self.base_path = base_path or Path.cwd() / ".gaia"
        self.base_path.mkdir(parents=True, exist_ok=True)

    def save(self, state: GAIAState) -> None:
        """保存状态"""
        state_file = self.base_path / "state.json"
        import json

        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(state.to_dict(), f, indent=2, default=str)

    def load(self, project_id: str) -> Optional[GAIAState]:
        """加载状态"""
        state_file = self.base_path / "state.json"
        if not state_file.exists():
            return None

        import json

        with open(state_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            # 转换字符串枚举回枚举类型
            if "current_phase" in data and isinstance(data["current_phase"], str):
                data["current_phase"] = Phase(data["current_phase"])
            if "phase_status" in data and isinstance(data["phase_status"], str):
                data["phase_status"] = PhaseStatus(data["phase_status"])
            if "generate_path" in data and data["generate_path"] is not None and isinstance(data["generate_path"], str):
                data["generate_path"] = GeneratePath(data["generate_path"])
            # 转换 phase_states 的键和值
            if "phase_states" in data:
                new_phase_states = {}
                for phase_str, status_str in data["phase_states"].items():
                    if isinstance(phase_str, str) and isinstance(status_str, str):
                        new_phase_states[Phase(phase_str)] = PhaseStatus(status_str)
                    else:
                        new_phase_states[phase_str] = status_str
                data["phase_states"] = new_phase_states
            # 转换 tasks 中的枚举
            if "tasks" in data:
                for task in data["tasks"]:
                    if "phase" in task and task["phase"] is not None and isinstance(task["phase"], str):
                        task["phase"] = Phase(task["phase"])
                    if "status" in task and isinstance(task["status"], str):
                        task["status"] = PhaseStatus(task["status"])
                    if "priority" in task and isinstance(task["priority"], str):
                        task["priority"] = Priority(task["priority"])
            return GAIAState(**data)

    def exists(self) -> bool:
        """检查是否存在状态"""
        return (self.base_path / "state.json").exists()


__all__ = [
    "Phase",
    "PhaseStatus",
    "Priority",
    "GeneratePath",
    "Task",
    "GAIAState",
    "StateStore",
]
