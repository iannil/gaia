"""
GAIA CLI - Commands

CLI 命令实现。
"""

from pathlib import Path
from typing import Optional, List
import sys

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

# 导入 GAIA 核心模块
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from gaia_core import GAIAEngine, Phase, Priority, GeneratePath
from gaia_skills import SkillManager, EvolutionManager
from gaia_templates import TemplateEngine
from gaia_workflow import WorkflowExecutor, WorkflowBuilder, Actions

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def cli() -> None:
    """GAIA - AI 协作问题解决框架"""
    pass


# ========== gaia init ==========

@cli.command()
@click.argument("project_name")
@click.option("--path", type=click.Path(), default=None, help="项目路径")
def init(project_name: str, path: Optional[str]) -> None:
    """初始化新项目

    示例:
        gaia init my-project
        gaia init my-project --path ./projects
    """
    base_path = Path(path) if path else Path.cwd()
    engine = GAIAEngine(project_name, base_path)

    console.print(f"[green]✓[/green] 项目初始化成功: {project_name}")
    console.print(f"  状态文件: {base_path / '.gaia' / 'state.json'}")
    console.print("\n使用 [cyan]gaia phase[/cyan] 开始 GAIA 流程")


# ========== gaia phase ==========

@cli.group()
def phase() -> None:
    """阶段管理"""
    pass


@phase.command("status")
@click.option("--project", default=None, help="项目名称")
def phase_status(project: Optional[str]) -> None:
    """查看当前阶段状态"""
    # 获取项目
    project_name = project or _get_current_project()
    if not project_name:
        console.print("[red]错误: 未指定项目[/red]")
        return

    engine = GAIAEngine(project_name)
    status = engine.get_status()

    # 显示状态
    console.print(Panel.fit(f"[bold]项目: {status['project']}[/bold]"))

    # 当前阶段
    current = status["current_phase"]
    console.print(f"\n当前阶段: [cyan]{current['label']} ({current['phase']})[/cyan]")
    console.print(f"思维模式: {current['mindset']}")
    console.print(f"状态: {_status_badge(current['status'])}")

    # 各阶段状态
    console.print("\n[bold]各阶段状态:[/bold]")
    for phase_value, phase_info in status["phases"].items():
        phase_label = phase_info["label"]
        phase_status = phase_info["status"]
        console.print(f"  {phase_label}: {_status_badge(phase_status)}")


@phase.command("generate")
@click.argument("problem_statement")
@click.option("--project", default=None, help="项目名称")
@click.option("--path", type=click.Choice(["market", "github", "masters"]), default="market", help="解决方案路径")
def phase_generate(
    problem_statement: str,
    project: Optional[str],
    path: str,
) -> None:
    """启动 Phase G: 生成

    示例:
        gaia phase generate "需要实现用户认证功能"
        gaia phase generate "需要实现用户认证功能" --path github
    """
    project_name = project or _get_current_project()
    if not project_name:
        console.print("[red]错误: 未指定项目[/red]")
        return

    # 转换路径
    path_map = {
        "market": GeneratePath.MARKET_FIRST,
        "github": GeneratePath.GITHUB_FIRST,
        "masters": GeneratePath.MASTERS_FIRST,
    }

    engine = GAIAEngine(project_name)
    success, error = engine.start_generate(problem_statement, path_map[path])

    if success:
        console.print("[green]✓[/green] Phase G 启动成功")
        console.print(f"  问题陈述: {problem_statement}")
        console.print(f"  解决路径: {path}")

        # 提示下一步
        console.print("\n下一步:")
        console.print("  1. 使用 [cyan]gaia phase set-outline[/cyan] 设置解决方案大纲")
        console.print("  2. 使用 [cyan]gaia phase advance[/cyan] 进入下一阶段")
    else:
        console.print(f"[red]✗[/red] Phase G 启动失败: {error}")


@phase.command("set-outline")
@click.argument("outline")
@click.option("--project", default=None, help="项目名称")
def phase_set_outline(outline: str, project: Optional[str]) -> None:
    """设置解决方案大纲"""
    project_name = project or _get_current_project()
    if not project_name:
        console.print("[red]错误: 未指定项目[/red]")
        return

    engine = GAIAEngine(project_name)
    engine.set_solution_outline(outline)

    console.print("[green]✓[/green] 解决方案大纲已更新")


