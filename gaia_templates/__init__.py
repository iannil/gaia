"""
GAIA Templates - Template System

GAIA 模板系统。

提供:
- Engine: 模板渲染引擎
- BuiltIn: 内置模板
- Custom: 自定义模板
"""

from .engine import Template, TemplateEngine

__version__ = "0.1.0"

__all__ = [
    "Template",
    "TemplateEngine",
]
