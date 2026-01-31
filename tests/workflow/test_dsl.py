"""
Tests for workflow module
"""

import pytest

from gaia_workflow import (
    Workflow,
    Step,
    Trigger,
    TriggerType,
    WorkflowParser,
    WorkflowBuilder,
    WorkflowExecutor,
    Actions,
)


class TestWorkflowDSL:
    """Workflow DSL 测试"""

    def test_workflow_creation(self):
        """测试工作流创建"""
        workflow = Workflow(
            id="test-workflow",
            name="Test Workflow",
        )

        assert workflow.id == "test-workflow"
        assert workflow.name == "Test Workflow"

    def test_step_creation(self):
        """测试步骤创建"""
        step = Step(
            id="step1",
            name="Step 1",
            action="echo",
        )

        assert step.id == "step1"
        assert step.action == "echo"

    def test_add_step(self):
        """测试添加步骤"""
        workflow = Workflow(id="test", name="Test")
        step = Step(id="s1", name="S1", action="echo")

        workflow.steps.append(step)

        assert len(workflow.steps) == 1

    def test_get_start_steps(self):
        """测试获取起始步骤"""
        workflow = Workflow(id="test", name="Test")
        workflow.steps.append(
            Step(id="s1", name="S1", action="echo")
        )
        workflow.steps.append(
            Step(id="s2", name="S2", action="echo", depends_on=["s1"])
        )

        start = workflow.get_start_steps()
        assert len(start) == 1
        assert start[0].id == "s1"

    def test_get_ready_steps(self):
        """测试获取可执行步骤"""
        workflow = Workflow(id="test", name="Test")
        workflow.steps.append(
            Step(id="s1", name="S1", action="echo")
        )
        workflow.steps.append(
            Step(id="s2", name="S2", action="echo", depends_on=["s1"])
        )

        ready = workflow.get_ready_steps(set())
        assert len(ready) == 1
        assert ready[0].id == "s1"


class TestWorkflowParser:
    """WorkflowParser 测试"""

    def test_parse_yaml(self):
        """测试解析 YAML"""
        yaml_content = """
id: test-workflow
name: Test Workflow
steps:
  - id: step1
    name: Step 1
    action: echo
    parameters:
      message: Hello
"""

        parser = WorkflowParser()
        workflow = parser.parse(yaml_content)

        assert workflow.id == "test-workflow"
        assert len(workflow.steps) == 1

    def test_validate_workflow(self):
        """测试验证工作流"""
        yaml_content = """
id: test-workflow
name: Test Workflow
steps:
  - id: step1
    name: Step 1
    action: echo
"""

        parser = WorkflowParser()
        workflow = parser.parse(yaml_content)
        errors = parser.validate(workflow)

        assert len(errors) == 0

    def test_circular_dependency(self):
        """测试循环依赖检测"""
        parser = WorkflowParser()

        workflow = Workflow(id="test", name="Test")
        workflow.steps.append(
            Step(id="s1", name="S1", action="echo", depends_on=["s2"])
        )
        workflow.steps.append(
            Step(id="s2", name="S2", action="echo", depends_on=["s1"])
        )

        errors = parser.validate(workflow)
        assert any("循环依赖" in e for e in errors)


class TestWorkflowBuilder:
    """WorkflowBuilder 测试"""

    def test_build_workflow(self):
        """测试构建工作流"""
        builder = WorkflowBuilder("test", "Test Workflow")

        builder \
            .description("A test workflow") \
            .variable("var1", "value1") \
            .step("s1", "echo", parameters={"message": "Hello"})

        workflow = builder.build()

        assert workflow.id == "test"
        assert workflow.description == "A test workflow"
        assert workflow.variables["var1"] == "value1"
        assert len(workflow.steps) == 1


class TestActions:
    """Actions 测试"""

    def test_action_constants(self):
        """测试动作常量"""
        assert Actions.PHASE_GENERATE == "gaia.phase.generate"
        assert Actions.PHASE_ANALYZE == "gaia.phase.analyze"
        assert Actions.PHASE_IMPLEMENT == "gaia.phase.implement"
        assert Actions.PHASE_ACCEPTANCE == "gaia.phase.acceptance"
        assert Actions.SKILL_INSTALL == "gaia.skill.install"
        assert Actions.ECHO == "echo"


class TestWorkflowExecutor:
    """WorkflowExecutor 测试"""

    def test_create_executor(self):
        """测试创建执行器"""
        executor = WorkflowExecutor()

        assert executor is not None

    def test_execute_simple_workflow(self):
        """测试执行简单工作流"""
        builder = WorkflowBuilder("test", "Test")
        builder.step("s1", Actions.ECHO, parameters={"message": "Hello"})

        workflow = builder.build()
        executor = WorkflowExecutor()

        execution = executor.execute_sync(workflow)

        assert execution is not None
        assert execution.workflow_id == "test"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
