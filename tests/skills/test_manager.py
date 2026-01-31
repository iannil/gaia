"""
GAIA Skills Tests
"""

import pytest

from gaia_skills import SkillManager, SkillMetadata, EvolutionManager, EvolutionRecord
from gaia_knowledge import KnowledgeGraph, Node, Edge


class TestSkillMetadata:
    """SkillMetadata 测试"""

    def test_metadata_creation(self):
        """测试元数据创建"""
        meta = SkillMetadata(
            id="test-skill",
            name="Test Skill",
            version="1.0.0",
            description="A test skill",
            category="testing",
            tags=["test", "example"],
        )

        assert meta.id == "test-skill"
        assert meta.name == "Test Skill"
        assert "test" in meta.tags


class TestSkillManager:
    """SkillManager 测试"""

    def test_manager_status(self):
        """测试管理器状态"""
        manager = SkillManager()
        status = manager.get_status()

        assert "total" in status
        assert "enabled" in status


class TestEvolutionManager:
    """EvolutionManager 测试"""

    def test_manager_creation(self):
        """测试管理器创建"""
        manager = EvolutionManager()

        assert not manager.exists()

    def test_create_record(self):
        """测试创建演化记录"""
        manager = EvolutionManager()
        record = manager.create(
            skill_id="test-skill",
            skill_name="Test Skill",
            version="1.0.0",
        )

        assert record.skill_id == "test-skill"
        assert record.skill_name == "Test Skill"

    def test_record_parameter(self):
        """测试记录参数"""
        record = EvolutionRecord("test-skill", "Test Skill")

        record.record_parameter(
            "param1",
            "value1",
            "用于测试",
        )

        assert "param1" in record.effective_parameters

    def test_record_success_pattern(self):
        """测试记录成功模式"""
        record = EvolutionRecord("test-skill", "Test Skill")

        record.record_success_pattern(
            "pattern1",
            "测试场景",
            "成功",
        )

        assert len(record.success_patterns) == 1

    def test_record_anti_pattern(self):
        """测试记录反模式"""
        record = EvolutionRecord("test-skill", "Test Skill")

        record.record_anti_pattern(
            "bad_pattern",
            "失败原因",
            "正确做法",
        )

        assert len(record.anti_patterns) == 1

    def test_save_and_get_record(self, tmp_path):
        """测试保存和获取记录"""
        manager = EvolutionManager(tmp_path)

        record = manager.create("test-skill", "Test Skill")
        record.record_parameter("param1", "value1", "测试")

        manager.save_record(record)

        retrieved = manager.get_record("test-skill")
        assert retrieved is not None
        assert "param1" in retrieved.effective_parameters


class TestKnowledgeGraph:
    """KnowledgeGraph 测试"""

    def test_graph_creation(self):
        """测试图创建"""
        graph = KnowledgeGraph()

        assert len(graph._nodes) == 0
        assert len(graph._edges) == 0

    def test_add_node(self):
        """测试添加节点"""
        graph = KnowledgeGraph()
        node = Node(id="test", type="test", label="Test Node")

        graph.add_node(node)

        assert graph.get_node("test") == node
        assert len(graph._nodes) == 1

    def test_add_edge(self):
        """测试添加边"""
        graph = KnowledgeGraph()

        graph.add_node(Node(id="n1", type="test", label="Node 1"))
        graph.add_node(Node(id="n2", type="test", label="Node 2"))

        edge = Edge(id="e1", source="n1", target="n2", relation="connects")
        graph.add_edge(edge)

        assert len(graph._edges) == 1
        assert len(graph.get_neighbors("n1")) == 1

    def test_search_nodes(self):
        """测试搜索节点"""
        graph = KnowledgeGraph()

        graph.add_node(Node(id="test", type="test", label="Test Node"))
        graph.add_node(Node(id="other", type="test", label="Other Node"))

        results = graph.search_nodes("test")
        assert len(results) >= 1

    def test_shortest_path(self):
        """测试最短路径"""
        graph = KnowledgeGraph()

        graph.add_node(Node(id="a", type="test", label="A"))
        graph.add_node(Node(id="b", type="test", label="B"))
        graph.add_node(Node(id="c", type="test", label="C"))

        graph.add_edge(Edge(id="e1", source="a", target="b", relation="connects"))
        graph.add_edge(Edge(id="e2", source="b", target="c", relation="connects"))

        path = graph.shortest_path("a", "c")
        assert path is not None
        assert path == ["a", "b", "c"]

    def test_get_centrality(self):
        """测试中心性计算"""
        graph = KnowledgeGraph()

        graph.add_node(Node(id="a", type="test", label="A"))
        graph.add_node(Node(id="b", type="test", label="B"))
        graph.add_node(Node(id="c", type="test", label="C"))

        graph.add_edge(Edge(id="e1", source="a", target="b", relation="connects"))
        graph.add_edge(Edge(id="e2", source="a", target="c", relation="connects"))

        centrality = graph.get_centrality()
        assert centrality["a"] > centrality["b"]
        assert centrality["a"] == 1.0

    def test_to_and_from_json(self, tmp_path):
        """测试 JSON 序列化"""
        from gaia_knowledge import KnowledgeGraph, Node, Edge

        graph = KnowledgeGraph()
        graph.add_node(Node(id="test", type="test", label="Test"))
        graph.add_edge(Edge(id="e1", source="test", target="test", relation="self"))

        json_file = tmp_path / "graph.json"
        graph.to_json(json_file)

        loaded = KnowledgeGraph.from_json(json_file)

        assert len(loaded._nodes) == 1
        assert len(loaded._edges) == 1


class TestPatternLibrary:
    """PatternLibrary 测试"""

    def test_load_builtin_patterns(self):
        """测试加载内置模式"""
        from gaia_knowledge import PatternLibrary

        library = PatternLibrary()
        library.load_builtin_patterns()

        assert library.count() > 0

    def test_best_practices(self):
        """测试获取最佳实践"""
        from gaia_knowledge import PatternLibrary

        library = PatternLibrary()
        library.load_builtin_patterns()

        best_practices = library.get_best_practices()
        assert len(best_practices) > 0

        for pattern in best_practices:
            assert pattern.type == "best_practice"

    def test_anti_patterns(self):
        """测试获取反模式"""
        from gaia_knowledge import PatternLibrary

        library = PatternLibrary()
        library.load_builtin_patterns()

        anti_patterns = library.get_anti_patterns()
        assert len(anti_patterns) > 0

        for pattern in anti_patterns:
            assert pattern.type == "anti_pattern"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
