# GAIA 文档导航

欢迎来到 GAIA 文档中心。这里是 GAIA 执行框架的完整文档。

---

## 快速开始

| 你想了解 | 跳转到 |
|----------|--------|
| 这个项目是什么 | [项目 README](../README.md) |
| GAIA 框架是什么 | [GAIA 框架总览](./01-gaia-framework/overview.md) |
| 如何开始使用 | [快速开始指南](./getting-started.md) |
| API 参考 | [API 参考文档](./api-reference.md) |
| 项目当前进展 | [进度总览](./02-progress/index.md) |

---

## 文档结构

```
docs/
├── 01-gaia-framework/     # GAIA 框架规范
├── 02-progress/            # 项目进度记录
├── 03-cases-templates/     # 案例与模板
└── 04-appendix/            # 附录
```

---

## 目录导航

### 01. GAIA 框架规范

| 文档 | 说明 |
|------|------|
| [框架总览](./01-gaia-framework/overview.md) | GAIA 框架的定位和价值 |
| [核心原则](./01-gaia-framework/principles.md) | 需求驱动、站在巨人肩上、工匠专家结合、动态演化 |
| [Phase G: 生成](./01-gaia-framework/phases/01-generate.md) | 定义"做什么"与"怎么做" |
| [Phase A: 分析](./01-gaia-framework/phases/02-analyze.md) | 分解与规划 |
| [Phase I: 实现](./01-gaia-framework/phases/03-implement.md) | 构建与记录 |
| [Phase A: 验收](./01-gaia-framework/phases/04-acceptance.md) | 验证与复盘 |
| [工作流与指令映射](./01-gaia-framework/workflows.md) | 标准指令和简化调用 |
| [最佳实践与反模式](./01-gaia-framework/best-practices.md) | 常见问题和建议 |

### 02. 项目进度

| 文档 | 说明 |
|------|------|
| [进度总览](./02-progress/index.md) | 当前状态快照 |
| [里程碑记录](./02-progress/milestones.md) | 关键节点历史 |
| [迭代历史](./02-progress/changelog.md) | 变更记录 |
| [待办规划](./02-progress/roadmap.md) | 短期/中期/长期计划 |

### 03. 案例与模板

| 文档 | 说明 |
|------|------|
| [案例索引](./03-cases-templates/index.md) | 实际应用案例 |
| [PRD 模板](./03-cases-templates/templates/prd-template.md) | 产品需求文档模板 |
| [技术设计模板](./03-cases-templates/templates/tech-design-template.md) | 技术设计文档模板 |
| [复盘模板](./03-cases-templates/templates/retrospective-template.md) | 复盘会议模板 |
| [Skill 演化模板](./03-cases-templates/templates/skill-evolution-template.json) | evolution.json 结构 |

### 04. 附录

| 文档 | 说明 |
|------|------|
| [术语表](./04-appendix/glossary.md) | 关键术语解释 |
| [参考资源](./04-appendix/references.md) | 推荐阅读和资源 |
| [常见问题](./04-appendix/faq.md) | 常见问题解答 |

---

## 按场景查找

| 场景 | 推荐阅读 |
|------|----------|
| 第一次使用 | 框架总览 → 核心原则 → Phase G |
| 遇到技术问题 | Phase G → Phase A → Phase I |
| 任务完成后复盘 | Phase A (验收) → 复盘模板 |
| 想要理解某阶段 | 对应的 Phase 文档 |
| 寻找最佳实践 | 最佳实践与反模式 |
| 查看项目历史 | 进度记录 → 里程碑/变更历史 |
| 需要写文档 | 案例与模板中的对应模板 |

---

## AI 协作入口

如果你是 AI 助手（如 Claude Code），请阅读：
- 根目录的 [CLAUDE.md](../CLAUDE.md) — AI 工作指南
- [核心原则](./01-gaia-framework/principles.md) — 四条核心指导原则

---

## 文档规范

| 类型 | 命名规范 | 示例 |
|------|----------|------|
| 文件夹 | `NN-短横线分隔` | `01-gaia-framework/` |
| 文档文件 | `kebab-case.md` | `best-practices.md` |
| 模板文件 | `*-template.md` | `prd-template.md` |
| 顺序编号 | 两位数前缀 | 01-, 02-, 03- |
