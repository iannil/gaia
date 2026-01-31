"""
GAIA Core - Phase Interfaces

定义 GAIA 四阶段的接口和基础实现。
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from ..state import GAIAState, Phase, PhaseStatus, GeneratePath, Priority, Task


class PhaseExecutor(ABC):
    """阶段执行器基类"""

    phase: Phase

    def __init__(self, state: GAIAState):
        self.state = state
        self.outputs: Dict[str, Any] = {}

    @abstractmethod
    def validate_preconditions(self) -> tuple[bool, Optional[str]]:
        """验证前置条件"""
        pass

    @abstractmethod
    def execute(self) -> None:
        """执行阶段逻辑"""
        pass

    @abstractmethod
    def validate_outputs(self) -> tuple[bool, Optional[str]]:
        """验证输出"""
        pass

    def run(self) -> tuple[bool, Optional[str]]:
        """运行阶段"""
        # 验证前置条件
        valid, error = self.validate_preconditions()
        if not valid:
            return False, f"前置条件不满足: {error}"

        # 标记为进行中
        self.state.phase_status = PhaseStatus.IN_PROGRESS

        try:
            # 执行
            self.execute()

            # 验证输出
            valid, error = self.validate_outputs()
            if not valid:
                return False, f"输出验证失败: {error}"

            # 标记完成
            self.state.mark_phase_completed(self.phase)
            return True, None

        except Exception as e:
            self.state.mark_phase_failed(self.phase, str(e))
            return False, f"执行失败: {e}"


class GeneratePhase(PhaseExecutor):
    """Phase G: 生成 - 专家思维"""

    phase = Phase.GENERATE

    def validate_preconditions(self) -> tuple[bool, Optional[str]]:
        """验证前置条件"""
        if not self.state.problem_statement:
            return False, "缺少问题陈述 (problem_statement)"
        return True, None

    def execute(self) -> None:
        """执行生成阶段"""
        path = self.state.generate_path or GeneratePath.MARKET_FIRST

        if path == GeneratePath.MARKET_FIRST:
            self._execute_market_first()
        elif path == GeneratePath.GITHUB_FIRST:
            self._execute_github_first()
        elif path == GeneratePath.MASTERS_FIRST:
            self._execute_masters_first()

        # 记录到上下文
        self.state.update_context("generate_path", path)

    def _execute_market_first(self) -> None:
        """市场优先路径：搜索现有 Skills"""
        self.outputs["search_queries"] = self._generate_search_queries()
        self.outputs["sources"] = ["anthropics/skills", "ComposioHQ", "skills.sh"]

    def _execute_github_first(self) -> None:
        """GitHub 优先路径：从仓库学习"""
        self.outputs["github_repos"] = []
        self.outputs["learning_points"] = []

    def _execute_masters_first(self) -> None:
        """方法论优先路径：综合专家理论"""
        self.outputs["expert_sources"] = []
        self.outputs["best_practices"] = []

    def _generate_search_queries(self) -> List[str]:
        """生成搜索查询"""
        problem = self.state.problem_statement or ""
        # 简单的关键词提取
        keywords = problem.split()[:5]
        return [f"{' '.join(keywords)} skill", f"{' '.join(keywords)} tool"]

    def validate_outputs(self) -> tuple[bool, Optional[str]]:
        """验证输出"""
        if not self.state.solution_outline:
            return False, "缺少解决方案大纲 (solution_outline)"
        return True, None


class AnalyzePhase(PhaseExecutor):
    """Phase A: 分析 - 架构师思维"""

    phase = Phase.ANALYZE

    def validate_preconditions(self) -> tuple[bool, Optional[str]]:
        """验证前置条件"""
        if self.state.phase_states[Phase.GENERATE] != PhaseStatus.COMPLETED:
            return False, "Phase G 尚未完成"
        if not self.state.solution_outline:
            return False, "缺少解决方案大纲"
        return True, None

    def execute(self) -> None:
        """执行分析阶段"""
        # 定义 MVP
        if not self.state.mvp_definition:
            self.state.mvp_definition = self._define_mvp()

        # 分解任务
        tasks = self._decompose_tasks()
        for task in tasks:
            self.state.add_task(**task)

        # 记录到上下文
        self.state.update_context("analyze_completed", True)

    def _define_mvp(self) -> str:
        """定义 MVP"""
        return """MVP 定义:

