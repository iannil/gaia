#!/usr/bin/env python3
"""
GAIA Framework Demo

This script demonstrates the core features of the GAIA framework:
- Phase execution (Generate → Analyze → Implement → Acceptance)
- State management and persistence
- Task management with priorities
- Knowledge graph operations
- Template usage
- Workflow execution
"""

from pathlib import Path
import tempfile
import json

from gaia_core import (
    GAIAEngine, Phase, PhaseStatus, Priority, GeneratePath,
    GAIAState, StateStore, Task
)
from gaia_knowledge import (
    KnowledgeGraph, Node, Edge,
    SemanticSearch, DocumentIndex,
    PatternLibrary
)
from gaia_templates import TemplateEngine
from gaia_workflow import WorkflowParser, WorkflowExecutor
from gaia_skills import (
    SkillManager, SkillMetadata,
    EvolutionManager, EvolutionRecord
)


def print_section(title: str) -> None:
    """Print a formatted section header"""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}\n")


def demo_gaia_engine():
    """Demonstrate GAIA Engine execution"""
    print_section("GAIA Engine Demo")

    # Create a temporary directory for the demo
    with tempfile.TemporaryDirectory() as tmpdir:
        base_path = Path(tmpdir)
        engine = GAIAEngine("demo-project", base_path=base_path)

        # Phase G: Generate
        print("Starting Phase G (Generate)...")
        success, error = engine.start_generate(
            "Build a CLI todo application with GAIA framework",
            path=GeneratePath.MARKET_FIRST
        )
        print(f"  Phase G started: {success}")

        # Set solution outline
        engine.set_solution_outline(
            "Use GAIA framework with Click for CLI, "
            "implement CRUD operations with JSON storage"
        )
        print(f"  Solution outline set")

        # Check status
        status = engine.get_status()
        print(f"  Current phase: {status['current_phase']['label']}")
        print(f"  Phase status: {status['current_phase']['status']}")

        # Advance to Phase A
        print("\nAdvancing to Phase A (Analyze)...")
        success, error = engine.advance_phase()
        print(f"  Phase A started: {success}")

        # Add tasks
        engine.add_task("Design CLI interface", Priority.P0)
        engine.add_task("Implement storage layer", Priority.P0)
        engine.add_task("Add tests", Priority.P1)
        print(f"  Added 3 tasks")

        status = engine.get_status()
        print(f"  Current phase: {status['current_phase']['label']}")
        print(f"  Total tasks: {status['tasks']['total']}")
        print(f"  P0 tasks: {status['tasks']['by_priority']['P0']}")

        # Export evolution data
        evolution_path = engine.export_evolution(base_path / "evolution.json")
        print(f"\n  Evolution data exported to: {evolution_path}")


def demo_knowledge_graph():
    """Demonstrate Knowledge Graph operations"""
    print_section("Knowledge Graph Demo")

    graph = KnowledgeGraph()

    # Add nodes
    cli_node = Node(id="cli", type="technology", label="CLI Application")
    click_node = Node(id="click", type="library", label="Click Framework")
    json_node = Node(id="json", type="storage", label="JSON Storage")

    graph.add_node(cli_node)
    graph.add_node(click_node)
    graph.add_node(json_node)

    print(f"Added {graph.count()} nodes")

    # Add edges
    edge1 = Edge(id="e1", source="cli", target="click", relation="uses", weight=1.0)
    edge2 = Edge(id="e2", source="cli", target="json", relation="stores_data_in", weight=0.8)
    edge3 = Edge(id="e3", source="click", target="json", relation="compatible_with", weight=0.5)

    graph.add_edge(edge1)
    graph.add_edge(edge2)
    graph.add_edge(edge3)

    print(f"Added {len(graph.edges)} edges")

    # Find related nodes
    related = graph.find_related("cli", max_depth=2)
    print(f"\nRelated nodes to 'cli': {[n.id for n in related]}")

    # Shortest path
    path = graph.shortest_path("click", "json")
    print(f"Shortest path from Click to JSON: {path}")

    # Centrality
    centrality = graph.get_centrality()
    print(f"\nNode centrality scores:")
    for node_id, score in sorted(centrality.items(), key=lambda x: -x[1])[:3]:
        print(f"  {node_id}: {score:.3f}")


def demo_semantic_search():
    """Demonstrate Semantic Search"""
    print_section("Semantic Search Demo")

    search_engine = SemanticSearch()

    # Add documents
    search_engine.index.add_document(
        "doc1",
        title="Click Framework",
        content="Click is a Python package for creating beautiful command line interfaces",
        doc_type="library",
        metadata={"tags": ["cli", "python", "framework"]}
    )
    search_engine.index.add_document(
        "doc2",
        title="Rich Library",
        content="Rich is a library for rendering rich text and formatting in terminal",
        doc_type="library",
        metadata={"tags": ["cli", "terminal", "formatting"]}
    )
    search_engine.index.add_document(
        "doc3",
        title="GAIA Framework",
        content="GAIA is a framework for systematic problem solving with AI",
        doc_type="framework",
        metadata={"tags": ["ai", "framework", "methodology"]}
    )

    # Search
    results = search_engine.search("command line interface")
    print(f"Search 'command line interface':")
    for result in results:
        print(f"  {result.id}: {result.score:.2f}")
        doc = search_engine.index.get_document(result.id)
        if doc:
            content = doc.get("content", "")[:50]
            print(f"    {content}...")

    # Add alias and expand query
    search_engine.add_alias("cli", ["command line", "command-line"])
    suggestions = search_engine.expand_query("cli tool")
    print(f"\nQuery expansions for 'cli tool': {suggestions}")


