# GAIA 框架

> 系统化的 AI 协作问题解决框架

[![Python 版本](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![许可证](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![测试](https://img.shields.io/badge/tests-53%20passing-brightgreen.svg)](tests/)

[English](README.md) | 简体中文

---

## 什么是 GAIA？

**GAIA**（Generate → Analyze → Implement → Acceptance，生成→分析→实现→验收）是一套用于 AI 协作解决复杂问题的系统化框架。它通过结构化的四阶段方法，将 AI 从简单的"执行者"转变为"分析师、架构师和工匠"。

**一句话概括**：GAIA 是一套让 AI 协作从临时对话升级为系统化问题解决的工作协议。

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   │
│   │  G: 生成 │ → │  A: 分析 │ → │  I: 实现 │ → │  A: 验收 │   │
│   │Generate │   │ Analyze │   │Implement│   │Acceptance│  │
│   └─────────┘   └─────────┘   └─────────┘   └─────────┘   │
│      专家思维      架构师思维      工匠思维      质检员思维    │
│   定义"做什么"    分解与规划     构建与记录     验证与复盘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 特性

### 🎯 四阶段执行模型

| 阶段 | 思维模式 | 核心产出 |
|------|----------|----------|
| **G: 生成** | 专家 | 解决方案大纲 |
| **A: 分析** | 架构师 | MVP 定义与优先级 |
| **I: 实现** | 工匠 | 可交付成果 |
| **A: 验收** | 质检员 | 验收报告与演化记录 |

### 🧩 核心模块

- **`gaia_core`** - 执行引擎、状态管理、阶段执行器
- **`gaia_skills`** - Skill 安装、演化追踪、仓库管理
- **`gaia_knowledge`** - 知识图谱、语义搜索、模式库
- **`gaia_templates`** - 模板引擎与内置模板
- **`gaia_workflow`** - YAML DSL 工作流编排
- **`gaia_integration`** - MCP 网关、统一 API、适配器
- **`gaia_cli`** - 命令行界面
- **`gaia_web`** - FastAPI 后端服务

### 📊 知识管理

- **知识图谱** - 追踪 Skill、任务和经验之间的关系
- **语义搜索** - 文档索引与查询扩展
- **模式库** - 最佳实践与反模式
- **演化追踪** - 记录有效参数与经验教训

---

## 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/gaia.git
cd gaia

# 安装依赖
pip install -e .

# 或包含 Web 支持
pip install -e ".[web]"

# 或包含开发依赖
pip install -e ".[dev]"
```

### 初始化新项目

```bash
# 交互式项目设置
python scripts/quickstart.py

# 或手动操作
gaia init my-project
cd my-project
```

### 运行演示

```bash
# 查看所有功能演示
python examples/demo.py
```

### 基本用法

```python
from gaia_core import GAIAEngine, Phase, Priority

# 创建引擎
engine = GAIAEngine("my-project")

# Phase G: 生成
engine.start_generate("用 Python 构建一个 CLI 待办事项应用")
engine.set_solution_outline("使用 Click 构建 CLI，JSON 存储数据")

# Phase A: 分析
engine.advance_phase()
engine.add_task("设计 CLI 界面", Priority.P0)
engine.add_task("实现存储层", Priority.P0)

# 查看状态
status = engine.get_status()
print(f"当前阶段: {status['current_phase']['label']}")
print(f"任务数量: {status['tasks']['total']}")
```

---

## 文档

| 主题 | 链接 |
|------|------|
| 框架概览 | [docs/01-gaia-framework/overview.md](docs/01-gaia-framework/overview.md) |
| 核心原则 | [docs/01-gaia-framework/principles.md](docs/01-gaia-framework/principles.md) |
| 快速入门 | [docs/getting-started.md](docs/getting-started.md) |
| API 参考 | [docs/api-reference.md](docs/api-reference.md) |
| 更新日志 | [docs/02-progress/changelog.md](docs/02-progress/changelog.md) |

---

## CLI 命令

```bash
# 初始化新项目
gaia init <项目名称>

# 阶段操作
gaia phase generate <问题陈述>
gaia phase analyze
gaia phase implement
gaia phase accept

# 任务管理
gaia task add <标题> --priority P0
gaia task list
gaia task complete <任务ID>

# Skill 管理
gaia skill install <git-url>
gaia skill list
gaia skill update <skill-id>

# 模板操作
gaia template list
gaia template render <模板ID>

# 工作流执行
gaia workflow run <workflow-yaml>
gaia workflow validate <workflow-yaml>

# 状态查询
gaia status
```

---

## 工作流示例

```yaml
# gaia-full-flow.yaml
id: gaia-full-flow
name: 完整 GAIA 流程

triggers:
  - type: manual

steps:
  - id: generate
    action: phase_generate
    params:
      problem: "构建一个 CLI 待办事项应用"
      path: "market-first"

  - id: analyze
    action: phase_analyze
    depends_on: [generate]

  - id: implement
    action: phase_implement
    depends_on: [analyze]

  - id: accept
    action: phase_accept
    depends_on: [implement]
```

运行工作流：
```bash
gaia workflow run examples/workflows/gaia-full-flow.yaml
```

---

## 开发

### 运行测试

```bash
# 所有测试
pytest tests/

# 特定模块
pytest tests/core/

# 带覆盖率
pytest --cov=gaia_core --cov=gaia_knowledge tests/
```

### 代码质量

```bash
# 格式化代码
black gaia_*/ tests/

# 代码检查
ruff check gaia_*/ tests/

# 类型检查
mypy gaia_core/
```

### 项目结构

```
gaia/
├── gaia_core/           # 核心引擎
├── gaia_skills/         # Skill 管理
├── gaia_knowledge/      # 知识系统
├── gaia_templates/      # 模板引擎
├── gaia_workflow/       # 工作流编排
├── gaia_integration/    # MCP 与 API
├── gaia_cli/           # CLI 命令
├── gaia_web/           # FastAPI 后端
├── tests/              # 53 个测试
├── examples/           # 演示脚本
├── scripts/            # 工具脚本
└── docs/               # 文档
```

---

## 环境要求

- Python 3.10+
- Click 8.1+
- Pydantic 2.0+
- PyYAML 6.0+
- Requests 2.28+
- Rich 13.0+
- NetworkX 3.0+

---

## 路线图

- [ ] 增强的 MCP 协议支持
- [ ] Web 仪表板界面
- [ ] Skill 市场集成
- [ ] 多语言 SDK
- [ ] Docker 部署

详情请参阅 [docs/02-progress/roadmap.md](docs/02-progress/roadmap.md)。

---

## 贡献

欢迎贡献！请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 了解指南。

1. Fork 本仓库
2. 创建功能分支
3. 进行更改
4. 添加测试
5. 提交 Pull Request

---

## 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 致谢

灵感来源：
- [Anthropic Skills](https://github.com/anthropics/skills)
- [ComposioHQ](https://github.com/ComposioHQ/composio)
- [AutoGPT](https://github.com/Significant-Gravitas/AutoGPT)
- [LangChain](https://github.com/langchain-ai/langchain)

---

## 链接

- **文档**: [docs/](docs/)
- **问题反馈**: [GitHub Issues](https://github.com/yourusername/gaia-framework/issues)
- **讨论**: [GitHub Discussions](https://github.com/yourusername/gaia-framework/discussions)

---

<div align="center">

**为 AI 协作社区打造 ❤️**

</div>
