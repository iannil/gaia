"""
GAIA Skills - Registry

Skill 注册表，维护官方和社区 Skill 的索引。
"""

from typing import List, Optional, Dict, Any
import requests


class SkillSource:
    """Skill 来源定义"""

    def __init__(
        self,
        name: str,
        url: str,
        source_type: str,  # git, github, marketplace
        tier: str = "community",  # official, community, custom
    ):
        self.name = name
        self.url = url
        self.source_type = source_type
        self.tier = tier

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "url": self.url,
            "type": self.source_type,
            "tier": self.tier,
        }


class SkillRegistry:
    """Skill 注册表

    维护官方和社区 Skills 的索引。
    """

    # 官方 Skill 来源
    OFFICIAL_SOURCES = [
        SkillSource(
            name="anthropics/skills",
            url="https://github.com/anthropics/skills",
            source_type="github",
            tier="official",
        ),
        SkillSource(
            name="ComposioHQ",
            url="https://github.com/ComposioHQ/composio",
            source_type="github",
            tier="official",
        ),
    ]

    def __init__(self):
        self.sources: List[SkillSource] = []
        self._index: Dict[str, Dict[str, Any]] = {}

        # 加载官方来源
        self.sources.extend(self.OFFICIAL_SOURCES)

    def add_source(self, source: SkillSource) -> None:
        """添加 Skill 来源"""
        self.sources.append(source)

    def remove_source(self, name: str) -> bool:
        """移除 Skill 来源"""
        for i, source in enumerate(self.sources):
            if source.name == name:
                self.sources.pop(i)
                return True
        return False

    def get_sources(self, tier: Optional[str] = None) -> List[SkillSource]:
        """获取 Skill 来源"""
        if tier:
            return [s for s in self.sources if s.tier == tier]
        return self.sources.copy()

    def search_official_skills(self, query: str) -> List[Dict[str, Any]]:
        """搜索官方 Skills

        Args:
            query: 搜索关键词

        Returns:
            搜索结果列表
        """
        # 这里是简化实现，实际应该调用 GitHub API 或其他服务
        results = []

        for source in self.get_sources(tier="official"):
            if source.source_type == "github":
                # 简单的搜索模拟
                if query.lower() in source.name.lower():
                    results.append({
                        "name": source.name,
                        "url": source.url,
                        "source": "github",
                        "tier": "official",
                    })

        return results

    def get_skill_info(self, repo: str) -> Optional[Dict[str, Any]]:
        """获取 Skill 信息

        Args:
            repo: GitHub 仓库 (owner/repo)

        Returns:
            Skill 信息
        """
        # 简化实现，实际应该调用 GitHub API
        try:
            # 尝试从 GitHub API 获取
            api_url = f"https://api.github.com/repos/{repo}"
            response = requests.get(api_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    "name": data.get("name"),
                    "full_name": data.get("full_name"),
                    "description": data.get("description"),
                    "url": data.get("html_url"),
                    "stars": data.get("stargazers_count"),
                    "language": data.get("language"),
                    "updated_at": data.get("updated_at"),
                }
        except Exception:
            pass

        return None

    def list_official_skills(self) -> List[Dict[str, Any]]:
        """列出官方 Skills"""
        return [source.to_dict() for source in self.get_sources(tier="official")]

    def get_install_url(self, skill_name: str) -> Optional[str]:
        """获取 Skill 的安装 URL"""
        for source in self.sources:
            if source.name == skill_name:
                return source.url

        # 尝试作为 GitHub 仓库处理
        if "/" in skill_name:
            return f"https://github.com/{skill_name}"

        return None


__all__ = [
    "SkillSource",
    "SkillRegistry",
]
