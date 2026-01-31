"""
GAIA Knowledge - Knowledge Evolution System

GAIA 知识演化系统。

提供:
- Graph: 知识图谱，维护实体间的关系网络
- Search: 智能检索，基于语义的文档搜索
- Patterns: 模式库，最佳实践和反模式
"""

from .graph import Node, Edge, KnowledgeGraph
from .search import SearchResult, DocumentIndex, SemanticSearch
from .patterns import Pattern, PatternLibrary

__version__ = "0.1.0"

__all__ = [
    # Graph
    "Node",
    "Edge",
    "KnowledgeGraph",
    # Search
    "SearchResult",
    "DocumentIndex",
    "SemanticSearch",
    # Patterns
    "Pattern",
    "PatternLibrary",
]
