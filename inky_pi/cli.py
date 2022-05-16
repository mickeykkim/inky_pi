"""Console script for inky_pi."""
import click
from loguru import logger

import inky_pi.main
from inky_pi.util import configure_logging


@click.group()
def cli():
    """CLI group for inky_pi."""


@cli.command()
@click.option("--dry-run", is_flag=True, default=False, help="Dry run")
def train(dry_run: bool):
    """Console script for inky_pi train and weather."""
    click.echo("CLI inky_pi train")
    if not dry_run:
        inky_pi.main.main()


@cli.command()
@click.option("--dry-run", is_flag=True, default=False, help="Dry run")
def weather(dry_run: bool):
    """Console script for inky_pi weather extended forecast."""
    click.echo("CLI inky_pi weather")
    if not dry_run:
        inky_pi.main.weather()


@cli.command()
@click.option("--dry-run", is_flag=True, default=False, help="Dry run")
def night(dry_run: bool):
    """Console script for inky_pi night mode."""
    click.echo("CLI inky_pi night")
    if not dry_run:
        inky_pi.main.night()


@cli.command()
@click.option("--dry-run", is_flag=True, default=False, help="Dry run")
def terminal(dry_run: bool):
    """Console script for terminal mode."""
    click.echo("CLI inky_pi terminal")
    if not dry_run:
        inky_pi.main.terminal()


@cli.command()
@click.option("--dry-run", is_flag=True, default=False, help="Dry run")
def desktop(dry_run: bool):
    """Console script for desktop mode."""
    click.echo("CLI inky_pi desktop")
    if not dry_run:
        inky_pi.main.desktop()


def main():
    """CLI main method."""
    configure_logging()
    logger.debug("InkyPi initialized")
    cli()


if __name__ == "__main__":
    main()