P0 (核心 - 必须完成):
- 核心功能 1
- 核心功能 2

P1 (重要 - 应该完成):
- 重要功能 1

P2 (可选 - 有时间再做):
- 锦上添花的功能
"""

    def _decompose_tasks(self) -> List[Dict[str, Any]]:
        """分解任务"""
        return [
            {"title": "任务 1", "priority": Priority.P0},
            {"title": "任务 2", "priority": Priority.P0},
        ]

    def validate_outputs(self) -> tuple[bool, Optional[str]]:
        """验证输出"""
        if not self.state.tasks:
            return False, "缺少任务分解"
        return True, None


class ImplementPhase(PhaseExecutor):
    """Phase I: 实现 - 工匠思维"""

    phase = Phase.IMPLEMENT

    def validate_preconditions(self) -> tuple[bool, Optional[str]]:
        """验证前置条件"""
        if self.state.phase_states[Phase.ANALYZE] != PhaseStatus.COMPLETED:
            return False, "Phase A (分析) 尚未完成"
        if not self.state.tasks:
            return False, "缺少任务定义"
        return True, None

    def execute(self) -> None:
        """执行实现阶段"""
        # 获取 P0 任务
        p0_tasks = self.state.get_tasks_by_priority(Priority.P0)

        for task in p0_tasks:
            if task.status != PhaseStatus.COMPLETED:
                # 标记为进行中
                task.status = PhaseStatus.IN_PROGRESS
                # 这里实际会调用具体的实现逻辑
                # task.status = PhaseStatus.COMPLETED

        # 记录使用的 Skills
        self.state.update_context("implementation_started", True)

    def validate_outputs(self) -> tuple[bool, Optional[str]]:
        """验证输出"""
        p0_tasks = self.state.get_tasks_by_priority(Priority.P0)
        incomplete = [t for t in p0_tasks if t.status != PhaseStatus.COMPLETED]
        if incomplete:
            return False, f"存在未完成的 P0 任务: {[t.title for t in incomplete]}"
        return True, None


class AcceptancePhase(PhaseExecutor):
    """Phase A: 验收 - 质检员思维"""

    phase = Phase.ACCEPTANCE

    def validate_preconditions(self) -> tuple[bool, Optional[str]]:
        """验证前置条件"""
        if self.state.phase_states[Phase.IMPLEMENT] != PhaseStatus.COMPLETED:
            return False, "Phase I (实现) 尚未完成"
        return True, None

    def execute(self) -> None:
        """执行验收阶段"""
        # 根据 MVP 定义验收
        if self.state.acceptance_criteria:
            for criterion in self.state.acceptance_criteria:
                # 默认通过，实际需要检查
                self.state.acceptance_results[criterion] = True

        # 记录复盘
        self.state.update_context("acceptance_completed", True)

    def validate_outputs(self) -> tuple[bool, Optional[str]]:
        """验证输出"""
        if not self.state.acceptance_results:
            return False, "缺少验收结果"
        failed = [c for c, passed in self.state.acceptance_results.items() if not passed]
        if failed:
            return False, f"以下验收项未通过: {failed}"
        return True, None


class PhaseFactory:
    """阶段工厂"""

    _executors: Dict[Phase, type[PhaseExecutor]] = {
        Phase.GENERATE: GeneratePhase,
        Phase.ANALYZE: AnalyzePhase,
        Phase.IMPLEMENT: ImplementPhase,
        Phase.ACCEPTANCE: AcceptancePhase,
    }

    @classmethod
    def create(cls, phase: Phase, state: GAIAState) -> PhaseExecutor:
        """创建阶段执行器"""
        executor_class = cls._executors.get(phase)
        if not executor_class:
            raise ValueError(f"未知的阶段: {phase}")
        return executor_class(state)

    @classmethod
    def create_current(cls, state: GAIAState) -> PhaseExecutor:
        """创建当前阶段执行器"""
        return cls.create(state.current_phase, state)


__all__ = [
    "PhaseExecutor",
    "GeneratePhase",
    "AnalyzePhase",
    "ImplementPhase",
    "AcceptancePhase",
    "PhaseFactory",
]
