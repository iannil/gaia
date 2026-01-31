# 迭代历史

本文档记录 GAIA 项目的所有重要变更。

---

## Version 0.5.0 (2025-01-31)

### 新增
- **类型存根**: 为所有核心模块添加 `.pyi` 类型存根文件
  - `gaia_core/__init__.pyi` - 核心引擎类型
  - `gaia_knowledge/__init__.pyi` - 知识图谱类型
  - `gaia_workflow/__init__.pyi` - 工作流类型
  - `gaia_templates/__init__.pyi` - 模板引擎类型
  - `gaia_skills/__init__.pyi` - Skill 管理类型
- **Demo 脚本**: `examples/demo.py` - 全功能演示脚本
- **Quick Start**: `scripts/quickstart.py` - 交互式项目初始化脚本

### 测试
- 新增 53 个测试用例，全部通过
- 测试覆盖率: Core (16), Knowledge (10), Skills (14), Workflow (13)

### 修复
- **Pydantic v2 兼容**: 将 `class Config` 替换为 `ConfigDict`
- **枚举序列化**: 修复 Phase/PhaseStatus/Priority 的 JSON 序列化/反序列化
- **测试隔离**: 修复测试间的状态共享问题
- **模板命名冲突**: 修复 Template 与 string.Template 的命名冲突

### 改进
- KnowledgeGraph 添加 `count()`, `nodes`, `edges` 属性
- PatternLibrary 添加 `count()` 方法
- GAIAEngine 改进 Phase 推进逻辑
- StateStore 改进枚举类型转换

---

## Version 0.4.0 (2025-01-31)

### 新增 - Phase 3: 生态扩展
- gaia_knowledge: 知识图谱、语义搜索、模式库
- gaia_templates: 模板引擎、内置模板
- gaia_workflow: 工作流 DSL、执行器、触发器
- gaia_integration: MCP 网关、统一 API、适配器
- gaia_web: FastAPI 后端服务
- 示例工作流: 4 个 YAML 工作流示例

### 核心功能实现
- **知识图谱**: Node/Edge 模型、路径查询、中心性分析、连通分量
- **语义搜索**: 文档索引、倒排索引、查询扩展、TF 计算
- **模式库**: 6 个内置最佳实践/反模式
- **模板系统**: 参数化渲染、模板继承、4 个内置模板
- **工作流**: YAML DSL、异步执行器、依赖管理、触发器

### CLI 扩展
- `gaia template list/render/info`: 模板操作
- `gaia workflow run/validate`: 工作流执行

### API 服务
- FastAPI 后端: /api/v1/ 端点
- REST API: Phase, Skill, Knowledge, Template, Integration, Workflow

---

## Version 0.3.0 (2025-01-31)

### 新增
- 创建 8 个功能模块目录结构（gaia-core, gaia-skills, gaia-knowledge, gaia-templates, gaia-workflow, gaia-integration, gaia-cli, gaia-web）
- 新增模块 README 文档（每个模块的职责、目录结构、功能矩阵）
- 新增系统架构图（5 层架构：核心层 → Skill 层 → 知识层 → 集成层 → 交互层）
- 新增 M3/M4/M5 里程碑规划（Phase 1/2/3 验收标准）
- 新增参考平台链接（20+ 个 AI 协作、知识管理、工作流自动化平台）

### 变更
- 重写 `docs/02-progress/roadmap.md`：替换为完整的功能模块开发计划
- 更新 `docs/02-progress/milestones.md`：添加 M3/M4/M5 里程碑
- 更新 `docs/01-gaia-framework/overview.md`：添加系统架构图
- 更新 `docs/04-appendix/references.md`：扩展参考资源列表

### 目录结构
```
新增模块目录:
├── gaia-core/          # 核心引擎
│   ├── engine/
│   ├── phases/
│   └── state/
├── gaia-skills/        # Skill 管理
│   ├── repository/
│   ├── manager/
│   ├── evolution/
│   └── registry/
├── gaia-knowledge/     # 知识系统
│   ├── graph/
│   ├── search/
│   └── patterns/
├── gaia-templates/     # 模板系统
│   ├── engine/
│   ├── built-in/
│   └── custom/
├── gaia-workflow/      # 工作流编排
│   ├── dsl/
│   ├── executor/
│   └── triggers/
├── gaia-integration/   # 集成框架
│   ├── mcp/
│   ├── adapters/
│   └── api/
├── gaia-cli/           # CLI 工具
│   └── commands/
└── gaia-web/           # Web 界面
    ├── backend/
    └── frontend/
```

### 技术栈确定
- 核心引擎: Python 3.10+
- CLI: Click/Typer
- 状态管理: Pydantic
- 知识存储: SQLite + JSON
- 知识图谱: NetworkX
- Web 界面: FastAPI + React
- MCP 协议: anthropic/sdk

---

## Version 0.2.0 (2025-01-31)

### 新增
- 创建完整的 `/docs` 目录结构
- 新增 GAIA 框架详细文档（8 个文件）
- 新增项目进度记录系统（4 个文件）
- 新增模板文件集合（4 个模板）
- 新增附录文档（3 个文件）

### 变更
- 重写 `README.md`：从详细框架文档变为项目门面
- 迁移 GAIA 框架内容到 `docs/01-gaia-framework/`

### 文档结构
```
新增文件:
- docs/index.md
- docs/01-gaia-framework/overview.md
- docs/01-gaia-framework/principles.md
- docs/01-gaia-framework/workflows.md
- docs/01-gaia-framework/best-practices.md
- docs/01-gaia-framework/phases/*.md (4个)
- docs/02-progress/*.md (4个)
- docs/03-cases-templates/index.md
- docs/03-cases-templates/templates/*.md/*.json (4个)
- docs/04-appendix/*.md (3个)
```

---

## Version 0.1.0 (2025-01-31)

### 新增
- 创建 `README.md`：GAIA 框架完整定义
- 创建 `CLAUDE.md`：AI 协作工作指南

### 内容
- 定义 GAIA 执行框架（G → A → I → A）
- 定义四条核心指导原则
- 定义 Phase G 的三条路径
- 定义 Skill 管理约定

---

## 变更类型说明

| 类型标签 | 说明 |
|----------|------|
| 新增 | 新增功能、文档或配置 |
| 变更 | 对现有内容的修改 |
| 移除 | 删除不再需要的内容 |
| 修复 | 修正错误或问题 |
| 重构 | 内部结构调整，不影响功能 |
