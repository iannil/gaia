"""
Type stubs for gaia_templates
"""

from typing import Optional, Dict, Any, List
from pathlib import Path

class Template:
    """Template definition"""
    id: str
    name: str
    description: str
    content: str
    parameters: Dict[str, Any]
    category: str
    extends: Optional[str]

    def render(self, values: Dict[str, Any]) -> str: ...
    def validate_parameters(self, values: Dict[str, Any]) -> List[str]: ...
    def get_required_parameters(self) -> List[str]: ...

class TemplateEngine:
    """Template rendering engine"""
    _templates: Dict[str, Template]
    _built_in_path: Optional[Path]
    _custom_path: Optional[Path]

    def __init__(self) -> None: ...

    def set_paths(
        self,
        built_in: Optional[Path] = None,
        custom: Optional[Path] = None
    ) -> None: ...

    def register(self, template: Template) -> None: ...
    def get(self, template_id: str) -> Optional[Template]: ...
    def list_templates(self, category: Optional[str] = None) -> List[Template]: ...

    def render(
        self,
        template_id: str,
        values: Dict[str, Any]
    ) -> Optional[str]: ...
    def render_with_inheritance(
        self,
        template_id: str,
        values: Dict[str, Any]
    ) -> Optional[str]: ...

    def load_from_directory(self, directory: Path) -> None: ...
    def load_builtin_templates(self) -> None: ...
    def load_custom_templates(self, directory: Path) -> None: ...

__all__ = [
    "Template",
    "TemplateEngine",
]
