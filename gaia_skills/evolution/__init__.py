"""
GAIA Skills - Evolution Manager

演化记录管理器，负责记录和维护 evolution.json。
"""

from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime
import json


class EvolutionRecord:
    """演化记录"""

    def __init__(
        self,
        skill_id: str,
        skill_name: str,
        version: str = "0.1.0",
    ):
        self.skill_id = skill_id
        self.skill_name = skill_name
        self.version = version
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()

        # 核心数据
        self.description: str = ""
        self.category: str = "other"
        self.tags: List[str] = []

        # 演化数据
        self.effective_parameters: Dict[str, Any] = {}
        self.success_patterns: List[Dict[str, Any]] = []
        self.anti_patterns: List[Dict[str, Any]] = []
        self.usage_history: List[Dict[str, Any]] = []

        # 元数据
        self.dependencies: List[Dict[str, str]] = []
        self.quality_metrics: Dict[str, float] = {}
        self.maintenance_status: str = "active"
        self.metadata: Dict[str, Any] = {}

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "skill_id": self.skill_id,
            "skill_name": self.skill_name,
            "version": self.version,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "description": self.description,
            "category": self.category,
            "tags": self.tags,
            "effective_parameters": self.effective_parameters,
            "success_patterns": self.success_patterns,
            "anti_patterns": self.anti_patterns,
            "usage_history": self.usage_history,
            "dependencies": self.dependencies,
            "quality_metrics": self.quality_metrics,
            "maintenance_status": self.maintenance_status,
            "metadata": self.metadata,
        }

    def update(self, **kwargs) -> None:
        """更新记录"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now().isoformat()

    def record_parameter(
        self,
        name: str,
        value: Any,
        use_case: str,
        performance_notes: str = "",
    ) -> None:
        """记录有效参数"""
        self.effective_parameters[name] = {
            "value": value,
            "tested_at": datetime.now().isoformat(),
            "use_case": use_case,
            "performance_notes": performance_notes,
        }
        self.updated_at = datetime.now().isoformat()

    def record_success_pattern(
        self,
        pattern: str,
        context: str,
        outcome: str,
    ) -> None:
        """记录成功模式"""
        self.success_patterns.append({
            "pattern": pattern,
            "context": context,
            "outcome": outcome,
            "documented_at": datetime.now().isoformat(),
        })
        self.updated_at = datetime.now().isoformat()

    def record_anti_pattern(
        self,
        pattern: str,
        why_fails: str,
        alternative: str,
    ) -> None:
        """记录反模式"""
        self.anti_patterns.append({
            "pattern": pattern,
            "why_fails": why_fails,
            "alternative": alternative,
        })
        self.updated_at = datetime.now().isoformat()

    def record_usage(
        self,
        task: str,
        parameters: Dict[str, Any],
        outcome: str,
        notes: str = "",
    ) -> None:
        """记录使用历史"""
        self.usage_history.append({
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "parameters": parameters,
            "outcome": outcome,
            "notes": notes,
        })
        self.updated_at = datetime.now().isoformat()


class EvolutionManager:
    """演化记录管理器

    负责 evolution.json 的读写和维护。
    """

    def __init__(self, base_path: Optional[Path] = None):
        self.base_path = base_path or Path.cwd()
        self.evolution_file = self.base_path / "evolution.json"

    def exists(self) -> bool:
        """检查演化记录是否存在"""
        return self.evolution_file.exists()

    def load(self) -> Optional[Dict[str, Any]]:
        """加载演化记录"""
        if not self.exists():
            return None

        try:
            with open(self.evolution_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None

    def save(self, data: Dict[str, Any]) -> None:
        """保存演化记录"""
        data["updated_at"] = datetime.now().isoformat()

        with open(self.evolution_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def create(
        self,
        skill_id: str,
        skill_name: str,
        **kwargs,
    ) -> EvolutionRecord:
        """创建新的演化记录"""
        record = EvolutionRecord(skill_id, skill_name, **kwargs)
        return record

    def get_record(self, skill_id: str) -> Optional[EvolutionRecord]:
        """获取 Skill 的演化记录"""
        data = self.load()
        if not data:
            return None

        skills = data.get("skills", {})
        if skill_id not in skills:
            return None

        skill_data = skills[skill_id]
        record = EvolutionRecord(
            skill_id=skill_data.get("skill_id", skill_id),
            skill_name=skill_data.get("skill_name", ""),
            version=skill_data.get("version", "0.1.0"),
        )
        record.update(**skill_data)
        return record

    def save_record(self, record: EvolutionRecord) -> None:
        """保存演化记录"""
        data = self.load() or {"version": "1.0", "skills": {}}

        if "skills" not in data:
            data["skills"] = {}

        data["skills"][record.skill_id] = record.to_dict()
        self.save(data)

    def update_record(self, skill_id: str, **kwargs) -> bool:
        """更新演化记录"""
        record = self.get_record(skill_id)
        if not record:
            return False

        record.update(**kwargs)
        self.save_record(record)
        return True

    def add_parameter(
        self,
        skill_id: str,
        name: str,
        value: Any,
        use_case: str,
        performance_notes: str = "",
    ) -> bool:
        """添加有效参数"""
        record = self.get_record(skill_id)
        if not record:
            return False

        record.record_parameter(name, value, use_case, performance_notes)
        self.save_record(record)
        return True

    def add_success_pattern(
        self,
        skill_id: str,
        pattern: str,
        context: str,
        outcome: str,
    ) -> bool:
        """添加成功模式"""
        record = self.get_record(skill_id)
        if not record:
            return False

        record.record_success_pattern(pattern, context, outcome)
        self.save_record(record)
        return True

    def add_anti_pattern(
        self,
        skill_id: str,
        pattern: str,
        why_fails: str,
        alternative: str,
    ) -> bool:
        """添加反模式"""
        record = self.get_record(skill_id)
        if not record:
            return False

        record.record_anti_pattern(pattern, why_fails, alternative)
        self.save_record(record)
        return True

    def add_usage(
        self,
        skill_id: str,
        task: str,
        parameters: Dict[str, Any],
        outcome: str,
        notes: str = "",
    ) -> bool:
        """添加使用记录"""
        record = self.get_record(skill_id)
        if not record:
            return False

        record.record_usage(task, parameters, outcome, notes)
        self.save_record(record)
        return True

    def get_all_skills(self) -> List[str]:
        """获取所有有演化记录的 Skill ID"""
        data = self.load()
        if not data:
            return []

        return list(data.get("skills", {}).keys())

    def get_summary(self) -> Dict[str, Any]:
        """获取演化记录摘要"""
        data = self.load() or {}

        skills = data.get("skills", {})
        return {
            "total_skills": len(skills),
            "updated_at": data.get("updated_at"),
            "skills": list(skills.keys()),
        }


__all__ = [
    "EvolutionRecord",
    "EvolutionManager",
]
