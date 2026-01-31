"""
GAIA Templates - Engine

模板引擎，支持参数化模板渲染。
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import re
import json
from string import Template as StringTemplate
from dataclasses import dataclass


@dataclass
class Template:
    """模板定义"""

    id: str
    name: str
    description: str
    content: str
    parameters: Dict[str, Any]  # 参数定义：类型、默认值、描述
    category: str = "general"
    extends: Optional[str] = None  # 继承的模板 ID

    def render(self, values: Dict[str, Any]) -> str:
        """渲染模板"""
        # 合并默认值和传入值
        params = {}
        for param_name, param_def in self.parameters.items():
            default = param_def.get("default", "")
            params[param_name] = values.get(param_name, default)

        # 使用字符串模板
        template = StringTemplate(self.content)
        return template.safe_substitute(params)

    def validate_parameters(self, values: Dict[str, Any]) -> List[str]:
        """验证参数"""
        errors = []

        for param_name, param_def in self.parameters.items():
            # 检查必填参数
            if param_def.get("required", False) and param_name not in values:
                errors.append(f"缺少必填参数: {param_name}")
                continue

            # 类型检查
            if param_name in values:
                expected_type = param_def.get("type", "string")
                value = values[param_name]

                if expected_type == "string" and not isinstance(value, str):
                    errors.append(f"参数 {param_name} 应为字符串")
                elif expected_type == "number" and not isinstance(value, (int, float)):
                    errors.append(f"参数 {param_name} 应为数字")
                elif expected_type == "boolean" and not isinstance(value, bool):
                    errors.append(f"参数 {param_name} 应为布尔值")

        return errors


class TemplateEngine:
    """模板引擎

    支持模板的加载、渲染、继承和组合。
    """

    def __init__(self):
        self._templates: Dict[str, Template] = {}
        self._built_in_path: Optional[Path] = None
        self._custom_path: Optional[Path] = None

    def set_paths(
        self,
        built_in: Optional[Path] = None,
        custom: Optional[Path] = None,
    ) -> None:
        """设置模板路径"""
        self._built_in_path = built_in
        self._custom_path = custom

    def register(self, template: Template) -> None:
        """注册模板"""
        self._templates[template.id] = template

    def get(self, template_id: str) -> Optional[Template]:
        """获取模板"""
        return self._templates.get(template_id)

    def list_templates(
        self,
        category: Optional[str] = None,
    ) -> List[Template]:
        """列出模板"""
        templates = list(self._templates.values())

        if category:
            templates = [t for t in templates if t.category == category]

        return templates

    def render(
        self,
        template_id: str,
        values: Dict[str, Any],
    ) -> Optional[str]:
        """渲染模板"""
        template = self.get(template_id)
        if not template:
            return None

        return template.render(values)

    def render_with_inheritance(
        self,
        template_id: str,
        values: Dict[str, Any],
    ) -> Optional[str]:
        """渲染模板（支持继承）"""
        template = self.get(template_id)
        if not template:
            return None

        # 处理继承
        if template.extends:
            parent = self.get(template.extends)
            if parent:
                # 先渲染父模板
                base_content = parent.render(values)
                # 子模板可以覆盖父模板的内容
                # 这里简化处理：直接返回子模板渲染结果
                return template.render(values)

        return template.render(values)

    def load_from_directory(
        self,
        directory: Path,
        category: str = "custom",
    ) -> int:
        """从目录加载模板

        目录结构:
        templates/
        ├── template_id/
        │   ├── template.md     # 模板内容
        │   └── meta.json       # 模板元数据
        """
        count = 0

        for template_dir in directory.iterdir():
            if not template_dir.is_dir():
                continue

            template_id = template_dir.name
            meta_file = template_dir / "meta.json"
            content_file = template_dir / "template.md"

            if not meta_file.exists() or not content_file.exists():
                continue

            try:
                # 读取元数据
                with open(meta_file, "r", encoding="utf-8") as f:
                    meta = json.load(f)

                # 读取内容
                with open(content_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # 创建模板
                template = Template(
                    id=template_id,
                    name=meta.get("name", template_id),
                    description=meta.get("description", ""),
                    content=content,
                    parameters=meta.get("parameters", {}),
                    category=meta.get("category", category),
                    extends=meta.get("extends"),
                )

                self.register(template)
                count += 1

            except Exception:
                continue

        return count

    def create_template(
        self,
        template_id: str,
        name: str,
        content: str,
        parameters: Optional[Dict[str, Any]] = None,
        description: str = "",
        category: str = "custom",
    ) -> Template:
        """创建新模板"""
        template = Template(
            id=template_id,
            name=name,
            description=description,
            content=content,
            parameters=parameters or {},
            category=category,
        )
        self.register(template)
        return template

    def validate_template(
        self,
        template_id: str,
        values: Dict[str, Any],
    ) -> List[str]:
        """验证模板参数"""
        template = self.get(template_id)
        if not template:
            return [f"模板不存在: {template_id}"]

        return template.validate_parameters(values)

    # ========== 内置模板 ==========

    def load_builtin_templates(self) -> None:
        """加载内置模板"""
        # Phase 启动模板
        self.register(Template(
            id="phase-startup",
            name="Phase 启动模板",
            description="GAIA 各阶段启动检查清单",
            category="gaia",
            parameters={
                "phase": {"type": "string", "default": "G", "description": "当前阶段"},
                "context": {"type": "string", "default": "", "description": "上下文信息"},
            },
            content="""# Phase $phase 启动检查清单

