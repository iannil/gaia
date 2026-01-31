#!/usr/bin/env python3
"""
GAIA Quick Start Script

This script helps you quickly initialize a new GAIA project.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

def print_header(text: str) -> None:
    """Print a formatted header"""
    print(f"\n{'=' * 60}")
    print(f"  {text}")
    print(f"{'=' * 60}\n")

def print_step(step: int, text: str) -> None:
    """Print a formatted step"""
    print(f"[{step}] {text}")

def get_input(prompt: str, default: str = "") -> str:
    """Get user input with optional default"""
    if default:
        full_prompt = f"{prompt} [{default}]: "
    else:
        full_prompt = f"{prompt}: "
    result = input(full_prompt).strip()
    return result if result else default

def select_option(prompt: str, options: list[str]) -> str:
    """Select an option from a list"""
    print(f"\n{prompt}")
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")

    while True:
        choice = input(f"\nSelect (1-{len(options)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        print("Invalid choice, please try again.")

def confirm(prompt: str, default: bool = True) -> bool:
    """Ask for yes/no confirmation"""
    default_str = "Y/n" if default else "y/N"
    response = input(f"{prompt} [{default_str}]: ").strip().lower()
    if not response:
        return default
    return response in ["y", "yes"]

def create_project_directory(project_name: str, base_path: Path) -> Path:
    """Create project directory structure"""
    project_path = base_path / project_name

    # Create directories
    dirs = [
        project_path,
        project_path / ".gaia",
        project_path / "docs",
        project_path / "src",
        project_path / "tests",
    ]

    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"  Created: {dir_path.relative_to(base_path)}")

    return project_path

def create_initial_state(project_path: Path, project_name: str, problem: str) -> None:
    """Create initial GAIA state file"""
    state_file = project_path / ".gaia" / "state.json"

    state = {
        "project_id": project_name.lower().replace(" ", "-"),
        "project_name": project_name,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "current_phase": "G",
        "phase_status": "pending",
        "phase_states": {
            "G": "pending",
            "A": "pending",
            "I": "pending",
            "A2": "pending"
        },
        "problem_statement": problem,
        "generate_path": "search-skill",
        "solution_outline": None,
        "tasks": [],
        "mvp_definition": None,
        "used_skills": [],
        "implementation_notes": [],
        "acceptance_criteria": [],
        "acceptance_results": {},
        "retrospective_notes": None,
        "evolution_data": {},
        "context": {}
    }

    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

    print(f"  Created: .gaia/state.json")

def create_readme(project_path: Path, project_name: str, description: str) -> None:
    """Create README.md file"""
    readme_content = f"""# {project_name}

{description}

## GAIA Project

This project uses the GAIA framework for systematic problem solving.

## Project Structure

```
{project_name}/
├── .gaia/           # GAIA state and evolution data
├── docs/            # Project documentation
├── src/             # Source code
├── tests/           # Tests
└── README.md        # This file
```

## Getting Started

1. Start Phase G (Generate):
   ```bash
   gaia phase generate
   ```

2. Track your progress:
   ```bash
   gaia status
   ```

## Documentation

- GAIA Framework: https://github.com/anthropics/claude-code
- Project docs: See `docs/` directory

---

Created with GAIA Quick Start on {datetime.now().strftime("%Y-%m-%d")}
"""

    readme_file = project_path / "README.md"
    with open(readme_file, "w", encoding="utf-8") as f:
        f.write(readme_content)

    print(f"  Created: README.md")

def create_gitignore(project_path: Path) -> None:
    """Create .gitignore file"""
    gitignore_content = """# GAIA state (can be regenerated)
.gaia/state.json

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
"""

    gitignore_file = project_path / ".gitignore"
    with open(gitignore_file, "w", encoding="utf-8") as f:
        f.write(gitignore_content)

    print(f"  Created: .gitignore")

def create_initial_docs(project_path: Path, project_name: str) -> None:
    """Create initial documentation files"""
    # Create phase-g.md for Phase G notes
    phase_g_content = f"""# Phase G: Generate

**Project**: {project_name}
**Date**: {datetime.now().strftime("%Y-%m-%d")}

## Problem Statement

<!-- Describe the problem you're trying to solve -->

## Solution Path

- [ ] Market First: Search for existing solutions
- [ ] GitHub First: Learn from similar projects
- [ ] Masters First: Research expert methodologies

## Research Notes

<!-- Add your research findings here -->

## Solution Outline

<!-- Define your solution approach -->

---

Next: [Phase A: Analyze](phase-a.md)
"""

    with open(project_path / "docs" / "phase-g.md", "w", encoding="utf-8") as f:
        f.write(phase_g_content)
    print(f"  Created: docs/phase-g.md")

    # Create phase-a.md template
    phase_a_content = """# Phase A: Analyze

**Date**: <!-- TODO: Add date -->

## MVP Definition

### P0 (Core - Must Complete)
-
-

### P1 (Important - Should Complete)
-
-

### P2 (Optional - Nice to Have)
-
-

## Task Breakdown

| ID | Task | Priority | Status |
|----|------|----------|--------|
| T1 | <!-- Task name --> | P0 | Pending |

---

Back: [Phase G: Generate](phase-g.md) | Next: [Phase I: Implement](phase-i.md)
"""

    with open(project_path / "docs" / "phase-a.md", "w", encoding="utf-8") as f:
        f.write(phase_a_content)
    print(f"  Created: docs/phase-a.md")

def main():
    """Main quick start flow"""
    print_header("GAIA Quick Start")

    print("This script will help you initialize a new GAIA project.")
    print("You'll be asked for some basic information about your project.\n")

    # Step 1: Project name
    print_step(1, "Enter your project name")
    project_name = get_input("Project name", "my-gaia-project")
    print()

    # Step 2: Problem statement
    print_step(2, "Describe the problem you want to solve")
    print("  This will help guide the GAIA framework through Phase G (Generate).")
    problem = get_input("Problem statement", "I need to solve a specific problem")
    print()

    # Step 3: Description
    print_step(3, "Enter a short description for your project")
    description = get_input("Description", f"{project_name} - A GAIA framework project")
    print()

    # Step 4: Location
    print_step(4, "Choose project location")
    current_dir = os.getcwd()
    use_current = confirm(f"Create project in current directory? ({current_dir})", default=False)

    if use_current:
        base_path = Path(current_dir)
    else:
        custom_path = get_input("Enter path", str(Path.home() / "projects"))
        base_path = Path(custom_path)
    print()

    # Summary
    print_header("Project Summary")
    print(f"  Project Name: {project_name}")
    print(f"  Problem: {problem}")
    print(f"  Location: {base_path / project_name}")
    print()

    if not confirm("Create project?", default=True):
        print("\nCancelled. No files were created.")
        return

    # Create project
    print_header("Creating Project...")

    project_path = create_project_directory(project_name, base_path)
    create_initial_state(project_path, project_name, problem)
    create_readme(project_path, project_name, description)
    create_gitignore(project_path)
    create_initial_docs(project_path, project_name)

    print_header("Project Created!")
    print(f"Your GAIA project '{project_name}' is ready.")
    print(f"\nNext steps:")
    print(f"  1. cd {project_path}")
    print(f"  2. Edit docs/phase-g.md to start Phase G")
    print(f"  3. Run: gaia status (if CLI is installed)")
    print(f"\nFor more information, see docs/getting-started.md")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
