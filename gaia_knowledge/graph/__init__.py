"""
GAIA Knowledge - Graph

知识图谱模块，维护 Skill、任务、经验之间的关系网络。
"""

from typing import Dict, List, Set, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import json


@dataclass
class Node:
    """图节点"""

    id: str
    type: str  # skill, task, experience, concept, pattern
    label: str
    data: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "label": self.label,
            "data": self.data,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Node":
        return cls(
            id=data["id"],
            type=data["type"],
            label=data["label"],
            data=data.get("data", {}),
            created_at=data.get("created_at", datetime.now().isoformat()),
        )


@dataclass
class Edge:
    """图边（关系）"""

    id: str
    source: str  # 源节点 ID
    target: str  # 目标节点 ID
    relation: str  # 关系类型: depends_on, similar_to, solves, contains, etc.
    weight: float = 1.0  # 关系强度
    data: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "source": self.source,
            "target": self.target,
            "relation": self.relation,
            "weight": self.weight,
            "data": self.data,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Edge":
        return cls(
            id=data["id"],
            source=data["source"],
            target=data["target"],
            relation=data["relation"],
            weight=data.get("weight", 1.0),
            data=data.get("data", {}),
        )


class KnowledgeGraph:
    """知识图谱

    维护 Skill、任务、经验等实体之间的关系网络。
    """

    # 关系类型定义
    RELATION_DEPENDS_ON = "depends_on"
    RELATION_SIMILAR_TO = "similar_to"
    RELATION_SOLVES = "solves"
    RELATION_CONTAINS = "contains"
    RELATION_RELATED_TO = "related_to"
    RELATION_PRECEDES = "precedes"
    RELATION_FOLLOWS = "follows"
    RELATION_EXAMPLE_OF = "example_of"
    RELATION_PART_OF = "part_of"

    def __init__(self):
        self._nodes: Dict[str, Node] = {}
        self._edges: Dict[str, Edge] = {}
        self._adjacency: Dict[str, Set[str]] = {}  # 邻接表

    # ========== 节点操作 ==========

    @property
    def nodes(self) -> List[Node]:
        """获取所有节点"""
        return list(self._nodes.values())

    @property
    def edges(self) -> List[Edge]:
        """获取所有边"""
        return list(self._edges.values())

    def count(self) -> int:
        """返回节点总数"""
        return len(self._nodes)

    def add_node(self, node: Node) -> None:
        """添加节点"""
        self._nodes[node.id] = node
        if node.id not in self._adjacency:
            self._adjacency[node.id] = set()

    def get_node(self, node_id: str) -> Optional[Node]:
        """获取节点"""
        return self._nodes.get(node_id)

    def remove_node(self, node_id: str) -> None:
        """删除节点及相关边"""
        if node_id in self._nodes:
            del self._nodes[node_id]

        # 删除相关边
        edges_to_remove = [
            edge_id for edge_id, edge in self._edges.items()
            if edge.source == node_id or edge.target == node_id
        ]
        for edge_id in edges_to_remove:
            self.remove_edge(edge_id)

        # 删除邻接信息
        if node_id in self._adjacency:
            del self._adjacency[node_id]

        # 从其他节点的邻接表中删除
        for neighbors in self._adjacency.values():
            neighbors.discard(node_id)

    def get_nodes_by_type(self, node_type: str) -> List[Node]:
        """按类型获取节点"""
        return [n for n in self._nodes.values() if n.type == node_type]

    def search_nodes(self, query: str) -> List[Node]:
        """搜索节点"""
        query_lower = query.lower()
        return [
            n for n in self._nodes.values()
            if query_lower in n.label.lower()
            or any(query_lower in str(v).lower() for v in n.data.values())
        ]

    # ========== 边操作 ==========

    def add_edge(self, edge: Edge) -> None:
        """添加边"""
        self._edges[edge.id] = edge

        # 更新邻接表
        if edge.source not in self._adjacency:
            self._adjacency[edge.source] = set()
        if edge.target not in self._adjacency:
            self._adjacency[edge.target] = set()

        self._adjacency[edge.source].add(edge.target)
        self._adjacency[edge.target].add(edge.source)

    def remove_edge(self, edge_id: str) -> None:
        """删除边"""
        edge = self._edges.get(edge_id)
        if not edge:
            return

        del self._edges[edge_id]

        # 更新邻接表
        if edge.source in self._adjacency:
            self._adjacency[edge.source].discard(edge.target)
        if edge.target in self._adjacency:
            self._adjacency[edge.target].discard(edge.source)

    def get_edge(self, edge_id: str) -> Optional[Edge]:
        """获取边"""
        return self._edges.get(edge_id)

    def get_edges(
        self,
        source: Optional[str] = None,
        target: Optional[str] = None,
        relation: Optional[str] = None,
    ) -> List[Edge]:
        """获取边"""
        edges = list(self._edges.values())

        if source:
            edges = [e for e in edges if e.source == source]
        if target:
            edges = [e for e in edges if e.target == target]
        if relation:
            edges = [e for e in edges if e.relation == relation]

        return edges

    # ========== 图查询 ==========

    def get_neighbors(self, node_id: str) -> List[Node]:
        """获取邻居节点"""
        if node_id not in self._adjacency:
            return []

        neighbor_ids = self._adjacency[node_id]
        return [self._nodes[nid] for nid in neighbor_ids if nid in self._nodes]

    def get_neighbors_by_relation(
        self, node_id: str, relation: str
    ) -> List[Node]:
        """按关系类型获取邻居"""
        edges = self.get_edges(source=node_id, relation=relation)
        target_ids = [e.target for e in edges]
        return [self._nodes[tid] for tid in target_ids if tid in self._nodes]

    def shortest_path(self, source: str, target: str) -> Optional[List[str]]:
        """计算最短路径"""
        if source not in self._nodes or target not in self._nodes:
            return None

        if source == target:
            return [source]

        # BFS
        from collections import deque

        queue = deque([(source, [source])])
        visited = {source}

        while queue:
            current, path = queue.popleft()

            for neighbor in self._adjacency.get(current, set()):
                if neighbor == target:
                    return path + [neighbor]

                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return None

    def find_related(self, node_id: str, max_depth: int = 2) -> List[Node]:
        """查找相关节点（广度优先）"""
        if node_id not in self._nodes:
            return []

        result = set()
        current_level = {node_id}

        for _ in range(max_depth):
            next_level = set()
            for nid in current_level:
                neighbors = self._adjacency.get(nid, set())
                for neighbor in neighbors:
                    if neighbor != node_id and neighbor not in result:
                        result.add(neighbor)
                        next_level.add(neighbor)
            current_level = next_level

        return [self._nodes[nid] for nid in result if nid in self._nodes]

    # ========== 图分析 ==========

    def get_degree(self, node_id: str) -> int:
        """获取节点度数"""
        return len(self._adjacency.get(node_id, set()))

    def get_connected_components(self) -> List[List[str]]:
        """获取连通分量"""
        visited = set()
        components = []

        for node_id in self._nodes:
            if node_id not in visited:
                component = []
                queue = [node_id]
                visited.add(node_id)

                while queue:
                    current = queue.pop(0)
                    component.append(current)

                    for neighbor in self._adjacency.get(current, set()):
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)

                components.append(component)

        return components

    def get_centrality(self) -> Dict[str, float]:
        """计算节点中心性（度中心性）"""
        max_degree = max((self.get_degree(nid) for nid in self._nodes), default=1)

        if max_degree == 0:
            return {nid: 0.0 for nid in self._nodes}

        return {
            nid: self.get_degree(nid) / max_degree
            for nid in self._nodes
        }

    # ========== 序列化 ==========

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "nodes": [n.to_dict() for n in self._nodes.values()],
            "edges": [e.to_dict() for e in self._edges.values()],
        }

    def to_json(self, path: Path) -> None:
        """导出为 JSON"""
        data = self.to_dict()
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "KnowledgeGraph":
        """从字典创建"""
        graph = cls()

        for node_data in data.get("nodes", []):
            graph.add_node(Node.from_dict(node_data))

        for edge_data in data.get("edges", []):
            graph.add_edge(Edge.from_dict(edge_data))

        return graph

    @classmethod
    def from_json(cls, path: Path) -> "KnowledgeGraph":
        """从 JSON 加载"""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)

    # ========== 统计 ==========

    def stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        node_types = {}
        for node in self._nodes.values():
            node_types[node.type] = node_types.get(node.type, 0) + 1

        relation_types = {}
        for edge in self._edges.values():
            relation_types[edge.relation] = relation_types.get(edge.relation, 0) + 1

        return {
            "total_nodes": len(self._nodes),
            "total_edges": len(self._edges),
            "node_types": node_types,
            "relation_types": relation_types,
            "connected_components": len(self.get_connected_components()),
        }


__all__ = [
    "Node",
    "Edge",
    "KnowledgeGraph",
]
