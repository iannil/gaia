# GAIA Web Interface

## 模块概述

Web 可视化界面提供图形化的项目管理和协作体验。

## 目录结构

```
gaia-web/
├── backend/         # FastAPI 后端
└── frontend/        # React 前端
```

## 功能点

| 子模块 | 描述 | 优先级 |
|--------|------|--------|
| Web Dashboard | 项目和任务总览 | P1 |
| GAIA 流程可视化 | 四阶段流程图展示 | P1 |
| 知识图谱视图 | Skill/经验关系可视化 | P1 |
| 模板编辑器 | 可视化模板创建 | P2 |
| 实时协作 | 多用户协作编辑 | P2 |

## 参考实现

- Cursor IDE
- n8n Visual Builder
- Notion 界面

## 技术栈

- 后端: FastAPI
- 前端: React
- 图谱: D3.js / Cytoscape.js

## 交付物

- Web 应用
- 组件库
- API 契约
