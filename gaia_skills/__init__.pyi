"""
Type stubs for gaia_skills
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass

class SkillMetadata:
    """Skill metadata"""
    id: str
    name: str
    version: str
    description: str
    author: str
    license: str
    tags: List[str]
    dependencies: List[str]
    homepage: Optional[str]
    repository: Optional[str]
    documentation: Optional[str]
    installed_at: datetime
    last_updated: datetime
    enabled: bool

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SkillMetadata": ...
    def to_dict(self) -> Dict[str, Any]: ...

class LocalSkillStore:
    """Local skill storage"""
    base_path: Path
    skills_dir: Path
    metadata_dir: Path

    def __init__(self, base_path: Optional[Path] = None) -> None: ...

    def get_skill_path(self, skill_id: str) -> Path: ...
    def get_metadata_path(self, skill_id: str) -> Path: ...
    def skill_exists(self, skill_id: str) -> bool: ...
    def list_skills(self) -> List[str]: ...

class SkillRepository:
    """Skill repository"""
    store: LocalSkillStore

    def __init__(self, store: Optional[LocalSkillStore] = None) -> None: ...

    def register(self, metadata: SkillMetadata) -> None: ...
    def get(self, skill_id: str) -> Optional[SkillMetadata]: ...
    def remove(self, skill_id: str) -> bool: ...
    def list_all(self) -> List[SkillMetadata]: ...
    def search(self, query: str) -> List[SkillMetadata]: ...

    def find_by_tag(self, tag: str) -> List[SkillMetadata]: ...
    def find_by_author(self, author: str) -> List[SkillMetadata]: ...

class SkillManager:
    """Skill manager"""
    repository: SkillRepository
    store: LocalSkillStore

    def __init__(self, base_path: Optional[Path] = None) -> None: ...

    def install_from_git(
        self,
        url: str,
        skill_id: Optional[str] = None,
        branch: str = ...
    ) -> SkillMetadata: ...
    def install_from_github(
        self,
        repo: str,
        skill_id: Optional[str] = None,
        branch: str = ...
    ) -> SkillMetadata: ...
    def install_from_local(self, path: Path) -> SkillMetadata: ...

    def uninstall(self, skill_id: str) -> bool: ...
    def update(self, skill_id: str) -> SkillMetadata: ...
    def enable(self, skill_id: str) -> bool: ...
    def disable(self, skill_id: str) -> bool: ...

    def get_status(self, skill_id: str) -> Dict[str, Any]: ...

class EvolutionRecord:
    """Skill evolution record"""
    skill_id: str
    skill_name: str
    version: str
    created_at: str
    updated_at: str

    description: str
    category: str
    tags: List[str]

    effective_parameters: Dict[str, Any]
    success_patterns: List[Dict[str, Any]]
    anti_patterns: List[Dict[str, Any]]
    usage_history: List[Dict[str, Any]]

    dependencies: List[Dict[str, str]]
    quality_metrics: Dict[str, float]
    maintenance_status: str
    metadata: Dict[str, Any]

    def update(self, **kwargs) -> None: ...

    def record_parameter(
        self,
        name: str,
        value: Any,
        use_case: str,
        performance_notes: str = ...
    ) -> None: ...
    def record_success_pattern(
        self,
        pattern: str,
        context: str,
        outcome: str
    ) -> None: ...
    def record_anti_pattern(
        self,
        pattern: str,
        why_fails: str,
        alternative: str
    ) -> None: ...
    def record_usage(
        self,
        task: str,
        parameters: Dict[str, Any],
        outcome: str,
        notes: str = ...
    ) -> None: ...

    def to_dict(self) -> Dict[str, Any]: ...

class EvolutionManager:
    """Evolution record manager"""
    base_path: Path
    evolution_file: Path

    def __init__(self, base_path: Optional[Path] = None) -> None: ...

    def exists(self) -> bool: ...
    def load(self) -> Optional[Dict[str, Any]]: ...
    def save(self, data: Dict[str, Any]) -> None: ...

    def create(
        self,
        skill_id: str,
        skill_name: str,
        **kwargs
    ) -> EvolutionRecord: ...
    def get_record(self, skill_id: str) -> Optional[EvolutionRecord]: ...
    def save_record(self, record: EvolutionRecord) -> None: ...
    def list_records(self) -> List[EvolutionRecord]: ...

__all__ = [
    "SkillMetadata",
    "LocalSkillStore",
    "SkillRepository",
    "SkillManager",
    "EvolutionRecord",
    "EvolutionManager",
]
