"""
GAIA Skills - Repository

Skill 仓库管理，负责 Skill 的存储和索引。
"""

from pathlib import Path
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
import json
import fnmatch


@dataclass
class SkillMetadata:
    """Skill 元数据"""

    id: str
    name: str
    version: str
    description: str
    category: str
    tags: List[str] = field(default_factory=list)
    author: str = ""
    license: str = "MIT"
    created_at: str = ""
    updated_at: str = ""
    source: str = ""  # 来源 URL 或路径
    enabled: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "category": self.category,
            "tags": self.tags,
            "author": self.author,
            "license": self.license,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "source": self.source,
            "enabled": self.enabled,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SkillMetadata":
        return cls(**data)


class SkillRepository:
    """Skill 仓库"""

    def __init__(self, base_path: Optional[Path] = None):
        self.base_path = base_path or Path.home() / ".gaia" / "skills"
        self.base_path.mkdir(parents=True, exist_ok=True)

        self.index_path = self.base_path / "index.json"
        self._index: Dict[str, SkillMetadata] = {}
        self._load_index()

    def _load_index(self) -> None:
        """加载索引"""
        if self.index_path.exists():
            with open(self.index_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for skill_id, skill_data in data.items():
                    self._index[skill_id] = SkillMetadata.from_dict(skill_data)

    def _save_index(self) -> None:
        """保存索引"""
        data = {skill_id: meta.to_dict() for skill_id, meta in self._index.items()}
        with open(self.index_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def add(self, metadata: SkillMetadata) -> None:
        """添加 Skill"""
        metadata.created_at = metadata.created_at or datetime.now().isoformat()
        metadata.updated_at = datetime.now().isoformat()
        self._index[metadata.id] = metadata
        self._save_index()

    def get(self, skill_id: str) -> Optional[SkillMetadata]:
        """获取 Skill"""
        return self._index.get(skill_id)

    def remove(self, skill_id: str) -> bool:
        """移除 Skill"""
        if skill_id in self._index:
            del self._index[skill_id]
            self._save_index()
            return True
        return False

    def list_all(
        self,
        category: Optional[str] = None,
        tag: Optional[str] = None,
        enabled_only: bool = True,
    ) -> List[SkillMetadata]:
        """列出所有 Skills"""
        skills = list(self._index.values())

        if enabled_only:
            skills = [s for s in skills if s.enabled]

        if category:
            skills = [s for s in skills if s.category == category]

        if tag:
            skills = [s for s in skills if tag in s.tags]

        return skills

    def search(self, query: str) -> List[SkillMetadata]:
        """搜索 Skills"""
        query_lower = query.lower()
        results = []

        for skill in self._index.values():
            # 搜索名称、描述、标签
            if (
                query_lower in skill.name.lower()
                or query_lower in skill.description.lower()
                or any(query_lower in tag.lower() for tag in skill.tags)
            ):
                results.append(skill)

        return results

    def get_by_path(self, path: Path) -> Optional[SkillMetadata]:
        """通过路径获取 Skill"""
        for skill in self._index.values():
            if skill.source and path in Path(skill.source).parents:
                return skill
        return None

    def update(self, skill_id: str, **kwargs) -> bool:
        """更新 Skill"""
        skill = self._index.get(skill_id)
        if not skill:
            return False

        for key, value in kwargs.items():
            if hasattr(skill, key):
                setattr(skill, key, value)

        skill.updated_at = datetime.now().isoformat()
        self._save_index()
        return True

    def enable(self, skill_id: str) -> bool:
        """启用 Skill"""
        return self.update(skill_id, enabled=True)

    def disable(self, skill_id: str) -> bool:
        """禁用 Skill"""
        return self.update(skill_id, enabled=False)

    def get_categories(self) -> List[str]:
        """获取所有分类"""
        categories = set(s.category for s in self._index.values())
        return sorted(categories)

    def get_tags(self) -> List[str]:
        """获取所有标签"""
        tags = set()
        for skill in self._index.values():
            tags.update(skill.tags)
        return sorted(tags)

    def count(self, enabled_only: bool = True) -> int:
        """统计数量"""
        if enabled_only:
            return sum(1 for s in self._index.values() if s.enabled)
        return len(self._index)


class LocalSkillStore:
    """本地 Skill 存储

    管理本地文件系统中的 Skills。
    """

    def __init__(self, base_path: Optional[Path] = None):
        self.base_path = base_path or Path.home() / ".gaia" / "skills" / "local"
        self.base_path.mkdir(parents=True, exist_ok=True)

    def get_skill_path(self, skill_id: str) -> Path:
        """获取 Skill 目录路径"""
        return self.base_path / skill_id

    def skill_exists(self, skill_id: str) -> bool:
        """检查 Skill 是否存在"""
        return self.get_skill_path(skill_id).exists()

    def create_skill_directory(self, skill_id: str) -> Path:
        """创建 Skill 目录"""
        path = self.get_skill_path(skill_id)
        path.mkdir(parents=True, exist_ok=True)
        return path

    def get_skill_files(self, skill_id: str) -> List[Path]:
        """获取 Skill 下的所有文件"""
        skill_path = self.get_skill_path(skill_id)
        if not skill_path.exists():
            return []

        return list(skill_path.rglob("*"))

    def read_skill_manifest(self, skill_id: str) -> Optional[Dict[str, Any]]:
        """读取 Skill 清单文件"""
        manifest_path = self.get_skill_path(skill_id) / "skill.json"
        if not manifest_path.exists():
            return None

        with open(manifest_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def write_skill_manifest(self, skill_id: str, manifest: Dict[str, Any]) -> None:
        """写入 Skill 清单文件"""
        skill_path = self.create_skill_directory(skill_id)
        manifest_path = skill_path / "skill.json"

        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)


__all__ = [
    "SkillMetadata",
    "SkillRepository",
    "LocalSkillStore",
]