**上下文**: $context

## 前置条件检查
- [ ] 前一阶段已完成
- [ ] 上下文已传递
- [ ] 目标明确

## 本阶段目标
1.
2.
3.

## 预期输出
- 输出 1:
- 输出 2:

## 完成标准
- [ ] 标准 1
- [ ] 标准 2
""",
        ))

        # Skill 定义模板
        self.register(Template(
            id="skill-definition",
            name="Skill 定义模板",
            description="定义新 Skill 的文档模板",
            category="skill",
            parameters={
                "skill_name": {"type": "string", "description": "Skill 名称"},
                "description": {"type": "string", "description": "Skill 描述"},
                "author": {"type": "string", "default": "", "description": "作者"},
            },
            content="""# $skill_name

## 描述
$description

## 使用方式

### 安装
\`\`\`bash
# 安装命令
\`\`\`

### 配置
\`\`\`yaml
# 配置示例
\`\`\`

### 使用示例
\`\`\`bash
# 基本用法
\`\`\`

## 参数说明

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| | | | |

## 演化记录

### 有效参数
- 参数名: 值 (使用场景)

### 成功技巧
1. 技巧 1
2. 技巧 2

### 常见问题
| 问题 | 解决方案 |
|------|----------|
| | |

---
作者: $author
创建时间: $timestamp
""",
        ))

        # PRD 模板
        self.register(Template(
            id="prd",
            name="PRD 模板",
            description="产品需求文档模板",
            category="document",
            parameters={
                "product_name": {"type": "string", "description": "产品名称"},
                "version": {"type": "string", "default": "1.0", "description": "版本"},
            },
            content="""# $product_name PRD

## 1. 产品概述

### 1.1 产品背景
$background

### 1.2 目标用户
- 用户类型 1
- 用户类型 2

### 1.3 核心价值
- 价值点 1
- 价值点 2

## 2. 功能需求

### 2.1 核心功能 (P0)
- [ ] 功能 1
- [ ] 功能 2

### 2.2 重要功能 (P1)
- [ ] 功能 3

### 2.3 可选功能 (P2)
- [ ] 功能 4

## 3. 非功能需求

### 3.1 性能要求
- 响应时间 < 200ms
- 支持 1000 并发

### 3.2 安全要求
- 用户数据加密
- 权限控制

### 3.3 可用性要求
- 99.9% 可用性

## 4. 里程碑

| 里程碑 | 交付时间 | 交付物 |
|--------|----------|--------|
| M1 | | |
| M2 | | |

---
文档版本: $version
更新时间: $timestamp
""",
        ))

        # 复盘模板
        self.register(Template(
            id="retrospective",
            name="复盘模板",
            description="项目复盘文档模板",
            category="document",
            parameters={
                "project_name": {"type": "string", "description": "项目名称"},
                "sprint": {"type": "string", "default": "", "description": "迭代/版本"},
            },
            content="""# $project_name 复盘报告

## 基本信息

**项目**: $project_name
**时间**: $sprint
**日期**: $date

## 目标回顾

### 原定目标
1.
2.
3.

### 完成情况
- 目标 1: ✅ / ❌
- 目标 2: ✅ / ❌
- 目标 3: ✅ / ❌

## 做得好的

1.
2.
3.

## 需要改进的

1.
2.
3.

## 行动计划

| 行动项 | 负责人 | 完成时间 |
|--------|--------|----------|
| | | |

## 其他讨论

---
记录人: $author
""",
        ))


__all__ = [
    "Template",
    "TemplateEngine",
]
