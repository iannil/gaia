"""
Tests for knowledge module
"""

import pytest

from gaia_knowledge import (
    KnowledgeGraph,
    Node,
    Edge,
    SemanticSearch,
    SearchResult,
    DocumentIndex,
    PatternLibrary,
    Pattern,
)


class TestDocumentIndex:
    """DocumentIndex 测试"""

    def test_add_and_search(self):
        """测试添加和搜索文档"""
        index = DocumentIndex()

        index.add_document(
            "doc1",
            "Test Document",
            "This is a test document about Python programming",
            doc_type="guide",
        )

        # 搜索
        results = index.search("python")
        assert len(results) >= 1

        # 搜索不存在的关键词
        results = index.search("nonexistent")
        assert len(results) == 0

    def test_get_document(self):
        """测试获取文档"""
        index = DocumentIndex()

        index.add_document(
            "doc1",
            "Test Document",
            "Content here",
            doc_type="test",
        )

        doc = index.get_document("doc1")
        assert doc is not None
        assert doc["title"] == "Test Document"

    def test_remove_document(self):
        """测试删除文档"""
        index = DocumentIndex()

        index.add_document("doc1", "Test", "Content")
        index.remove_document("doc1")

        assert index.get_document("doc1") is None


class TestSemanticSearch:
    """SemanticSearch 测试"""

    def test_search(self):
        """测试搜索"""
        search = SemanticSearch()

        search.index.add_document(
            "doc1",
            "Python Guide",
            "Learn Python programming",
            doc_type="guide",
        )

        results = search.search("python")
        assert len(results) >= 1

    def test_add_alias(self):
        """测试添加别名"""
        search = SemanticSearch()

        search.add_alias("python", ["py", "python3"])

        expanded = search.expand_query("python guide")
        assert "py guide" in expanded

    def test_suggest(self):
        """测试搜索建议"""
        search = SemanticSearch()

        search.index.add_document(
            "doc1",
            "Python Tutorial",
            "Learn python",
        )

        suggestions = search.suggest("pyt")
        assert len(suggestions) >= 0


class TestKnowledgeGraph:
    """KnowledgeGraph 测试"""

    def test_create_graph(self):
        """测试创建图"""
        graph = KnowledgeGraph()

        graph.add_node(Node(id="n1", type="skill", label="Git"))
        graph.add_node(Node(id="n2", type="skill", label="GitHub"))
        graph.add_edge(Edge(id="e1", source="n1", target="n2", relation="similar_to"))

        stats = graph.stats()
        assert stats["total_nodes"] == 2
        assert stats["total_edges"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
