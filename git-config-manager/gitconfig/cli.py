"""Git-powered configuration management CLI.

This module provides the command-line interface using Click.
"""

from pathlib import Path

import click

from gitconfig.core.config_manager import ConfigManager
from gitconfig.exceptions import (
    BranchNotFoundError,
    ConfigNotFoundError,
    GitConfigError,
)
from gitconfig.models import ConfigFormat


@click.group()
@click.option(
    "--repo",
    "-r",
    type=click.Path(exists=True, path_type=Path),
    default=Path.cwd(),
    help="Path to the configuration repository",
)
@click.pass_context
def cli(ctx: click.Context, repo: Path) -> None:
    """Git-powered configuration management CLI.

    Manage versioned configurations using Git as the backend.
    """
    ctx.ensure_object(dict)
    try:
        ctx.obj["manager"] = ConfigManager.from_path(repo)
    except GitConfigError:
        ctx.obj["manager"] = None


@cli.command()
@click.argument("path", type=click.Path(path_type=Path))
@click.option("--branch", "-b", default="main", help="Initial branch name")
def init(path: Path, branch: str) -> None:
    """Initialize a new configuration repository."""
    try:
        ConfigManager.create(path, initial_branch=branch)
        click.echo(f"Initialized config repository at {path}")
    except GitConfigError as e:
        click.echo(f"Error: {e.message}", err=True)
        raise SystemExit(1) from None


@cli.command()
@click.argument("name")
@click.argument("content")
@click.option(
    "--format",
    "-f",
    "fmt",
    type=click.Choice(["json", "yaml"]),
    default="json",
    help="Configuration format",
)
@click.option("--message", "-m", default=None, help="Commit message")
@click.pass_context
def save(
    ctx: click.Context,
    name: str,
    content: str,
    fmt: str,
    message: str | None,
) -> None:
    """Save a configuration.

    NAME is the configuration name.
    CONTENT is the configuration content (JSON or YAML string).
    """
    manager: ConfigManager | None = ctx.obj.get("manager")
    if manager is None:
        click.echo("Error: Not in a config repository", err=True)
        raise SystemExit(1)

    try:
        import json

        import yaml

        format_enum = ConfigFormat.JSON if fmt == "json" else ConfigFormat.YAML
        parsed: dict = json.loads(content) if fmt == "json" else yaml.safe_load(content)

        from gitconfig.models import ConfigEntry

        config = ConfigEntry(name=name, content=parsed, format=format_enum)
        commit = manager.save(config, message=message)
        click.echo(f"Saved '{name}' in commit {commit.sha[:8]}")
    except GitConfigError as e:
        click.echo(f"Error: {e.message}", err=True)
        raise SystemExit(1) from None


@cli.command()
@click.argument("name")
@click.option("--branch", "-b", default=None, help="Branch to read from")
@click.option("--output", "-o", type=click.Path(path_type=Path), help="Output file")
@click.pass_context
def get(
    ctx: click.Context,
    name: str,
    branch: str | None,
    output: Path | None,
) -> None:
    """Get a configuration by name."""
    manager: ConfigManager | None = ctx.obj.get("manager")
    if manager is None:
        click.echo("Error: Not in a config repository", err=True)
        raise SystemExit(1)

    try:
        config = manager.get(name, branch=branch)

        # Format output
        from gitconfig.core.parsers import JsonParser, YamlParser

        parser = JsonParser() if config.format == ConfigFormat.JSON else YamlParser()
        content = parser.serialize(config.content)

        if output:
            output.write_text(content)
            click.echo(f"Saved to {output}")
        else:
            click.echo(content)
    except ConfigNotFoundError:
        click.echo(f"Error: Configuration '{name}' not found", err=True)
        raise SystemExit(1) from None


@cli.command("list")
@click.pass_context
def list_configs(ctx: click.Context) -> None:
    """List all configurations."""
    manager: ConfigManager | None = ctx.obj.get("manager")
    if manager is None:
        click.echo("Error: Not in a config repository", err=True)
        raise SystemExit(1)

    configs = manager.list_configs()
    if not configs:
        click.echo("No configurations found")
        return

    click.echo("Configurations:")
    for config in configs:
        click.echo(f"  - {config.name} ({config.format.value})")


