# GAIA 快速开始指南

本指南帮助你快速上手 GAIA 框架。

---

## 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/gaia-framework.git
cd gaia-framework

# 安装依赖（可选）
pip install -e .
```

---

## 基本使用

### 1. 初始化项目

```bash
gaia init my-project
```

### 2. 启动 Phase G

```bash
gaia phase generate "需要实现用户认证功能"
```

### 3. 设置解决方案大纲

```bash
gaia phase set-outline "使用 JWT + Flask-Login 实现"
```

### 4. 推进到下一阶段

```bash
gaia phase advance
```

### 5. 查看状态

```bash
gaia status
```

---

## 模板使用

### 列出可用模板

```bash
gaia template list
```

### 渲染模板

```bash
# 渲染 PRD 模板
gaia template render prd -o prd.md -p product_name=MyApp

# 渲染复盘模板
gaia template render retrospective -o retro.md -p project_name=MyApp
```

---

## Skill 管理

### 安装 Skill

```bash
# 从 GitHub 安装
gaia skill install anthropics/skills

# 从 Git URL 安装
gaia skill install https://github.com/user/repo.git
```

### 列出 Skills

```bash
gaia skill list
```

### 搜索 Skills

```bash
gaia skill search authentication
```

---

## 工作流使用

### 验证工作流

```bash
gaia workflow validate examples/workflows/gaia-full-flow.yaml
```

### 运行工作流

```bash
gaia workflow run examples/workflows/project-init.yaml -v project_name=MyApp
```

---

## Python API 使用

```python
from gaia_core import GAIAEngine, Phase, Priority

# 创建引擎
engine = GAIAEngine("my-project")

# Phase G
engine.start_generate("需要实现用户认证", path="market")

# Phase A
engine.add_task("实现登录接口", Priority.P0)
engine.add_task("实现注册接口", Priority.P0)

# 导出演化记录
engine.export_evolution()
```

---

## Web API

启动服务器:

```bash
cd gaia_web
python -m uvicorn backend:app --reload
```

访问 http://localhost:8000/docs 查看 API 文档。

---

## 下一步

- 阅读 [GAIA 框架文档](../01-gaia-framework/overview.md)
- 查看 [更多示例](../examples/)
- 了解 [工作流定义](../examples/workflows/)
