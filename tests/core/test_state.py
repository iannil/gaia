"""
GAIA Core Tests
"""

from datetime import datetime
import pytest

from gaia_core import (
    Phase,
    PhaseStatus,
    Priority,
    GeneratePath,
    Task,
    GAIAState,
    StateStore,
)
from gaia_core.phases import (
    GeneratePhase,
    AnalyzePhase,
    ImplementPhase,
    AcceptancePhase,
    PhaseFactory,
)
from gaia_core.engine import GAIAEngine


class TestPhase:
    """Phase 枚举测试"""

    def test_phase_values(self):
        """测试阶段值"""
        assert Phase.GENERATE.value == "G"
        assert Phase.ANALYZE.value == "A"
        assert Phase.IMPLEMENT.value == "I"
        assert Phase.ACCEPTANCE.value == "A2"

    def test_phase_labels(self):
        """测试阶段标签"""
        assert Phase.GENERATE.label == "生成"
        assert Phase.ANALYZE.label == "分析"
        assert Phase.IMPLEMENT.label == "实现"
        assert Phase.ACCEPTANCE.label == "验收"

    def test_phase_flow(self):
        """测试阶段流程"""
        flow = Phase.flow()
        assert flow == [Phase.GENERATE, Phase.ANALYZE, Phase.IMPLEMENT, Phase.ACCEPTANCE]


class TestGAIAState:
    """GAIAState 测试"""

    def test_state_creation(self):
        """测试状态创建"""
        state = GAIAState(
            project_id="test-project",
            project_name="Test Project",
        )

        assert state.project_id == "test-project"
        assert state.project_name == "Test Project"
        assert state.current_phase == Phase.GENERATE
        assert state.phase_status == PhaseStatus.PENDING

    def test_add_task(self):
        """测试添加任务"""
        state = GAIAState(
            project_id="test-project",
            project_name="Test Project",
        )

        task = state.add_task("Test Task", Priority.P0)
        assert task.title == "Test Task"
        assert task.priority == Priority.P0
        assert len(state.tasks) == 1

    def test_get_tasks_by_priority(self):
        """测试按优先级获取任务"""
        state = GAIAState(
            project_id="test-project",
            project_name="Test Project",
        )

        state.add_task("Task 1", Priority.P0)
        state.add_task("Task 2", Priority.P1)
        state.add_task("Task 3", Priority.P0)

        p0_tasks = state.get_tasks_by_priority(Priority.P0)
        assert len(p0_tasks) == 2

    def test_transition_to(self):
        """测试阶段转换"""
        state = GAIAState(
            project_id="test-project",
            project_name="Test Project",
        )

        # 正常转换
        assert state.transition_to(Phase.ANALYZE)
        assert state.current_phase == Phase.ANALYZE

        # 不能回退
        assert not state.transition_to(Phase.GENERATE)

    def test_mark_phase_completed(self):
        """测试标记阶段完成"""
        state = GAIAState(
            project_id="test-project",
            project_name="Test Project",
        )

        state.mark_phase_completed(Phase.GENERATE)
        assert state.phase_states[Phase.GENERATE] == PhaseStatus.COMPLETED


class TestStateStore:
    """StateStore 测试"""

    def test_save_and_load(self, tmp_path):
        """测试保存和加载"""
        import tempfile
        import os

        store = StateStore(tmp_path)

        state = GAIAState(
            project_id="test-project",
            project_name="Test Project",
        )
        state.add_task("Test Task", Priority.P0)

        store.save(state)

        loaded = store.load("test-project")
        assert loaded is not None
        assert loaded.project_id == "test-project"
        assert len(loaded.tasks) == 1


class TestPhaseFactory:
    """PhaseFactory 测试"""

    def test_create_phase(self):
        """测试创建阶段"""
        state = GAIAState(
            project_id="test-project",
            project_name="Test Project",
        )

        phase = PhaseFactory.create(Phase.GENERATE, state)
        assert isinstance(phase, GeneratePhase)

    def test_create_current_phase(self):
        """测试创建当前阶段"""
        state = GAIAState(
            project_id="test-project",
            project_name="Test Project",
        )

        phase = PhaseFactory.create_current(state)
        assert isinstance(phase, GeneratePhase)


class TestGeneratePhase:
    """GeneratePhase 测试"""

    def test_validate_preconditions(self):
        """测试前置条件验证"""
        state = GAIAState(
            project_id="test-project",
            project_name="Test Project",
        )

        phase = GeneratePhase(state)

        # 缺少问题陈述
        valid, error = phase.validate_preconditions()
        assert not valid
        assert "问题陈述" in error

        # 添加问题陈述
        state.problem_statement = "需要实现功能 X"
        valid, error = phase.validate_preconditions()
        assert valid


class TestGAIAEngine:
    """GAIAEngine 测试"""

    def test_engine_creation(self, tmp_path):
        """测试引擎创建"""
        engine = GAIAEngine("test-project-engine", base_path=tmp_path)

        assert engine.state.project_name == "test-project-engine"
        assert engine.current_phase == Phase.GENERATE

    def test_start_generate(self, tmp_path):
        """测试启动 Phase G"""
        engine = GAIAEngine("test-project-generate", base_path=tmp_path)

        success, error = engine.start_generate("需要实现用户认证")
        assert success

        # 设置解决方案大纲后才能完成 Phase G
        engine.set_solution_outline("使用 JWT 实现")

        # 现在应该可以推进到下一阶段
        success, _ = engine.advance_phase()
        assert success
        assert engine.current_phase == Phase.ANALYZE

    def test_add_task(self, tmp_path):
        """测试添加任务"""
        engine = GAIAEngine("test-project-add", base_path=tmp_path)

        engine.add_task("实现登录", Priority.P0)
        assert len(engine.state.tasks) == 1

    def test_get_status(self, tmp_path):
        """测试获取状态"""
        engine = GAIAEngine("test-project-status", base_path=tmp_path)

        status = engine.get_status()
        assert status["project"] == "test-project-status"
        assert "current_phase" in status
        assert "tasks" in status

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
