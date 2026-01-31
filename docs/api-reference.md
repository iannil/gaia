# GAIA API 参考文档

GAIA 框架的完整 API 参考。

---

## 模块索引

| 模块 | 说明 |
|------|------|
| [gaia_core](#gaia_core) | 核心引擎 |
| [gaia_skills](#gaia_skills) | Skill 管理 |
| [gaia_knowledge](#gaia_knowledge) | 知识系统 |
| [gaia_templates](#gaia_templates) | 模板系统 |
| [gaia_workflow](#gaia_workflow) | 工作流编排 |
| [gaia_integration](#gaia_integration) | 集成框架 |
| [gaia_web](#gaia_web) | Web API |

---

## gaia_core

### GAIAEngine

```python
from gaia_core import GAIAEngine

engine = GAIAEngine(project_name="my-project")
```

**方法**:

| 方法 | 说明 |
|------|------|
| `start_generate(problem, path)` | 启动 Phase G |
| `start_analyze(mvp=None)` | 启动 Phase A |
| `start_implement()` | 启动 Phase I |
| `start_acceptance(criteria=None)` | 启动 Phase A 验收 |
| `advance_phase()` | 推进到下一阶段 |
| `add_task(title, priority)` | 添加任务 |
| `save()` | 保存状态 |
| `get_status()` | 获取状态 |

**示例**:

```python
engine = GAIAEngine("my-project")
engine.start_generate("需要实现用户认证")
engine.add_task("实现登录", Priority.P0)
status = engine.get_status()
```

---

## gaia_skills

### SkillManager

```python
from gaia_skills import SkillManager

manager = SkillManager()
```

**方法**:

| 方法 | 说明 |
|------|------|
| `install_from_git(url, skill_id)` | 从 Git 安装 |
| `install_from_github(repo, skill_id)` | 从 GitHub 安装 |
| `update(skill_id)` | 更新 Skill |
| `uninstall(skill_id, keep_files)` | 卸载 Skill |
| `list_skills(category, tag)` | 列出 Skills |
| `search_skills(query)` | 搜索 Skills |

### EvolutionManager

```python
from gaia_skills import EvolutionManager

evolution = EvolutionManager()
```

**方法**:

| 方法 | 说明 |
|------|------|
| `create(skill_id, skill_name)` | 创建演化记录 |
| `save_record(record)` | 保存记录 |
| `get_record(skill_id)` | 获取记录 |
| `add_parameter(skill_id, ...)` | 添加参数 |
| `add_success_pattern(skill_id, ...)` | 添加成功模式 |
| `add_anti_pattern(skill_id, ...)` | 添加反模式 |

---

## gaia_knowledge

### KnowledgeGraph

```python
from gaia_knowledge import KnowledgeGraph, Node, Edge

graph = KnowledgeGraph()
graph.add_node(Node(id="n1", type="skill", label="Git"))
graph.add_edge(Edge(id="e1", source="n1", target="n2", relation="similar_to"))
```

**方法**:

| 方法 | 说明 |
|------|------|
| `add_node(node)` | 添加节点 |
| `add_edge(edge)` | 添加边 |
| `get_node(node_id)` | 获取节点 |
| `get_neighbors(node_id)` | 获取邻居 |
| `shortest_path(source, target)` | 最短路径 |
| `search(query)` | 搜索节点 |
| `to_json(path)` | 导出 JSON |

### SemanticSearch

```python
from gaia_knowledge import SemanticSearch

search = SemanticSearch()
search.index.add_document(doc_id, title, content, doc_type)
results = search.search(query)
```

### PatternLibrary

```python
from gaia_knowledge import PatternLibrary

library = PatternLibrary()
library.load_builtin_patterns()
best_practices = library.get_best_practices()
```

---

## gaia_templates

### TemplateEngine

```python
from gaia_templates import TemplateEngine

engine = TemplateEngine()
engine.load_builtin_templates()
result = engine.render("prd", {"product_name": "MyApp"})
```

**内置模板**:

| ID | 名称 | 分类 |
|----|------|------|
| `phase-startup` | Phase 启动模板 | gaia |
| `skill-definition` | Skill 定义模板 | skill |
| `prd` | PRD 模板 | document |
| `retrospective` | 复盘模板 | document |

---

## gaia_workflow

### WorkflowParser

```python
from gaia_workflow import WorkflowParser

parser = WorkflowParser()
workflow = parser.parse_file("workflow.yaml")
```

### WorkflowExecutor

```python
from gaia_workflow import WorkflowExecutor

executor = WorkflowExecutor()
execution = executor.execute_sync(workflow, variables)
```

### WorkflowBuilder

```python
from gaia_workflow import WorkflowBuilder, Actions

builder = WorkflowBuilder("my-workflow", "My Workflow")
builder.step("s1", Actions.ECHO, parameters={"message": "Hello"})
workflow = builder.build()
```

---

## gaia_integration

### MCPGateway

```python
from gaia_integration import MCPGateway

gateway = MCPGateway()
gateway.setup_gaia_tools()
await gateway.call_tool("gaia.phase.generate", {"problem": "..."})
```

### UnifiedAPI

```python
from gaia_integration import AdapterFactory, UnifiedAPI

api = UnifiedAPI()
adapter = AdapterFactory.create("github", {"token": "...", "owner": "...", "repo": "..."})
api.register_adapter("github", adapter)
result = api.call("github", "create_issue", title="Issue", body="...")
```

---

## gaia_web

### FastAPI 应用

```python
from gaia_web import app
import uvicorn

# 运行服务器
uvicorn.run(app, host="0.0.0.0", port=8000)
```

**API 端点**:

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v1/phase/generate` | POST | 启动 Phase G |
| `/api/v1/phase/advance` | POST | 推进阶段 |
| `/api/v1/skills` | GET | 列出 Skills |
| `/api/v1/skills/install` | POST | 安装 Skill |
| `/api/v1/knowledge/search` | GET | 搜索知识 |
| `/api/v1/patterns` | GET | 列出模式 |
| `/api/v1/templates` | GET | 列出模板 |
| `/api/v1/templates/render` | POST | 渲染模板 |
| `/api/v1/workflows/execute` | POST | 执行工作流 |

---

## REST API 请求示例

### 启动 Phase G

```bash
curl -X POST http://localhost:8000/api/v1/phase/generate \
  -H "Content-Type: application/json" \
  -d '{"project": "my-project", "problem": "需要实现用户认证", "path": "market"}'
```

### 安装 Skill

```bash
curl -X POST http://localhost:8000/api/v1/skills/install \
  -H "Content-Type: application/json" \
  -d '{"source": "anthropics/skills"}'
```

### 渲染模板

```bash
curl -X POST http://localhost:8000/api/v1/templates/render \
  -H "Content-Type: application/json" \
  -d '{"template_id": "prd", "values": {"product_name": "MyApp"}}'
```

### 执行工作流

```bash
curl -X POST http://localhost:8000/api/v1/workflows/execute \
  -H "Content-Type: application/json" \
  -d '{"workflow": {...}, "variables": {...}}'
```
