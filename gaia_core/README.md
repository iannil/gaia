# GAIA Core Engine

## 模块概述

GAIA 核心引擎是 GAIA 的执行框架核心，负责协调 G → A → I → A 四阶段流程。

## 目录结构

```
gaia_core/
├── engine/          # GAIA 执行引擎核心
├── phases/          # Phase 实现 (G/A/I/A)
└── state/           # 状态管理
```

## 功能点

| 子模块 | 描述 | 优先级 |
|--------|------|--------|
| Phase 管理 | G → A → I → A 四阶段状态机 | P0 |
| 任务分解器 | 将复杂任务分解为可执行步骤 | P0 |
| 上下文传递 | 跨阶段状态和知识传递 | P0 |
| 验收检查器 | MVP Pass/Fail 自动验证 | P1 |
| 进度追踪 | 实时任务执行状态展示 | P1 |

## 参考实现

- LangChain Chains
- CrewAI Flows
- AutoGPT Goal Decomposition

## 交付物

- 状态机定义
- Phase 接口规范
- 执行引擎核心代码