@phase.command("advance")
@click.option("--project", default=None, help="项目名称")
def phase_advance(project: Optional[str]) -> None:
    """推进到下一阶段"""
    project_name = project or _get_current_project()
    if not project_name:
        console.print("[red]错误: 未指定项目[/red]")
        return

    engine = GAIAEngine(project_name)
    success, error = engine.advance_phase()

    if success:
        console.print(f"[green]✓[/green] 已推进到阶段: {engine.current_phase.label}")
    else:
        console.print(f"[red]✗[/red] 推进失败: {error}")


# ========== gaia skill ==========

@cli.group()
def skill() -> None:
    """Skill 管理"""
    pass


@skill.command("install")
@click.argument("source")
@click.option("--id", default=None, help="Skill ID")
def skill_install(source: str, id: Optional[str]) -> None:
    """安装 Skill

    示例:
        gaia skill install anthropics/skills
        gaia skill install https://github.com/user/repo.git
    """
    manager = SkillManager()

    if source.startswith("http"):
        # Git URL
        success, message = manager.install_from_git(source, id)
    elif "/" in source:
        # GitHub repo
        success, message = manager.install_from_github(source, id)
    else:
        console.print("[red]错误: 无效的来源[/red]")
        console.print("  支持的格式:")
        console.print("    - GitHub 仓库: owner/repo")
        console.print("    - Git URL: https://github.com/owner/repo.git")
        return

    if success:
        console.print(f"[green]✓[/green] {message}")
    else:
        console.print(f"[red]✗[/red] {message}")


@skill.command("list")
@click.option("--category", default=None, help="分类筛选")
@click.option("--tag", default=None, help="标签筛选")
def skill_list(category: Optional[str], tag: Optional[str]) -> None:
    """列出已安装的 Skills"""
    manager = SkillManager()
    skills = manager.list_skills(category=category, tag=tag)

    if not skills:
        console.print("[yellow]未找到已安装的 Skills[/yellow]")
        return

    table = Table(title="已安装的 Skills")
    table.add_column("ID", style="cyan")
    table.add_column("名称", style="green")
    table.add_column("版本")
    table.add_column("分类")
    table.add_column("描述")

    for skill in skills:
        table.add_row(
            skill["id"],
            skill["name"],
            skill["version"],
            skill["category"],
            skill["description"][:30] + "..." if len(skill["description"]) > 30 else skill["description"],
        )

    console.print(table)


@skill.command("search")
@click.argument("query")
def skill_search(query: str) -> None:
    """搜索已安装的 Skills"""
    manager = SkillManager()
    results = manager.search_skills(query)

    if not results:
        console.print(f"[yellow]未找到匹配 '{query}' 的 Skills[/yellow]")
        return

    console.print(f"\n找到 [cyan]{len(results)}[/cyan] 个匹配的 Skills:\n")

    for skill in results:
        console.print(f"  [cyan]{skill['name']}[/cyan] ({skill['id']})")
        console.print(f"    {skill['description']}")
        console.print(f"    标签: {', '.join(skill['tags'])}")
        console.print()


@skill.command("update")
@click.argument("skill_id")
def skill_update(skill_id: str) -> None:
    """更新 Skill"""
    manager = SkillManager()
    success, message = manager.update(skill_id)

    if success:
        console.print(f"[green]✓[/green] {message}")
    else:
        console.print(f"[red]✗[/red] {message}")


@skill.command("uninstall")
@click.argument("skill_id")
@click.option("--keep-files", is_flag=True, help="保留文件")
def skill_uninstall(skill_id: str, keep_files: bool) -> None:
    """卸载 Skill"""
    manager = SkillManager()
    success, message = manager.uninstall(skill_id, keep_files)

    if success:
        console.print(f"[green]✓[/green] {message}")
    else:
        console.print(f"[red]✗[/red] {message}")


@skill.command("info")
@click.argument("skill_id")
def skill_info(skill_id: str) -> None:
    """查看 Skill 详情"""
    manager = SkillManager()
    info = manager.get_skill_info(skill_id)

    if not info:
        console.print(f"[red]错误: Skill '{skill_id}' 未找到[/red]")
        return

    console.print(Panel.fit(f"[bold]{info['name']}[/bold]"))
    console.print(f"ID: {info['id']}")
    console.print(f"版本: {info['version']}")
    console.print(f"分类: {info['category']}")
    console.print(f"描述: {info['description']}")
    console.print(f"作者: {info.get('author', 'N/A')}")
    console.print(f"许可证: {info.get('license', 'N/A')}")
    console.print(f"来源: {info.get('source', 'N/A')}")
    console.print(f"标签: {', '.join(info.get('tags', []))}")


