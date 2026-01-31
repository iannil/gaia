"""
GAIA Core - Execution Engine

GAIA 执行引擎，协调整个 G→A→I→A 流程。
"""

from typing import Optional, List, Dict, Any
from pathlib import Path
import json

from ..state import GAIAState, Phase, PhaseStatus, GeneratePath, Priority, StateStore
from ..phases import PhaseFactory, PhaseExecutor


class GAIAEngine:
    """GAIA 执行引擎

    负责协调整个 GAIA 流程的执行。
    """

    def __init__(self, project_name: str, base_path: Optional[Path] = None):
        self.project_name = project_name
        self.base_path = base_path or Path.cwd()
        self.store = StateStore(self.base_path / ".gaia")

        # 尝试加载现有状态，或创建新状态
        existing = self.store.load(project_name)
        if existing:
            self.state = existing
        else:
            self.state = GAIAState(
                project_id=project_name.lower().replace(" ", "-"),
                project_name=project_name,
            )

    @property
    def current_phase(self) -> Phase:
        """获取当前阶段"""
        return self.state.current_phase

    @property
    def is_complete(self) -> bool:
        """检查是否完成所有阶段"""
        return all(
            status == PhaseStatus.COMPLETED
            for status in self.state.phase_states.values()
        )

    def save(self) -> None:
        """保存状态"""
        self.store.save(self.state)

    # ========== Phase G: 生成 ==========

    def start_generate(
        self,
        problem_statement: str,
        path: GeneratePath = GeneratePath.MARKET_FIRST,
    ) -> tuple[bool, Optional[str]]:
        """启动 Phase G: 生成

        Args:
            problem_statement: 问题陈述
            path: 解决方案路径 (market-first/github-first/masters-first)

        Returns:
            (成功, 错误信息)
        """
        self.state.current_phase = Phase.GENERATE
        self.state.phase_status = PhaseStatus.IN_PROGRESS
        self.state.problem_statement = problem_statement
        self.state.generate_path = path

        # 执行生成阶段的初始逻辑
        executor = PhaseFactory.create_current(self.state)
        executor.execute()

        self.save()
        return True, None

    def set_solution_outline(self, outline: str) -> None:
        """设置解决方案大纲"""
        self.state.solution_outline = outline
        self.save()

    # ========== Phase A: 分析 ==========

    def start_analyze(self, mvp_definition: Optional[str] = None) -> tuple[bool, Optional[str]]:
        """启动 Phase A: 分析

        Args:
            mvp_definition: MVP 定义

        Returns:
            (成功, 错误信息)
        """
        if not self.state.transition_to(Phase.ANALYZE):
            return False, "无法转换到分析阶段"

        if mvp_definition:
            self.state.mvp_definition = mvp_definition

        executor = PhaseFactory.create_current(self.state)
        success, error = executor.run()

        self.save()
        return success, error

    def add_task(
        self,
        title: str,
        priority: Priority = Priority.P2,
        description: Optional[str] = None,
    ) -> None:
        """添加任务"""
        self.state.add_task(title=title, priority=priority, description=description, phase=Phase.ANALYZE)
        self.save()

    def set_mvp_definition(self, definition: str) -> None:
        """设置 MVP 定义"""
        self.state.mvp_definition = definition
        self.save()

    # ========== Phase I: 实现 ==========

    def start_implement(self) -> tuple[bool, Optional[str]]:
        """启动 Phase I: 实现

        Returns:
            (成功, 错误信息)
        """
        if not self.state.transition_to(Phase.IMPLEMENT):
            return False, "无法转换到实现阶段"

        executor = PhaseFactory.create_current(self.state)
        success, error = executor.run()

        self.save()
        return success, error

    def mark_task_completed(self, task_id: str) -> bool:
        """标记任务完成"""
        for task in self.state.tasks:
            if task.id == task_id:
                task.status = PhaseStatus.COMPLETED
                self.save()
                return True
        return False

    def record_skill_usage(self, skill_name: str) -> None:
        """记录使用的 Skill"""
        if skill_name not in self.state.used_skills:
            self.state.used_skills.append(skill_name)
        self.save()

    def add_implementation_note(self, note: str) -> None:
        """添加实现笔记"""
        self.state.implementation_notes.append(note)
        self.save()

    # ========== Phase A: 验收 ==========

    def start_acceptance(
        self,
        acceptance_criteria: Optional[List[str]] = None,
    ) -> tuple[bool, Optional[str]]:
        """启动 Phase A: 验收

        Args:
            acceptance_criteria: 验收标准列表

        Returns:
            (成功, 错误信息)
        """
        if not self.state.transition_to(Phase.ACCEPTANCE):
            return False, "无法转换到验收阶段"

        if acceptance_criteria:
            self.state.acceptance_criteria = acceptance_criteria

        executor = PhaseFactory.create_current(self.state)
        success, error = executor.run()

        self.save()
        return success, error

    def verify_criterion(self, criterion: str, passed: bool) -> None:
        """验证验收标准"""
        self.state.acceptance_results[criterion] = passed
        self.save()

    def set_retrospective(self, notes: str) -> None:
        """设置复盘笔记"""
        self.state.retrospective_notes = notes
        self.save()

    # ========== 流程控制 ==========

    def advance_phase(self) -> tuple[bool, Optional[str]]:
        """推进到下一阶段"""
        flow = Phase.flow()
        current_idx = flow.index(self.state.current_phase)

        if current_idx >= len(flow) - 1:
            return False, "已经是最后一个阶段"

        # 验证当前阶段是否可以推进
        current_executor = PhaseFactory.create_current(self.state)
        valid, error = current_executor.validate_outputs()
        if not valid:
            return False, f"当前阶段未完成: {error}"

        # 标记当前阶段完成
        self.state.mark_phase_completed(self.state.current_phase)

        next_phase = flow[current_idx + 1]

        # 根据不同阶段调用对应的启动方法
        if next_phase == Phase.ANALYZE:
            return self.start_analyze()
        elif next_phase == Phase.IMPLEMENT:
            return self.start_implement()
        elif next_phase == Phase.ACCEPTANCE:
            return self.start_acceptance()

        return False, f"未知的下一阶段: {next_phase}"

    def get_status(self) -> Dict[str, Any]:
        """获取当前状态摘要"""
        return {
            "project": self.state.project_name,
            "current_phase": {
                "phase": self.state.current_phase.value,
                "label": self.state.current_phase.label,
                "mindset": self.state.current_phase.mindset,
                "status": self.state.phase_status.value,
            },
            "phases": {
                phase.value: {
                    "label": phase.label,
                    "status": status.value,
                }
                for phase, status in self.state.phase_states.items()
            },
            "tasks": {
                "total": len(self.state.tasks),
                "pending": len([t for t in self.state.tasks if t.status == PhaseStatus.PENDING]),
                "in_progress": len([t for t in self.state.tasks if t.status == PhaseStatus.IN_PROGRESS]),
                "completed": len([t for t in self.state.tasks if t.status == PhaseStatus.COMPLETED]),
                "by_priority": {
                    "P0": len(self.state.get_tasks_by_priority(Priority.P0)),
                    "P1": len(self.state.get_tasks_by_priority(Priority.P1)),
                    "P2": len(self.state.get_tasks_by_priority(Priority.P2)),
                },
            },
            "skills_used": self.state.used_skills,
        }

    # ========== 演化记录 ==========

    def record_evolution(self, key: str, value: Any) -> None:
        """记录演化数据"""
        self.state.evolution_data[key] = value
        self.save()

    def get_evolution_data(self) -> Dict[str, Any]:
        """获取演化数据"""
        return self.state.evolution_data

    def export_evolution(self, path: Optional[Path] = None) -> Path:
        """导出演化记录到 JSON"""
        if path is None:
            path = self.base_path / "evolution.json"

        evolution_data = {
            "project": self.state.project_name,
            "generated_at": self.state.created_at.isoformat(),
            "updated_at": self.state.updated_at.isoformat(),
            "phases_completed": [
                phase.value for phase, status in self.state.phase_states.items()
                if status == PhaseStatus.COMPLETED
            ],
            "skills_used": self.state.used_skills,
            "evolution_data": self.state.evolution_data,
            "context": self.state.context,
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(evolution_data, f, indent=2, ensure_ascii=False)

        return path


__all__ = ["GAIAEngine"]