def demo_template_engine():
    """Demonstrate Template Engine"""
    print_section("Template Engine Demo")

    engine = TemplateEngine()
    engine.load_builtin_templates()

    # List templates
    templates = engine.list_templates()
    print(f"Available templates: {[t.id for t in templates]}")

    # Render phase startup template
    template = engine.get("phase-startup")
    if template:
        result = engine.render(
            "phase-startup",
            values={
                "phase": "Generate",
                "goal": "Build a todo CLI app",
                "mindset": "Expert Thinking"
            }
        )
        print(f"\nRendered 'phase-startup' template:")
        print(f"  {result[:100]}...")


def demo_pattern_library():
    """Demonstrate Pattern Library"""
    print_section("Pattern Library Demo")

    library = PatternLibrary()
    library.load_builtin_patterns()

    print(f"Total patterns: {library.count()}")

    # Get best practices
    best_practices = library.get_best_practices()
    print(f"\nBest practices ({len(best_practices)}):")
    for pattern in best_practices[:3]:
        print(f"  - {pattern.title}: {pattern.description[:50]}...")

    # Get anti-patterns
    anti_patterns = library.get_anti_patterns()
    print(f"\nAnti-patterns ({len(anti_patterns)}):")
    for pattern in anti_patterns[:3]:
        print(f"  - {pattern.title}: {pattern.description[:50]}...")

    # Search patterns
    results = library.search("test")
    print(f"\nSearch 'test': {len(results)} results")
    for pattern in results[:2]:
        print(f"  - {pattern.title}")


def demo_workflow():
    """Demonstrate Workflow execution"""
    print_section("Workflow Demo")

    workflow_yaml = """
id: demo-workflow
name: Demo Workflow
description: A simple demo workflow

triggers:
  - type: manual

steps:
  - id: step1
    action: log
    params:
      message: "Starting workflow..."

  - id: step2
    action: log
    params:
      message: "Processing data..."
    depends_on: [step1]

  - id: step3
    action: log
    params:
      message: "Workflow complete!"
    depends_on: [step2]
"""

    # Parse workflow
    parser = WorkflowParser()
    workflow = parser.parse(workflow_yaml)
    print(f"Parsed workflow: {workflow.name}")
    print(f"  Steps: {len(workflow.steps)}")
    print(f"  Triggers: {len(workflow.triggers)}")

    # Show workflow structure
    print(f"\nWorkflow structure:")
    for step in workflow.steps:
        deps = step.depends_on if step.depends_on else []
        print(f"  {step.id}: {step.action} (depends_on: {deps})")

    print("\n  (Note: Async execution requires running with asyncio)")


def demo_evolution_manager():
    """Demonstrate Evolution Manager"""
    print_section("Evolution Manager Demo")

    with tempfile.TemporaryDirectory() as tmpdir:
        manager = EvolutionManager(base_path=Path(tmpdir))

        # Create a record
        record = manager.create(
            skill_id="demo-skill",
            skill_name="Demo Skill"
        )
        record.description = "Demonstration skill for evolution tracking"

        # Record effective parameters
        record.record_parameter("output_format", "json", "JSON is easier to parse")
        record.record_parameter("log_level", "INFO", "Good balance of verbosity")

        # Record success pattern
        record.record_success_pattern(
            "Always validate inputs before processing",
            context="User input handling",
            outcome="Prevented 3 potential crashes in testing"
        )

        # Record anti-pattern
        record.record_anti_pattern(
            "Don't use global state for configuration",
            why_fails="Causes race conditions in multi-threaded execution",
            alternative="Use dependency injection instead"
        )

        # Save the record
        manager.save_record(record)

        print(f"Created evolution record for: {record.skill_name}")
        print(f"  Parameters: {len(record.effective_parameters)}")
        print(f"  Success patterns: {len(record.success_patterns)}")
        print(f"  Anti-patterns: {len(record.anti_patterns)}")

        # Retrieve the record
        retrieved = manager.get_record("demo-skill")
        print(f"\nRetrieved record: {retrieved.description if retrieved else 'Not found'}")


def demo_state_persistence():
    """Demonstrate State Persistence"""
    print_section("State Persistence Demo")

    with tempfile.TemporaryDirectory() as tmpdir:
        base_path = Path(tmpdir)
        store = StateStore(base_path / ".gaia")

        # Create and save state
        state = GAIAState(
            project_id="demo-persistence",
            project_name="State Persistence Demo"
        )

        state.add_task("Task 1", Priority.P0)
        state.add_task("Task 2", Priority.P1)
        state.problem_statement = "Demonstrate state persistence"
        state.solution_outline = "Use JSON for storage"

        store.save(state)
        print(f"Saved state with {len(state.tasks)} tasks")

        # Load state
        loaded = store.load("demo-persistence")
        if loaded:
            print(f"Loaded state:")
            print(f"  Project: {loaded.project_name}")
            print(f"  Tasks: {len(loaded.tasks)}")
            print(f"  Current phase: {loaded.current_phase.label}")
            print(f"  Problem: {loaded.problem_statement}")


def main():
    """Run all demos"""
    print("\n" + "=" * 60)
    print("  GAIA Framework Feature Demonstration")
    print("=" * 60)

    try:
        demo_gaia_engine()
        demo_knowledge_graph()
        demo_semantic_search()
        demo_template_engine()
        demo_pattern_library()
        demo_workflow()
        demo_evolution_manager()
        demo_state_persistence()

        print_section("Demo Complete!")
        print("All GAIA framework features demonstrated successfully.")
        print("For more information, see docs/getting-started.md\n")

    except Exception as e:
        print(f"\nDemo failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
