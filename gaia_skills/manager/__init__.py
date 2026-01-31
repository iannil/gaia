"""
GAIA Skills - Manager

Skill 管理器，提供 Skill 的安装、更新、卸载等管理功能。
"""

from pathlib import Path
from typing import List, Optional, Dict, Any
import shutil
import subprocess
from ..repository import SkillRepository, LocalSkillStore, SkillMetadata


class SkillManager:
    """Skill 管理器

    负责 Skill 的生命周期管理。
    """

    def __init__(
        self,
        repository: Optional[SkillRepository] = None,
        store: Optional[LocalSkillStore] = None,
    ):
        self.repository = repository or SkillRepository()
        self.store = store or LocalSkillStore()

    # ========== 安装 ==========

    def install_from_git(self, url: str, skill_id: Optional[str] = None) -> tuple[bool, str]:
        """从 Git 仓库安装 Skill

        Args:
            url: Git 仓库 URL
            skill_id: 可选的 Skill ID

        Returns:
            (成功, 消息)
        """
        # 从 URL 提取 skill_id
        if not skill_id:
            skill_id = url.rstrip("/").split("/")[-1].replace(".git", "")

        # 检查是否已安装
        if self.repository.get(skill_id):
            return False, f"Skill '{skill_id}' 已安装"

        try:
            # 克隆仓库
            skill_path = self.store.get_skill_path(skill_id)
            subprocess.run(
                ["git", "clone", url, str(skill_path)],
                check=True,
                capture_output=True,
            )

            # 读取 manifest
            manifest = self.store.read_skill_manifest(skill_id)
            if manifest:
                metadata = SkillMetadata(
                    id=skill_id,
                    name=manifest.get("name", skill_id),
                    version=manifest.get("version", "0.1.0"),
                    description=manifest.get("description", ""),
                    category=manifest.get("category", "other"),
                    tags=manifest.get("tags", []),
                    author=manifest.get("author", ""),
                    license=manifest.get("license", "MIT"),
                    source=url,
                )
                self.repository.add(metadata)

            return True, f"Skill '{skill_id}' 安装成功"

        except subprocess.CalledProcessError as e:
            return False, f"克隆失败: {e.stderr.decode()}"
        except Exception as e:
            return False, f"安装失败: {e}"

    def install_from_local(self, path: Path, skill_id: str) -> tuple[bool, str]:
        """从本地路径安装 Skill

        Args:
            path: 本地路径
            skill_id: Skill ID

        Returns:
            (成功, 消息)
        """
        if not path.exists():
            return False, f"路径不存在: {path}"

        # 检查是否已安装
        if self.repository.get(skill_id):
            return False, f"Skill '{skill_id}' 已安装"

        try:
            # 复制到 Skill 目录
            skill_path = self.store.get_skill_path(skill_id)
            if path.is_dir():
                shutil.copytree(path, skill_path)
            else:
                shutil.copy2(path, skill_path)

            # 读取 manifest
            manifest = self.store.read_skill_manifest(skill_id)
            if manifest:
                metadata = SkillMetadata(
                    id=skill_id,
                    name=manifest.get("name", skill_id),
                    version=manifest.get("version", "0.1.0"),
                    description=manifest.get("description", ""),
                    category=manifest.get("category", "other"),
                    tags=manifest.get("tags", []),
                    author=manifest.get("author", ""),
                    license=manifest.get("license", "MIT"),
                    source=str(path),
                )
                self.repository.add(metadata)

            return True, f"Skill '{skill_id}' 安装成功"

        except Exception as e:
            return False, f"安装失败: {e}"

    def install_from_github(
        self, repo: str, skill_id: Optional[str] = None
    ) -> tuple[bool, str]:
        """从 GitHub 仓库安装 Skill

        Args:
            repo: 格式为 "owner/repo" 或完整 URL
            skill_id: 可选的 Skill ID

        Returns:
            (成功, 消息)
        """
        # 转换为完整 URL
        if not repo.startswith("http"):
            if "/" in repo:
                owner, name = repo.split("/", 1)
                url = f"https://github.com/{owner}/{name}.git"
            else:
                return False, "无效的仓库格式，应为 'owner/repo'"
        else:
            url = repo

        return self.install_from_git(url, skill_id)

    # ========== 更新 ==========

    def update(self, skill_id: str) -> tuple[bool, str]:
        """更新 Skill

        Args:
            skill_id: Skill ID

        Returns:
            (成功, 消息)
        """
        skill = self.repository.get(skill_id)
        if not skill:
            return False, f"Skill '{skill_id}' 未安装"

        skill_path = self.store.get_skill_path(skill_id)

        # 检查是否为 Git 仓库
        git_dir = skill_path / ".git"
        if not git_dir.exists():
            return False, f"Skill '{skill_id}' 不是 Git 仓库，无法更新"

        try:
            # 拉取更新
            subprocess.run(
                ["git", "pull"],
                cwd=skill_path,
                check=True,
                capture_output=True,
            )

            # 更新时间戳
            self.repository.update(skill_id)
            return True, f"Skill '{skill_id}' 更新成功"

        except subprocess.CalledProcessError as e:
            return False, f"更新失败: {e.stderr.decode()}"

    def update_all(self) -> List[tuple[bool, str]]:
        """更新所有 Skills

        Returns:
            [(成功, 消息), ...]
        """
        results = []
        for skill in self.repository.list_all():
            result = self.update(skill.id)
            results.append(result)
        return results

    # ========== 卸载 ==========

    def uninstall(self, skill_id: str, keep_files: bool = False) -> tuple[bool, str]:
        """卸载 Skill

        Args:
            skill_id: Skill ID
            keep_files: 是否保留文件

        Returns:
            (成功, 消息)
        """
        skill = self.repository.get(skill_id)
        if not skill:
            return False, f"Skill '{skill_id}' 未安装"

        try:
            # 删除文件
            if not keep_files:
                skill_path = self.store.get_skill_path(skill_id)
                if skill_path.exists():
                    shutil.rmtree(skill_path)

            # 从索引移除
            self.repository.remove(skill_id)

            return True, f"Skill '{skill_id}' 卸载成功"

        except Exception as e:
            return False, f"卸载失败: {e}"

    # ========== 查询 ==========

    def list_skills(
        self,
        category: Optional[str] = None,
        tag: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """列出 Skills

        Args:
            category: 分类筛选
            tag: 标签筛选

        Returns:
            Skill 信息列表
        """
        skills = self.repository.list_all(category=category, tag=tag)
        return [skill.to_dict() for skill in skills]

    def get_skill_info(self, skill_id: str) -> Optional[Dict[str, Any]]:
        """获取 Skill 信息

        Args:
            skill_id: Skill ID

        Returns:
            Skill 信息
        """
        skill = self.repository.get(skill_id)
        if skill:
            return skill.to_dict()
        return None

    def search_skills(self, query: str) -> List[Dict[str, Any]]:
        """搜索 Skills

        Args:
            query: 搜索关键词

        Returns:
            Skill 信息列表
        """
        skills = self.repository.search(query)
        return [skill.to_dict() for skill in skills]

    def get_categories(self) -> List[str]:
        """获取所有分类"""
        return self.repository.get_categories()

    def get_tags(self) -> List[str]:
        """获取所有标签"""
        return self.repository.get_tags()

    # ========== 状态管理 ==========

    def enable(self, skill_id: str) -> tuple[bool, str]:
        """启用 Skill"""
        if self.repository.enable(skill_id):
            return True, f"Skill '{skill_id}' 已启用"
        return False, f"Skill '{skill_id}' 不存在"

    def disable(self, skill_id: str) -> tuple[bool, str]:
        """禁用 Skill"""
        if self.repository.disable(skill_id):
            return True, f"Skill '{skill_id}' 已禁用"
        return False, f"Skill '{skill_id}' 不存在"

    def is_installed(self, skill_id: str) -> bool:
        """检查 Skill 是否已安装"""
        return self.repository.get(skill_id) is not None

    def get_status(self) -> Dict[str, Any]:
        """获取 Skill 管理器状态"""
        return {
            "total": self.repository.count(enabled_only=False),
            "enabled": self.repository.count(enabled_only=True),
            "categories": self.get_categories(),
            "tags": self.get_tags(),
        }


__all__ = ["SkillManager"]