@skill.command("ls")
def skill_ls() -> None:
    """简短列出所有 Skills (简写命令)"""
    manager = SkillManager()
    skills = manager.list_skills()

    for skill in skills:
        status = "[green]✓[/green]" if skill.get("enabled", True) else "[red]✗[/red]"
        console.print(f"  {status} {skill['id']} - {skill['name']}")


# ========== gaia status ==========

@cli.command()
@click.option("--project", default=None, help="项目名称")
def status(project: Optional[str]) -> None:
    """查看项目状态"""
    project_name = project or _get_current_project()
    if not project_name:
        console.print("[red]错误: 未指定项目[/red]")
        console.print("提示: 使用 --project 指定项目，或在项目目录下运行")
        return

    engine = GAIAEngine(project_name)
    project_status = engine.get_status()

    console.print(Panel.fit(f"[bold]{project_status['project']}[/bold]"))

    # 当前阶段
    current = project_status["current_phase"]
    console.print(f"\n[bold]当前阶段:[/bold] {current['label']} ({current['phase']})")
    console.print(f"[bold]状态:[/bold] {_status_badge(current['status'])}")

    # 任务统计
    tasks = project_status["tasks"]
    console.print(f"\n[bold]任务统计:[/bold]")
    console.print(f"  总计: {tasks['total']}")
    console.print(f"  待办: {tasks['pending']}")
    console.print(f"  进行中: {tasks['in_progress']}")
    console.print(f"  已完成: {tasks['completed']}")
    console.print(f"  优先级分布: P0={tasks['by_priority']['P0']}, P1={tasks['by_priority']['P1']}, P2={tasks['by_priority']['P2']}")

    # 使用的 Skills
    if project_status["skills_used"]:
        console.print(f"\n[bold]使用的 Skills:[/bold]")
        for skill in project_status["skills_used"]:
            console.print(f"  - {skill}")


# ========== gaia evolve ==========

@cli.group()
def evolve() -> None:
    """演化记录管理"""
    pass


@evolve.command("record")
@click.argument("key")
@click.argument("value")
@click.option("--project", default=None, help="项目名称")
def evolve_record(key: str, value: str, project: Optional[str]) -> None:
    """记录演化数据"""
    project_name = project or _get_current_project()
    if not project_name:
        console.print("[red]错误: 未指定项目[/red]")
        return

    engine = GAIAEngine(project_name)
    engine.record_evolution(key, value)

    console.print(f"[green]✓[/green] 演化数据已记录: {key} = {value}")


@evolve.command("export")
@click.option("--project", default=None, help="项目名称")
@click.option("--output", "-o", type=click.Path(), default=None, help="输出文件")
def evolve_export(project: Optional[str], output: Optional[str]) -> None:
    """导出演化记录"""
    project_name = project or _get_current_project()
    if not project_name:
        console.print("[red]错误: 未指定项目[/red]")
        return

    engine = GAIAEngine(project_name)
    output_path = Path(output) if output else None
    path = engine.export_evolution(output_path)

    console.print(f"[green]✓[/green] 演化记录已导出: {path}")


# ========== gaia template ==========

@cli.group()
def template() -> None:
    """模板操作"""
    pass


@template.command("list")
@click.option("--category", default=None, help="分类筛选")
def template_list(category: Optional[str]) -> None:
    """列出可用模板"""
    engine = TemplateEngine()
    engine.load_builtin_templates()

    templates = engine.list_templates(category=category)

    if not templates:
        console.print("[yellow]未找到模板[/yellow]")
        return

    table = Table(title="可用模板")
    table.add_column("ID", style="cyan")
    table.add_column("名称", style="green")
    table.add_column("分类")
    table.add_column("描述")

    for t in templates:
        table.add_row(
            t.id,
            t.name,
            t.category,
            t.description[:40] + "..." if len(t.description) > 40 else t.description,
        )

    console.print(table)


@template.command("render")
@click.argument("template_id")
@click.option("--output", "-o", type=click.Path(), default=None, help="输出文件")
@click.option("--param", "-p", multiple=True, help="参数 (格式: key=value)")
def template_render(template_id: str, output: Optional[str], param: tuple) -> None:
    """渲染模板

    示例:
        gaia template render prd -o prd.md -p product_name=MyApp -p version=1.0
    """
    engine = TemplateEngine()
    engine.load_builtin_templates()

    # 解析参数
    values = {}
    for p in param:
        if "=" in p:
            key, value = p.split("=", 1)
            values[key] = value

    # 渲染
    result = engine.render(template_id, values)

    if result is None:
        console.print(f"[red]错误: 模板 '{template_id}' 未找到[/red]")
        return

    # 输出
    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(result)
        console.print(f"[green]✓[/green] 模板已渲染到: {output}")
    else:
        console.print(result)


