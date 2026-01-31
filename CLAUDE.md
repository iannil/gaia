# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在此仓库中工作时提供指导。

## 仓库定位

这是 GAIA，一个 AI 协作概念框架仓库。它不包含源代码——其目的是定义 GAIA 执行框架（Generate → Analyze → Implement → Acceptance），用于系统性地解决复杂问题。

## 核心指导原则

1. 需求驱动 (Need-Driven)：所有行动必须源于明确、真实的需求。绝不为工具而工具。
2. 站在巨人肩上 (Leverage Giants)：优先利用现有市场/社区方案，避免重复造轮子。
3. 工匠与专家结合 (Craftsman & Expert Duality)：像专家一样思考（规划/设计），像工匠一样工作（实现/打磨）。
4. 动态演化 (Dynamic Evolution)：每次交互都应被记录并优化，以支持未来的决策。

## GAIA 执行框架

所有复杂任务都应遵循这四个阶段：

### Phase G: 生成 (Generate)

通过三条路径定义"做什么"和"怎么做"：

- 市场优先 (`search-skill`)：在可信源中搜索现有 Skills（anthropics/skills、ComposioHQ 等）
- 原理优先 (`skill-from-github`)：当市场无解决方案时，从高质量 GitHub 仓库学习核心算法
- 方法论优先 (`skill-from-masters`)：针对战略/创意问题，综合专家理论、最佳实践和反模式

### Phase A: 分析 (Analyze)

分解与规划：

- 定义 MVP（核心功能 vs. 锦上添花 vs. 明确不做）
- 优先级排序子任务（排名优于时间估算）
- 评估技术和知识依赖

### Phase I: 实现 (Implement)

使用"三件套"工具箱进行构建和记录：

- 工具箱管理 (`skill-manager`, `github-to-skills`)：仅打包 CLI/API 友好且绝对必要的工具
- 演化记录 (`skill-evolution-manager`)：将所有有效参数、成功技巧和坑点记录到 `evolution.json`

### Phase A: 验收 (Acceptance)

验证与归档：

- 对照 Phase A 的核心需求进行 Pass/Fail 验证
- 复盘：更新 `evolution.json`，清理临时 Skills
- 成果持久化：确保所有交付物妥善保存（"文件即记忆"）

## Skill 管理约定

使用以下简写指令映射：

- `ls-skills` → 列出所有 Skills
- `check-skills` → 检查所有 Skills 的更新

使用 `github-to-skills` 前，请验证项目是否适合（CLI/API 友好型，而非 GUI/复杂环境重型）。

## 文档语言

主要文档（README.md）使用中文编写，这反映了预期的用户群体和协作语境。
