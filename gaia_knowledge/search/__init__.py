"""
GAIA Knowledge - Search

智能检索模块，提供基于语义的知识搜索。
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import re
from collections import Counter


@dataclass
class SearchResult:
    """搜索结果"""

    id: str
    type: str
    title: str
    content: str
    score: float
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "title": self.title,
            "content": self.content,
            "score": self.score,
            "metadata": self.metadata,
        }


class DocumentIndex:
    """文档索引

    对知识文档进行索引和搜索。
    """

    def __init__(self):
        self._documents: Dict[str, Dict[str, Any]] = {}
        self._inverted_index: Dict[str, set] = {}  # 词汇 -> 文档 ID 集合
        self._document_vectors: Dict[str, Counter] = {}  # 文档词频向量

    def add_document(
        self,
        doc_id: str,
        title: str,
        content: str,
        doc_type: str = "general",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """添加文档到索引"""
        metadata = metadata or {}

        # 存储文档
        self._documents[doc_id] = {
            "id": doc_id,
            "title": title,
            "content": content,
            "type": doc_type,
            "metadata": metadata,
        }

        # 分词和建立索引
        text = f"{title} {content}"
        tokens = self._tokenize(text)

        # 更新倒排索引
        for token in set(tokens):
            if token not in self._inverted_index:
                self._inverted_index[token] = set()
            self._inverted_index[token].add(doc_id)

        # 存储文档向量
        self._document_vectors[doc_id] = Counter(tokens)

    def remove_document(self, doc_id: str) -> None:
        """从索引中删除文档"""
        if doc_id not in self._documents:
            return

        # 从倒排索引中删除
        tokens = self._document_vectors.get(doc_id, Counter()).keys()
        for token in tokens:
            if token in self._inverted_index:
                self._inverted_index[token].discard(doc_id)
                if not self._inverted_index[token]:
                    del self._inverted_index[token]

        # 删除文档和向量
        del self._documents[doc_id]
        if doc_id in self._document_vectors:
            del self._document_vectors[doc_id]

    def _tokenize(self, text: str) -> List[str]:
        """分词"""
        # 简单的分词实现（实际可用更复杂的分词器）
        # 转小写，分词，过滤停用词
        text = text.lower()
        # 分词：按非字母数字字符分割
        tokens = re.findall(r'\w+', text)
        # 过滤停用词
        stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
            'for', 'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are',
            'were', 'been', 'be', 'have', 'has', 'had', 'do', 'does', 'did',
            '的', '了', '是', '在', '有', '和', '与', '或', '但是', '然而',
            '因此', '所以', '如果', '那么', '这个', '那个', '这些', '那些',
        }
        return [t for t in tokens if len(t) > 1 and t not in stopwords]

    def search(
        self,
        query: str,
        limit: int = 10,
        doc_type: Optional[str] = None,
    ) -> List[SearchResult]:
        """搜索文档

        Args:
            query: 搜索查询
            limit: 返回结果数量
            doc_type: 文档类型过滤

        Returns:
            搜索结果列表
        """
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []

        # 计算文档得分
        scores = {}

        for token in query_tokens:
            # 获取包含该 token 的文档
            doc_ids = self._inverted_index.get(token, set())

            for doc_id in doc_ids:
                # 简单的 TF 计算
                doc_vector = self._document_vectors.get(doc_id, Counter())
                tf = doc_vector.get(token, 0)

                # 累加得分
                scores[doc_id] = scores.get(doc_id, 0) + tf

        # 按 ID 过滤
        if doc_type:
            scores = {
                doc_id: score
                for doc_id, score in scores.items()
                if self._documents.get(doc_id, {}).get("type") == doc_type
            }

        # 归一化得分
        if scores:
            max_score = max(scores.values())
            scores = {k: v / max_score for k, v in scores.items()}

        # 排序并返回结果
        results = []
        for doc_id, score in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]:
            doc = self._documents[doc_id]
            results.append(SearchResult(
                id=doc_id,
                type=doc["type"],
                title=doc["title"],
                content=doc["content"][:200] + "..." if len(doc["content"]) > 200 else doc["content"],
                score=score,
                metadata=doc.get("metadata", {}),
            ))

        return results

    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """获取文档"""
        return self._documents.get(doc_id)

    def get_all_documents(self) -> List[Dict[str, Any]]:
        """获取所有文档"""
        return list(self._documents.values())

    def stats(self) -> Dict[str, Any]:
        """获取索引统计"""
        return {
            "total_documents": len(self._documents),
            "unique_terms": len(self._inverted_index),
            "avg_document_length": sum(
                len(v) for v in self._document_vectors.values()
            ) / len(self._document_vectors) if self._document_vectors else 0,
        }


class SemanticSearch:
    """语义搜索

    结合文档索引和知识图谱的语义搜索。
    """

    def __init__(self, index: Optional[DocumentIndex] = None):
        self.index = index or DocumentIndex()
        self._aliases: Dict[str, List[str]] = {}  # 术语别名

    def add_alias(self, term: str, aliases: List[str]) -> None:
        """添加术语别名"""
        self._aliases[term.lower()] = [a.lower() for a in aliases]

    def expand_query(self, query: str) -> List[str]:
        """扩展查询（使用别名）"""
        query_lower = query.lower()
        expanded = [query]

        for term, aliases in self._aliases.items():
            if term in query_lower:
                for alias in aliases:
                    expanded.append(query_lower.replace(term, alias))

        return expanded

    def search(
        self,
        query: str,
        limit: int = 10,
        expand: bool = True,
    ) -> List[SearchResult]:
        """语义搜索

        Args:
            query: 搜索查询
            limit: 返回结果数量
            expand: 是否进行查询扩展

        Returns:
            搜索结果列表
        """
        # 查询扩展
        queries = [query]
        if expand:
            queries.extend(self.expand_query(query)[1:])

        # 执行搜索
        all_results = {}
        for q in queries:
            results = self.index.search(q, limit=limit * 2)
            for result in results:
                if result.id in all_results:
                    # 合并得分
                    all_results[result.id].score = max(
                        all_results[result.id].score,
                        result.score
                    )
                else:
                    all_results[result.id] = result

        # 排序并返回
        results = sorted(all_results.values(), key=lambda r: r.score, reverse=True)
        return results[:limit]

    def suggest(self, partial: str, limit: int = 5) -> List[str]:
        """获取搜索建议"""
        partial_lower = partial.lower()
        suggestions = set()

        # 从索引中查找匹配的术语
        for term in self.index._inverted_index.keys():
            if term.startswith(partial_lower):
                suggestions.add(term)

        # 从别名中查找
        for term, aliases in self._aliases.items():
            if term.startswith(partial_lower):
                suggestions.add(term)
            for alias in aliases:
                if alias.startswith(partial_lower):
                    suggestions.add(alias)

        return sorted(list(suggestions))[:limit]

    def index_from_directory(
        self,
        directory: Path,
        pattern: str = "*.md",
    ) -> None:
        """从目录索引文档

        Args:
            directory: 文档目录
            pattern: 文件匹配模式
        """
        for file_path in directory.rglob(pattern):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # 提取标题（第一行 # 开头的）
                title = file_path.stem
                lines = content.split('\n')
                for line in lines:
                    if line.startswith('# '):
                        title = line[2:].strip()
                        break

                self.index.add_document(
                    doc_id=str(file_path.relative_to(directory)),
                    title=title,
                    content=content,
                    doc_type="documentation",
                    metadata={"path": str(file_path)},
                )
            except Exception:
                continue


__all__ = [
    "SearchResult",
    "DocumentIndex",
    "SemanticSearch",
]