@cli.command()
@click.argument("name")
@click.option("--message", "-m", default=None, help="Commit message")
@click.pass_context
def delete(ctx: click.Context, name: str, message: str | None) -> None:
    """Delete a configuration."""
    manager: ConfigManager | None = ctx.obj.get("manager")
    if manager is None:
        click.echo("Error: Not in a config repository", err=True)
        raise SystemExit(1)

    try:
        manager.delete(name, message=message)
        click.echo(f"Deleted '{name}'")
    except ConfigNotFoundError:
        click.echo(f"Error: Configuration '{name}' not found", err=True)
        raise SystemExit(1) from None


@cli.command()
@click.argument("branch_name")
@click.pass_context
def draft(ctx: click.Context, branch_name: str) -> None:
    """Create a draft branch for changes."""
    manager: ConfigManager | None = ctx.obj.get("manager")
    if manager is None:
        click.echo("Error: Not in a config repository", err=True)
        raise SystemExit(1)

    try:
        manager.create_draft(branch_name)
        click.echo(f"Created draft branch: {branch_name}")
    except GitConfigError as e:
        click.echo(f"Error: {e.message}", err=True)
        raise SystemExit(1) from None


@cli.command()
@click.argument("branch_name")
@click.pass_context
def switch(ctx: click.Context, branch_name: str) -> None:
    """Switch to a different branch."""
    manager: ConfigManager | None = ctx.obj.get("manager")
    if manager is None:
        click.echo("Error: Not in a config repository", err=True)
        raise SystemExit(1)

    try:
        manager.switch_to(branch_name)
        click.echo(f"Switched to: {branch_name}")
    except BranchNotFoundError:
        click.echo(f"Error: Branch '{branch_name}' not found", err=True)
        raise SystemExit(1) from None


@cli.command()
@click.argument("source_branch")
@click.option("--target", "-t", default="main", help="Target branch")
@click.option("--message", "-m", default=None, help="Merge commit message")
@click.pass_context
def merge(
    ctx: click.Context,
    source_branch: str,
    target: str,
    message: str | None,
) -> None:
    """Merge a draft branch."""
    manager: ConfigManager | None = ctx.obj.get("manager")
    if manager is None:
        click.echo("Error: Not in a config repository", err=True)
        raise SystemExit(1)

    try:
        result = manager.merge_draft(source_branch, target=target, message=message)
        if result.success:
            click.echo(f"Merged '{source_branch}' into '{target}'")
        else:
            click.echo(
                f"Merge conflicts in: {', '.join(str(f) for f in result.conflicts)}",
                err=True,
            )
            raise SystemExit(1)
    except GitConfigError as e:
        click.echo(f"Error: {e.message}", err=True)
        raise SystemExit(1) from None


@cli.command()
@click.argument("name")
@click.option("--limit", "-n", type=int, default=10, help="Max history entries")
@click.pass_context
def history(ctx: click.Context, name: str, limit: int) -> None:
    """Show version history for a configuration."""
    manager: ConfigManager | None = ctx.obj.get("manager")
    if manager is None:
        click.echo("Error: Not in a config repository", err=True)
        raise SystemExit(1)

    try:
        commits = manager.get_history(name, max_count=limit)
        if not commits:
            click.echo(f"No history for '{name}'")
            return

        click.echo(f"History for '{name}':")
        for commit in commits:
            date = commit.timestamp.strftime("%Y-%m-%d %H:%M")
            click.echo(f"  {commit.sha[:8]} - {date} - {commit.message}")
    except ConfigNotFoundError:
        click.echo(f"Error: Configuration '{name}' not found", err=True)
        raise SystemExit(1) from None


@cli.command()
@click.pass_context
def branches(ctx: click.Context) -> None:
    """List all branches."""
    manager: ConfigManager | None = ctx.obj.get("manager")
    if manager is None:
        click.echo("Error: Not in a config repository", err=True)
        raise SystemExit(1)

    branch_list = manager.list_branches()
    click.echo("Branches:")
    for branch in branch_list:
        marker = "* " if branch.is_current else "  "
        click.echo(f"{marker}{branch.name}")


def main() -> None:
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
