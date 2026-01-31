"""
GAIA Skills - Skill Management System

GAIA Skill 管理系统。

提供:
- Repository: Skill 仓库和索引
- Manager: Skill 安装、更新、卸载
- Evolution: 演化记录管理
- Registry: Skill 注册表
"""

from .repository import (
    SkillMetadata,
    SkillRepository,
    LocalSkillStore,
)
from .manager import SkillManager
from .evolution import (
    EvolutionRecord,
    EvolutionManager,
)
from .registry import (
    SkillSource,
    SkillRegistry,
)

__version__ = "0.1.0"

__all__ = [
    # Repository
    "SkillMetadata",
    "SkillRepository",
    "LocalSkillStore",
    # Manager
    "SkillManager",
    # Evolution
    "EvolutionRecord",
    "EvolutionManager",
    # Registry
    "SkillSource",
    "SkillRegistry",
]
