"""
GAIA Integration - Adapters

统一 API 适配器，提供与外部系统的集成。
"""

from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod
from dataclasses import dataclass
import requests
import json
from pathlib import Path


class Adapter(ABC):
    """适配器基类"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}

    @abstractmethod
    def connect(self) -> bool:
        """建立连接"""
        pass

    @abstractmethod
    def execute(self, action: str, **kwargs) -> Any:
        """执行操作"""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """断开连接"""
        pass


@dataclass
class GitHubConfig:
    """GitHub 配置"""
    token: str = ""
    owner: str = ""
    repo: str = ""
    api_base: str = "https://api.github.com"


class GitHubAdapter(Adapter):
    """GitHub 适配器"""

    def __init__(self, config: Optional[GitHubConfig] = None):
        super().__init__(config.__dict__ if config else {})
        self._session = None

    def connect(self) -> bool:
        """建立连接"""
        self._session = requests.Session()
        if self.config.get("token"):
            self._session.headers.update({
                "Authorization": f"token {self.config['token']}",
            })
        return True

    def execute(self, action: str, **kwargs) -> Any:
        """执行操作"""
        if action == "create_issue":
            return self._create_issue(**kwargs)
        elif action == "get_issues":
            return self._get_issues(**kwargs)
        elif action == "create_pr":
            return self._create_pr(**kwargs)
        elif action == "get_file":
            return self._get_file(**kwargs)
        else:
            raise ValueError(f"未知操作: {action}")

    def disconnect(self) -> None:
        """断开连接"""
        if self._session:
            self._session.close()
            self._session = None

    def _get_api_base(self) -> str:
        """获取 API 基础地址"""
        return self.config.get("api_base", "https://api.github.com")

    def _get_repo_path(self) -> str:
        """获取仓库路径"""
        owner = self.config.get("owner", "")
        repo = self.config.get("repo", "")
        return f"{owner}/{repo}"

    def _create_issue(
        self,
        title: str,
        body: str = "",
        labels: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """创建 Issue"""
        url = f"{self._get_api_base()}/repos/{self._get_repo_path()}/issues"
        data = {
            "title": title,
            "body": body,
            "labels": labels or [],
        }

        response = self._session.post(url, json=data)
        response.raise_for_status()
        return response.json()

    def _get_issues(
        self,
        state: str = "open",
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """获取 Issue 列表"""
        url = f"{self._get_api_base()}/repos/{self._get_repo_path()}/issues"
        params = {"state": state, "per_page": limit}

        response = self._session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def _create_pr(
        self,
        title: str,
        head: str,
        base: str = "main",
        body: str = "",
    ) -> Dict[str, Any]:
        """创建 Pull Request"""
        url = f"{self._get_api_base()}/repos/{self._get_repo_path()}/pulls"
        data = {
            "title": title,
            "head": head,
            "base": base,
            "body": body,
        }

        response = self._session.post(url, json=data)
        response.raise_for_status()
        return response.json()

    def _get_file(self, path: str, branch: str = "main") -> Optional[str]:
        """获取文件内容"""
        url = f"{self._get_api_base()}/repos/{self._get_repo_path()}/contents/{path}"
        params = {"ref": branch}

        response = self._session.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            # 如果是文件，解码内容
            if data.get("type") == "file":
                import base64
                content = base64.b64decode(data["content"]).decode("utf-8")
                return content
        return None


@dataclass
class NotionConfig:
    """Notion 配置"""
    token: str = ""
    database_id: str = ""
    api_base: str = "https://api.notion.com"


class NotionAdapter(Adapter):
    """Notion 适配器"""

    def __init__(self, config: Optional[NotionConfig] = None):
        super().__init__(config.__dict__ if config else {})
        self._session = None

    def connect(self) -> bool:
        """建立连接"""
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"Bearer {self.config.get('token', '')}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        })
        return True

    def execute(self, action: str, **kwargs) -> Any:
        """执行操作"""
        if action == "create_page":
            return self._create_page(**kwargs)
        elif action == "query_database":
            return self._query_database(**kwargs)
        elif action == "append_block":
            return self._append_block(**kwargs)
        else:
            raise ValueError(f"未知操作: {action}")

    def disconnect(self) -> None:
        """断开连接"""
        if self._session:
            self._session.close()
            self._session = None

    def _create_page(
        self,
        parent_id: str,
        title: str,
        content: Optional[str] = None,
    ) -> Dict[str, Any]:
        """创建页面"""
        url = f"{self.config.get('api_base', 'https://api.notion.com')}/v1/pages"

        blocks = [{
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": content or title}}]
            },
        }]

        data = {
            "parent": {"page_id": parent_id},
            "properties": {
                "title": {
                    "title": [{"text": {"content": title}}]
                }
            },
            "children": blocks if content else [],
        }

        response = self._session.post(url, json=data)
        response.raise_for_status()
        return response.json()

    def _query_database(
        self,
        database_id: Optional[str] = None,
        filter: Optional[Dict] = None,
    ) -> List[Dict[str, Any]]:
        """查询数据库"""
        db_id = database_id or self.config.get("database_id")
        url = f"{self.config.get('api_base', 'https://api.notion.com')}/v1/databases/{db_id}/query"

        data = {}
        if filter:
            data["filter"] = filter

        response = self._session.post(url, json=data)
        response.raise_for_status()
        return response.json().get("results", [])

    def _append_block(
        self,
        block_id: str,
        content: str,
        block_type: str = "paragraph",
    ) -> Dict[str, Any]:
        """追加内容块"""
        url = f"{self.config.get('api_base', 'https://api.notion.com')}/v1/blocks/{block_id}/children"

        data = {
            "children": [{
                "object": "block",
                "type": block_type,
                block_type: {
                    "rich_text": [{"type": "text", "text": {"content": content}}]
                },
            }]
        }

        response = self._session.patch(url, json=data)
        response.raise_for_status()
        return response.json()


class AdapterFactory:
    """适配器工厂"""

    _adapters: Dict[str, type] = {
        "github": GitHubAdapter,
        "notion": NotionAdapter,
    }

    @classmethod
    def register(cls, name: str, adapter_class: type) -> None:
        """注册适配器类型"""
        cls._adapters[name] = adapter_class

    @classmethod
    def create(cls, name: str, config: Optional[Dict[str, Any]] = None) -> Adapter:
        """创建适配器"""
        adapter_class = cls._adapters.get(name)
        if not adapter_class:
            raise ValueError(f"未知的适配器: {name}")

        if name == "github":
            if isinstance(config, dict):
                config = GitHubConfig(**config)
        elif name == "notion":
            if isinstance(config, dict):
                config = NotionConfig(**config)

        return adapter_class(config)

    @classmethod
    def list_adapters(cls) -> List[str]:
        """列出所有适配器"""
        return list(cls._adapters.keys())


class UnifiedAPI:
    """统一 API

    提供统一的接口访问所有适配器。
    """

    def __init__(self):
        self._adapters: Dict[str, Adapter] = {}

    def register_adapter(
        self,
        name: str,
        adapter: Adapter,
        auto_connect: bool = True,
    ) -> None:
        """注册适配器"""
        if auto_connect:
            adapter.connect()
        self._adapters[name] = adapter

    def unregister_adapter(self, name: str) -> bool:
        """取消注册适配器"""
        if name in self._adapters:
            self._adapters[name].disconnect()
            del self._adapters[name]
            return True
        return False

    def call(
        self,
        service: str,
        action: str,
        **kwargs,
    ) -> Any:
        """调用服务"""
        adapter = self._adapters.get(service)
        if not adapter:
            raise ValueError(f"服务未注册: {service}")

        return adapter.execute(action, **kwargs)

    def get_services(self) -> List[str]:
        """获取已注册的服务"""
        return list(self._adapters.keys())

    def disconnect_all(self) -> None:
        """断开所有连接"""
        for adapter in self._adapters.values():
            adapter.disconnect()
        self._adapters.clear()


__all__ = [
    "Adapter",
    "GitHubAdapter",
    "GitHubConfig",
    "NotionAdapter",
    "NotionConfig",
    "AdapterFactory",
    "UnifiedAPI",
]
