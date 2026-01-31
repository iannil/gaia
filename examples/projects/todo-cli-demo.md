# GAIA 示例项目

这是一个使用 GAIA 框架的示例项目，演示如何用框架解决实际问题。

---

## 项目概述

**项目名称**: todo-cli-demo
**问题陈述**: 需要开发一个简单的命令行待办事项应用
**目标**: 演示 GAIA 框架的完整使用流程

---

## Phase G: 生成

### 问题分析

我们需要一个命令行待办事项应用，核心功能：
- 添加任务
- 列出任务
- 标记完成
- 删除任务

### 解决方案路径

**选择**: `search-skill` (市场优先)

搜索现有类似项目：
- `todo-txt` 格式：成熟的纯文本待办格式
- `topydo`：Python CLI todo 应用
- Python `click` 库：推荐的 CLI 框架

### 解决方案大纲

使用 Python + Click 实现 todo-txt 格式的 CLI 工具。

---

## Phase A: 分析

### MVP 定义

**P0 (核心功能 - 必须完成)**:
- [ ] 添加任务
- [ ] 列出任务
- [ ] 完成任务

**P1 (重要功能 - 应该完成)**:
- [ ] 删除任务
- [ ] 优先级标记
- [ ] 过滤任务

**P2 (可选功能 - 有时间再做)**:
- [ ] 任务编辑
- [ ] 子任务
- [ ] 归档

### 技术选型

- **语言**: Python 3.10+
- **CLI 框架**: Click
- **数据存储**: 纯文本文件 (todo.txt)
- **测试**: pytest

---

## Phase I: 实现

### 项目结构

```
todo-cli/
├── todo_cli/
│   ├── __init__.py
│   ├── cli.py          # CLI 入口
│   ├── manager.py       # 任务管理
│   └── storage.py       # 文件存储
├── tests/
├── pyproject.toml
└── README.md
```

### 核心代码

**cli.py**:
```python
import click
from .manager import TodoManager

@click.group()
def cli():
    """Todo CLI - 简单的命令行待办事项"""
    pass

@cli.command()
@click.argument('task')
def add(task):
    """添加任务"""
    manager = TodoManager()
    manager.add(task)
    click.echo(f"✓ 添加任务: {task}")

@cli.command()
def list():
    """列出所有任务"""
    manager = TodoManager()
    tasks = manager.list_all()
    for i, task in enumerate(tasks, 1):
        click.echo(f"{i}. [{task.status}] {task.text}")

@cli.command()
@click.argument('number', type=int)
def done(number):
    """标记完成"""
    manager = TodoManager()
    manager.mark_done(number)
    click.echo(f"✓ 任务 {number} 已完成")
```

### 使用的 Skills

- `click`: CLI 框架
- `pytest`: 测试框架

### 实现笔记

- Click 的装饰器语法很直观
- 纯文本存储简化了数据管理
- 参数验证需要手动实现

---

## Phase A: 验收

### 验收标准

| 验收项 | 结果 | 说明 |
|--------|------|------|
| 添加任务 | Pass ✅ | 可以正常添加 |
| 列出任务 | Pass ✅ | 显示所有任务 |
| 完成任务 | Pass ✅ | 状态更新正确 |
| P1 功能 | Skip | 未实现，留待后续 |

### 演化记录

**有效参数**:
- Click 版本: 8.1.0+ 兼容性最好
- 文件编码: UTF-8，支持中文任务

**成功技巧**:
- 使用 `@click.group()` 组织子命令
- 使用 `click.echo()` 而不是 `print()`

**反模式**:
- 不要在业务逻辑中混用 CLI 代码

---

## 项目总结

### 成果

- 功能完整的 CLI 待办应用
- 清晰的代码结构
- 完整的使用文档

### 经验总结

1. **GAIA 框架优势**:
   - Phase G 让我们先调研了 todo-txt 和 topydo
   - MVP 定义避免了功能蔓延
   - 演化记录记录了有效参数

2. **改进建议**:
   - 可以添加更多 P1 功能
   - 考虑添加配置文件支持

3. **可复用的 Skill**:
   - Click CLI 模板
   - 纯文本存储模式