@template.command("info")
@click.argument("template_id")
def template_info(template_id: str) -> None:
    """查看模板详情"""
    engine = TemplateEngine()
    engine.load_builtin_templates()

    template = engine.get(template_id)

    if not template:
        console.print(f"[red]错误: 模板 '{template_id}' 未找到[/red]")
        return

    console.print(Panel.fit(f"[bold]{template.name}[/bold]"))
    console.print(f"ID: {template.id}")
    console.print(f"分类: {template.category}")
    console.print(f"描述: {template.description}")

    if template.parameters:
        console.print("\n[bold]参数:[/bold]")
        for param_name, param_def in template.parameters.items():
            required = " [red]*[/red]" if param_def.get("required") else ""
            default = f" (默认: {param_def.get('default', '')})" if param_def.get("default") else ""
            desc = param_def.get("description", "")
            console.print(f"  {param_name}{required}{default}: {desc}")


# ========== gaia workflow ==========

@cli.group()
def workflow() -> None:
    """工作流操作"""
    pass


@workflow.command("run")
@click.argument("workflow_file", type=click.Path(exists=True))
@click.option("--var", "-v", multiple=True, help="变量 (格式: key=value)")
def workflow_run(workflow_file: str, var: tuple) -> None:
    """运行工作流

    示例:
        gaia workflow run workflow.yaml
    """
    from gaia_workflow import WorkflowParser

    # 解析工作流
    parser = WorkflowParser()
    workflow = parser.parse_file(workflow_file)

    # 验证
    errors = parser.validate(workflow)
    if errors:
        console.print("[red]工作流验证失败:[/red]")
        for error in errors:
            console.print(f"  - {error}")
        return

    # 解析变量
    variables = {}
    for v in var:
        if "=" in v:
            key, value = v.split("=", 1)
            variables[key] = value

    # 执行工作流
    console.print(f"\n[cyan]执行工作流: {workflow.name}[/cyan]\n")

    executor = WorkflowExecutor()
    execution = executor.execute_sync(workflow, variables)

    # 显示结果
    console.print(f"\n状态: {_status_badge(execution.status.value)}")
    console.print(f"执行时间: {execution.started_at} ~ {execution.completed_at}")

    if execution.results:
        console.print("\n[bold]步骤结果:[/bold]")
        for step_id, result in execution.results.items():
            console.print(f"  {step_id}: {_status_badge(result.status.value)}")
            if result.error:
                console.print(f"    错误: {result.error}")


@workflow.command("validate")
@click.argument("workflow_file", type=click.Path(exists=True))
def workflow_validate(workflow_file: str) -> None:
    """验证工作流定义"""
    from gaia_workflow import WorkflowParser

    parser = WorkflowParser()

    try:
        workflow = parser.parse_file(workflow_file)
        errors = parser.validate(workflow)

        if errors:
            console.print("[red]验证失败:[/red]")
            for error in errors:
                console.print(f"  - {error}")
        else:
            console.print("[green]✓[/green] 工作流定义有效")
            console.print(f"  ID: {workflow.id}")
            console.print(f"  名称: {workflow.name}")
            console.print(f"  步骤数: {len(workflow.steps)}")
            console.print(f"  触发器数: {len(workflow.triggers)}")

    except Exception as e:
        console.print(f"[red]解析失败: {e}[/red]")


# ========== 辅助函数 ==========

def _get_current_project() -> Optional[str]:
    """获取当前项目名称"""
    state_file = Path.cwd() / ".gaia" / "state.json"
    if state_file.exists():
        import json
        with open(state_file, "r") as f:
            data = json.load(f)
            return data.get("project_name")
    return None


def _status_badge(status: str) -> str:
    """获取状态徽章"""
    badges = {
        "pending": "[yellow]待办[/yellow]",
        "in_progress": "[blue]进行中[/blue]",
        "completed": "[green]已完成[/green]",
        "failed": "[red]失败[/red]",
        "skipped": "[dim]跳过[/dim]",
    }
    return badges.get(status, status)


__all__ = ["cli"]
