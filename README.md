# GAIA Framework

> A systematic AI-collaborative problem-solving framework

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-53%20passing-brightgreen.svg)](tests/)

---

## What is GAIA?

**GAIA** (Generate → Analyze → Implement → Acceptance) is a systematic framework for solving complex problems with AI collaboration. It transforms AI from a simple "executor" into an "analyst, architect, and craftsman" through a structured four-phase approach.

**In one sentence**: GAIA is a working protocol that elevates AI collaboration from ad-hoc conversations to systematic problem-solving.

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   │
│   │  G: Gen │ → │  A: Ana │ → │  I: Imp │ → │  A: Acc │   │
│   │Generate │   │ Analyze │   │Implement│   │Acceptance│  │
│   └─────────┘   └─────────┘   └─────────┘   └─────────┘   │
│    Expert Mind    Architect Mind   Craftsman Mind   QA Mind │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Features

### 🎯 Four-Phase Execution Model

| Phase | Mindset | Output |
|-------|---------|--------|
| **G: Generate** | Expert | Solution outline |
| **A: Analyze** | Architect | MVP definition & priorities |
| **I: Implement** | Craftsman | Deliverable artifacts |
| **A: Acceptance** | QA | Validation report & evolution record |

### 🧩 Core Modules

- **`gaia_core`** - Execution engine, state management, phase executors
- **`gaia_skills`** - Skill installation, evolution tracking, repository
- **`gaia_knowledge`** - Knowledge graph, semantic search, pattern library
- **`gaia_templates`** - Template engine with built-in templates
- **`gaia_workflow`** - YAML DSL workflow orchestration
- **`gaia_integration`** - MCP gateway, unified API, adapters
- **`gaia_cli`** - Command-line interface
- **`gaia_web`** - FastAPI backend service

### 📊 Knowledge Management

- **Knowledge Graph** - Track relationships between skills, tasks, and experiences
- **Semantic Search** - Document indexing with query expansion
- **Pattern Library** - Best practices and anti-patterns
- **Evolution Tracking** - Record effective parameters and lessons learned

---

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/gaia.git
cd gaia

# Install dependencies
pip install -e .

# Or with web support
pip install -e ".[web]"

# Or with dev dependencies
pip install -e ".[dev]"
```

### Initialize a New Project

```bash
# Interactive project setup
python scripts/quickstart.py

# Or manually
gaia init my-project
cd my-project
```

### Run Demo

```bash
# See all features in action
python examples/demo.py
```

### Basic Usage

```python
from gaia_core import GAIAEngine, Phase, Priority

# Create engine
engine = GAIAEngine("my-project")

# Phase G: Generate
engine.start_generate("Build a CLI todo app with Python")
engine.set_solution_outline("Use Click for CLI, JSON for storage")

# Phase A: Analyze
engine.advance_phase()
engine.add_task("Design CLI interface", Priority.P0)
engine.add_task("Implement storage layer", Priority.P0)

# Check status
status = engine.get_status()
print(f"Current phase: {status['current_phase']['label']}")
print(f"Tasks: {status['tasks']['total']}")
```

---

## Documentation

| Topic | Link |
|-------|------|
| Framework Overview | [docs/01-gaia-framework/overview.md](docs/01-gaia-framework/overview.md) |
| Core Principles | [docs/01-gaia-framework/principles.md](docs/01-gaia-framework/principles.md) |
| Getting Started | [docs/getting-started.md](docs/getting-started.md) |
| API Reference | [docs/api-reference.md](docs/api-reference.md) |
| Changelog | [docs/02-progress/changelog.md](docs/02-progress/changelog.md) |

---

## CLI Commands

```bash
# Initialize a new project
gaia init <project-name>

# Phase operations
gaia phase generate <problem>
gaia phase analyze
gaia phase implement
gaia phase accept

# Task management
gaia task add <title> --priority P0
gaia task list
gaia task complete <task-id>

# Skill management
gaia skill install <git-url>
gaia skill list
gaia skill update <skill-id>

# Template operations
gaia template list
gaia template render <template-id>

# Workflow execution
gaia workflow run <workflow-yaml>
gaia workflow validate <workflow-yaml>

# Status
gaia status
```

---

## Workflow Example

```yaml
# gaia-full-flow.yaml
id: gaia-full-flow
name: Complete GAIA Process

triggers:
  - type: manual

steps:
  - id: generate
    action: phase_generate
    params:
      problem: "Build a CLI todo app"
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

Run workflow:
```bash
gaia workflow run examples/workflows/gaia-full-flow.yaml
```

---

## Development

### Running Tests

```bash
# All tests
pytest tests/

# Specific module
pytest tests/core/

# With coverage
pytest --cov=gaia_core --cov=gaia_knowledge tests/
```

### Code Quality

```bash
# Format code
black gaia_*/ tests/

# Lint
ruff check gaia_*/ tests/

# Type check
mypy gaia_core/
```

### Project Structure

```
gaia/
├── gaia_core/           # Core engine
├── gaia_skills/         # Skill management
├── gaia_knowledge/      # Knowledge system
├── gaia_templates/      # Template engine
├── gaia_workflow/       # Workflow orchestration
├── gaia_integration/    # MCP & API
├── gaia_cli/           # CLI commands
├── gaia_web/           # FastAPI backend
├── tests/              # 53 tests
├── examples/           # Demo scripts
├── scripts/            # Utilities
└── docs/               # Documentation
```

---

## Requirements

- Python 3.10+
- Click 8.1+
- Pydantic 2.0+
- PyYAML 6.0+
- Requests 2.28+
- Rich 13.0+
- NetworkX 3.0+

---

## Roadmap

- [ ] Enhanced MCP protocol support
- [ ] Web dashboard UI
- [ ] Skill marketplace integration
- [ ] Multi-language SDKs
- [ ] Docker deployment

See [docs/02-progress/roadmap.md](docs/02-progress/roadmap.md) for details.

---

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Acknowledgments

Inspired by:
- [Anthropic Skills](https://github.com/anthropics/skills)
- [ComposioHQ](https://github.com/ComposioHQ/composio)
- [AutoGPT](https://github.com/Significant-Gravitas/AutoGPT)
- [LangChain](https://github.com/langchain-ai/langchain)

---

## Links

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/yourusername/gaia-framework/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/gaia-framework/discussions)

---

<div align="center">

**Made with ❤️ for the AI collaboration community**

</div>
