# 贡献指南

感谢你有意贡献 GAIA 项目！

---

## 开发环境设置

### 1. Fork 和克隆

```bash
# Fork 仓库
git clone https://github.com/YOUR_USERNAME/gaia-framework.git
cd gaia-framework
git remote add upstream https://github.com/ORIGINAL_OWNER/gaia-framework.git
```

### 2. 创建虚拟环境

```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows
```

### 3. 安装依赖

```bash
pip install -e ".[dev]"
```

---

## 开发流程

### 分支策略

- `master` - 主分支，稳定版本
- `develop` - 开发分支
- `feature/*` - 功能分支
- `fix/*` - 修复分支

### 工作流程

1. 从 `develop` 创建功能分支
   ```bash
   git checkout develop
   git pull upstream develop
   git checkout -b feature/your-feature-name
   ```

2. 进行开发和测试
   ```bash
   make test
   make lint
   make format
   ```

3. 提交变更
   ```bash
   git add .
   git commit -m "feat: add your feature"
   ```

4. 推送到你的 fork 并创建 Pull Request

---

## 代码规范

### Python 代码风格

- 使用 **Black** 进行代码格式化
- 使用 **Ruff** 进行 linting
- 使用 **类型注解** (type hints)
- 遵循 **PEP 8** 规范

### 命名约定

| 类型 | 约定 | 示例 |
|------|------|------|
| 模块 | `snake_case` | `gaia_core/` |
| 类 | `PascalCase` | `GAIAEngine` |
| 函数/方法 | `snake_case` | `get_status()` |
| 常量 | `UPPER_SNAKE_CASE` | `MAX_RETRIES` |
| 私有成员 | `_leading_underscore` | `_internal_method` |

### 文档字符串

使用 Google 风格的文档字符串：

```python
def phase_generate(problem: str, path: str = "market") -> bool:
    """启动 Phase G: 生成阶段

    Args:
        problem: 问题陈述
        path: 解决方案路径 (market/github/masters)

    Returns:
        是否成功启动

    Raises:
        ValueError: 当参数无效时
    """
```

---

## 测试

### 运行测试

```bash
# 所有测试
make test

# 详细输出
make test-verbose

# 特定模块
pytest tests/core/test_state.py -v

# 带覆盖率
pytest --cov=gaia_core --cov-report=html
```

### 编写测试

- 测试文件放在 `tests/` 目录下
- 测试文件名格式: `test_<module>.py`
- 使用 `pytest` 和 `pytest-asyncio` 编写测试

---

## 提交规范

### Commit Message 格式

使用 [Conventional Commits](https://www.conventionalcommits.org/)：

```
<type>(<scope>): <subject>

<body>
```

**类型 (type)**:
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具链相关

**示例**:
```
feat(core): add phase transition validation

Check if phase transitions are valid before executing.
Add validation logic to prevent invalid state transitions.
```

---

## Pull Request 流程

### PR 标题

格式: `[模块]: 简短描述`

示例:
```
[Core]: Add phase transition validation
[Skills]: Implement skill search functionality
```

### PR 描述模板

```markdown
## 变更内容
- 添加了功能 X
- 修复了问题 Y

## 相关 Issue
Closes #123

## 测试
- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] 文档已更新

## 检查清单
- [ ] 代码符合规范
- [ ] 添加了必要的测试
- [ ] 更新了相关文档
```

---

## 发布流程

由维护者执行：

1. 更新版本号
2. 更新 CHANGELOG
3. 创建 Git tag
4. 构建和发布到 PyPI

---

## 问题反馈

- **Bug 报告**: 使用 GitHub Issues
- **功能请求**: 使用 GitHub Discussions
- **安全问题**: 请私下联系维护者

---

## 行为准则

- 尊重他人
- 欢迎不同观点
- 专注于项目目标
- 建设性讨论

---

## 许可证

贡献的代码将采用项目的 MIT 许可证。
