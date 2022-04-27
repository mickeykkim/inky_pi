"""Console script for inky_pi."""
import click

import inky_pi.main
import inky_pi.main_goodnight
import inky_pi.main_weather


@click.group()
def cli():
    """CLI group for inky_pi."""


@cli.command()
@click.option("--dry-run", is_flag=True, default=False, help="Dry run")
def inky(dry_run: bool):
    """Console script for inky_pi train and weather."""
    if not dry_run:
        inky_pi.main.main()


@cli.command()
@click.option("--dry-run", is_flag=True, default=False, help="Dry run")
def weather(dry_run: bool):
    """Console script for inky_pi weather extended forecast."""
    if not dry_run:
        inky_pi.main_weather.main()


@cli.command()
@click.option("--dry-run", is_flag=True, default=False, help="Dry run")
def night(dry_run: bool):
    """Console script for inky_pi night mode."""
    if not dry_run:
        inky_pi.main_goodnight.main()


def main():
    """CLI main method."""
    cli()


if __name__ == "__main__":
    main()
