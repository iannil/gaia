"""
Type stubs for gaia_knowledge
"""

from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass

class Node:
    """Knowledge graph node"""
    id: str
    type: str
    label: str
    data: Dict[str, Any]
    created_at: str

    def to_dict(self) -> Dict[str, Any]: ...
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Node": ...

class Edge:
    """Knowledge graph edge"""
    id: str
    source: str
    target: str
    relation: str
    weight: float
    data: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]: ...
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Edge": ...

class KnowledgeGraph:
    """Knowledge graph for managing relationships"""
    _nodes: Dict[str, Node]
    _edges: Dict[str, Edge]
    _adjacency: Dict[str, set]

    def __init__(self) -> None: ...

    @property
    def nodes(self) -> List[Node]: ...
    @property
    def edges(self) -> List[Edge]: ...

    def count(self) -> int: ...

    def add_node(self, node: Node) -> None: ...
    def get_node(self, node_id: str) -> Optional[Node]: ...
    def remove_node(self, node_id: str) -> None: ...
    def get_nodes_by_type(self, node_type: str) -> List[Node]: ...
    def search_nodes(self, query: str) -> List[Node]: ...

    def add_edge(self, edge: Edge) -> None: ...
    def get_edge(self, edge_id: str) -> Optional[Edge]: ...
    def remove_edge(self, edge_id: str) -> None: ...
    def get_edges(
        self,
        source: Optional[str] = None,
        target: Optional[str] = None,
        relation: Optional[str] = None
    ) -> List[Edge]: ...

    def get_neighbors(self, node_id: str) -> List[Node]: ...
    def get_neighbors_by_relation(self, node_id: str, relation: str) -> List[Node]: ...

    def shortest_path(self, source: str, target: str) -> Optional[List[str]]: ...
    def find_related(self, node_id: str, max_depth: int = 2) -> List[Node]: ...

    def get_degree(self, node_id: str) -> int: ...
    def get_centrality(self) -> Dict[str, float]: ...
    def get_connected_components(self) -> List[List[str]]: ...

    def to_dict(self) -> Dict[str, Any]: ...
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "KnowledgeGraph": ...
    def to_json(self, path: Path) -> None: ...
    @classmethod
    def from_json(cls, path: Path) -> "KnowledgeGraph": ...

class SearchResult:
    """Search result"""
    id: str
    type: str
    score: float
    title: str
    snippet: str

class DocumentIndex:
    """Document index for search"""
    _documents: Dict[str, Dict[str, Any]]
    _inverted_index: Dict[str, set]
    _document_vectors: Dict[str, Any]

    def __init__(self) -> None: ...

    def add_document(
        self,
        doc_id: str,
        title: str,
        content: str,
        doc_type: str = ...,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None: ...
    def remove_document(self, doc_id: str) -> None: ...
    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]: ...
    def get_all_documents(self) -> List[Dict[str, Any]]: ...
    def stats(self) -> Dict[str, Any]: ...

    def search(
        self,
        query: str,
        limit: int = ...,
        doc_type: Optional[str] = None
    ) -> List[SearchResult]: ...

class SemanticSearch:
    """Semantic search with query expansion"""
    index: DocumentIndex
    _aliases: Dict[str, List[str]]

    def __init__(self, index: Optional[DocumentIndex] = None) -> None: ...

    def add_alias(self, term: str, aliases: List[str]) -> None: ...
    def expand_query(self, query: str) -> List[str]: ...

    def search(
        self,
        query: str,
        limit: int = ...,
        expand: bool = True
    ) -> List[SearchResult]: ...

class Pattern:
    """Best practice or anti-pattern"""
    id: str
    name: str
    type: str  # "best_practice" or "anti_pattern"
    category: str
    title: str
    description: str
    context: str
    solution: str
    examples: List[str]
    tags: List[str]
    related: List[str]

    def matches(self, query: str) -> bool: ...

class PatternLibrary:
    """Library of patterns"""
    _patterns: Dict[str, Pattern]
    _categories: Dict[str, List[str]]

    def __init__(self) -> None: ...

    def add(self, pattern: Pattern) -> None: ...
    def get(self, pattern_id: str) -> Optional[Pattern]: ...
    def remove(self, pattern_id: str) -> bool: ...
    def count(self) -> int: ...

    def list_by_type(self, pattern_type: str) -> List[Pattern]: ...
    def list_by_category(self, category: str) -> List[Pattern]: ...
    def list_by_tag(self, tag: str) -> List[Pattern]: ...
    def search(self, query: str) -> List[Pattern]: ...

    def get_best_practices(self, category: Optional[str] = None) -> List[Pattern]: ...
    def get_anti_patterns(self, category: Optional[str] = None) -> List[Pattern]: ...
    def get_categories(self) -> List[str]: ...
    def get_tags(self) -> List[str]: ...

    def load_builtin_patterns(self) -> None: ...

__all__ = [
    "Node",
    "Edge",
    "KnowledgeGraph",
    "SearchResult",
    "DocumentIndex",
    "SemanticSearch",
    "Pattern",
    "PatternLibrary",
]
