"""
GAIA Knowledge - Patterns

模式库模块，维护最佳实践和反模式。
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import json


@dataclass
class Pattern:
    """模式（最佳实践或反模式）"""

    id: str
    name: str
    type: str  # best_practice, anti_pattern
    category: str  # testing, security, performance, etc.
    title: str
    description: str
    context: str  # 适用场景
    solution: str  # 解决方案（最佳实践）或 替代方案（反模式）
    examples: List[str] = field(default_factory=list)
    consequences: str = ""  # 后果（主要用于反模式）
    references: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "category": self.category,
            "title": self.title,
            "description": self.description,
            "context": self.context,
            "solution": self.solution,
            "examples": self.examples,
            "consequences": self.consequences,
            "references": self.references,
            "tags": self.tags,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Pattern":
        return cls(**data)


class PatternLibrary:
    """模式库

    管理最佳实践和反模式。
    """

    def __init__(self):
        self._patterns: Dict[str, Pattern] = {}
        self._categories: Dict[str, List[str]] = {}

    def add(self, pattern: Pattern) -> None:
        """添加模式"""
        self._patterns[pattern.id] = pattern

        # 更新分类索引
        if pattern.category not in self._categories:
            self._categories[pattern.category] = []
        if pattern.id not in self._categories[pattern.category]:
            self._categories[pattern.category].append(pattern.id)

    def get(self, pattern_id: str) -> Optional[Pattern]:
        """获取模式"""
        return self._patterns.get(pattern_id)

    def remove(self, pattern_id: str) -> bool:
        """删除模式"""
        if pattern_id not in self._patterns:
            return False

        pattern = self._patterns[pattern_id]
        del self._patterns[pattern_id]

        # 更新分类索引
        if pattern.category in self._categories:
            self._categories[pattern.category].remove(pattern_id)
            if not self._categories[pattern.category]:
                del self._categories[pattern.category]

        return True

    def count(self) -> int:
        """返回模式总数"""
        return len(self._patterns)

    def list_by_type(self, pattern_type: str) -> List[Pattern]:
        """按类型列出模式"""
        return [p for p in self._patterns.values() if p.type == pattern_type]

    def list_by_category(self, category: str) -> List[Pattern]:
        """按分类列出模式"""
        pattern_ids = self._categories.get(category, [])
        return [self._patterns[pid] for pid in pattern_ids if pid in self._patterns]

    def list_by_tag(self, tag: str) -> List[Pattern]:
        """按标签列出模式"""
        return [p for p in self._patterns.values() if tag in p.tags]

    def search(self, query: str) -> List[Pattern]:
        """搜索模式"""
        query_lower = query.lower()
        return [
            p for p in self._patterns.values()
            if (
                query_lower in p.name.lower()
                or query_lower in p.title.lower()
                or query_lower in p.description.lower()
                or any(query_lower in tag.lower() for tag in p.tags)
            )
        ]

    def get_best_practices(self, category: Optional[str] = None) -> List[Pattern]:
        """获取最佳实践"""
        if category:
            return [p for p in self.list_by_category(category) if p.type == "best_practice"]
        return self.list_by_type("best_practice")

    def get_anti_patterns(self, category: Optional[str] = None) -> List[Pattern]:
        """获取反模式"""
        if category:
            return [p for p in self.list_by_category(category) if p.type == "anti_pattern"]
        return self.list_by_type("anti_pattern")

    def get_categories(self) -> List[str]:
        """获取所有分类"""
        return sorted(self._categories.keys())

    def get_tags(self) -> List[str]:
        """获取所有标签"""
        tags = set()
        for pattern in self._patterns.values():
            tags.update(pattern.tags)
        return sorted(tags)

    # ========== 内置模式 ==========

    def load_builtin_patterns(self) -> None:
        """加载内置模式"""
        # 最佳实践：测试
        self.add(Pattern(
            id="testing-tdd",
            name="test_driven_development",
            type="best_practice",
            category="testing",
            title="测试驱动开发 (TDD)",
            description="在编写功能代码之前先编写测试",
            context="需要开发新功能或修复 bug 时",
            solution="红-绿-重构循环：1. 先写一个失败的测试 2. 编写最少代码使测试通过 3. 重构代码",
            examples=[
                "先写单元测试验证预期行为",
                "使用 pytest 或 unittest 框架",
            ],
            references=["https://en.wikipedia.org/wiki/Test-driven_development"],
            tags=["testing", "tdd", "quality"],
        ))

        # 最佳实践：安全
        self.add(Pattern(
            id="security-input-validation",
            name="input_validation",
            type="best_practice",
            category="security",
            title="输入验证",
            description="对所有用户输入进行验证和清理",
            context="处理来自外部的任何数据（表单、API、文件上传等）",
            solution="使用白名单验证、参数化查询、输出编码",
            examples=[
                "使用 prepared statements 防止 SQL 注入",
                "验证和清理 HTML 输入防止 XSS",
            ],
            references=["OWASP Top 10"],
            tags=["security", "validation", "owasp"],
        ))

        # 最佳实践：性能
        self.add(Pattern(
            id="performance-caching",
            name="caching",
            type="best_practice",
            category="performance",
            title="缓存",
            description="缓存昂贵的计算结果",
            context="频繁访问但不常变化的数据",
            solution="使用 Redis、Memcached 或内存缓存",
            examples=["缓存 API 响应", "缓存数据库查询结果"],
            references=[],
            tags=["performance", "caching", "optimization"],
        ))

        # 反模式：过度工程
        self.add(Pattern(
            id="anti-over-engineering",
            name="over_engineering",
            type="anti_pattern",
            category="design",
            title="过度工程",
            description="为未来可能不需要的需求添加复杂性",
            context="设计系统架构时",
            solution="YAGNI 原则：你不会需要它（You Aren't Gonna Need It）",
            consequences="代码难以维护、理解和测试；开发时间变长",
            examples=["在只有 3 个表时实现完整的 ORM 抽象", "为简单的脚本使用微服务架构"],
            references=["https://en.wikipedia.org/wiki/You_aren%27t_gonna_need_it"],
            tags=["design", "yagni", "simplicity"],
        ))

        # 反模式：复制粘贴编程
        self.add(Pattern(
            id="anti-copy-paste",
            name="copy_paste_programming",
            type="anti_pattern",
            category="code-quality",
            title="复制粘贴编程",
            description="通过复制粘贴现有代码来复用功能",
            context="需要实现类似功能时",
            solution="提取共享逻辑到函数或类；使用模板或宏；应用设计模式",
            consequences="代码重复、维护困难、bug 传播",
            examples=["复制粘贴处理逻辑只修改变量名", "复制粘贴配置文件"],
            references=["DRY Principle"],
            tags=["code-quality", "dry", "maintenance"],
        ))

        # 反模式：魔法数字
        self.add(Pattern(
            id="anti-magic-numbers",
            name="magic_numbers",
            type="anti_pattern",
            category="code-quality",
            title="魔法数字",
            description="代码中直接使用未命名的数字常量",
            context="需要使用特定数值时",
            solution="定义有意义的常量或配置项",
            consequences="代码难以理解、修改困难",
            examples=["if (status == 2)  // 2 是什么？", "sleep(86400)  // 一天？"],
            references=["https://en.wikipedia.org/wiki/Magic_number_(programming)"],
            tags=["code-quality", "readability", "constants"],
        ))

    # ========== 序列化 ==========

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "patterns": [p.to_dict() for p in self._patterns.values()],
            "categories": self._categories,
        }

    def to_json(self, path: Path) -> None:
        """导出为 JSON"""
        data = self.to_dict()
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PatternLibrary":
        """从字典创建"""
        library = cls()
        for pattern_data in data.get("patterns", []):
            library.add(Pattern.from_dict(pattern_data))
        return library

    @classmethod
    def from_json(cls, path: Path) -> "PatternLibrary":
        """从 JSON 加载"""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)

    def stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        type_counts = {"best_practice": 0, "anti_pattern": 0}
        for pattern in self._patterns.values():
            type_counts[pattern.type] = type_counts.get(pattern.type, 0) + 1

        return {
            "total_patterns": len(self._patterns),
            "type_counts": type_counts,
            "categories": len(self._categories),
            "tags": len(self.get_tags()),
        }


__all__ = [
    "Pattern",
    "PatternLibrary",
]
