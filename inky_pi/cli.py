"""Console script for inky_pi."""
import click
from click import BaseCommand
from loguru import logger

from inky_pi.__init__ import __version__  # type: ignore
from inky_pi.__main__ import OUTPUT_HANDLER, DisplayOption, display_data
from inky_pi.util import configure_logging

OUTPUT_PREFIX = "inky_pi cli"


@click.group()
def cli() -> BaseCommand:
    """CLI group for inky_pi."""


@cli.command()
@click.version_option(version=__version__)
@click.option(
    "-o", "--option", default="train", help="Display option (train, weather, night)"
)
@click.option(
    "-m", "--output", default="inky", help="Output source (inky, terminal, desktop)"
)
@click.option("--dry-run", is_flag=True, default=False, help="Dry run")
def display(option: str, output: str, dry_run: bool):
    """Console script for inky_pi train and weather."""
    click.echo(
        f"{OUTPUT_PREFIX}"
        f" {DisplayOption[option.upper()]}"
        f" {OUTPUT_HANDLER[output.lower()].model}"
    )
    if not dry_run:
        display_data(DisplayOption[option.upper()], OUTPUT_HANDLER[output.lower()])


def main() -> None:
    """CLI main method."""
    configure_logging()
    logger.debug("InkyPi cli initialized")
    cli()


if __name__ == "__main__":
    main()
