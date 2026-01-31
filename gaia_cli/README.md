# GAIA CLI Tools

## 模块概述

CLI 工具集是用户与 GAIA 框架交互的主要命令行接口。

## 目录结构

```
gaia_cli/
└── commands/        # 命令实现
```

## 核心命令

| 命令 | 描述 | 优先级 |
|------|------|--------|
| `gaia init` | 初始化新项目 | P0 |
| `gaia phase` | 执行指定阶段 | P0 |
| `gaia skill` | Skill 管理命令 | P0 |
| `gaia template` | 模板操作 | P1 |
| `gaia evolve` | 记录演化经验 | P1 |
| `gaia status` | 查看项目状态 | P1 |

## 参考实现

- GitHub CLI (gh)
- Aider
- Pythagora

## 交付物

- Python 包 (gaia-cli)
- 命令参考文档
- Shell 自动补全脚本
