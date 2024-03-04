"""Console script for inky_pi."""
import click
from click import BaseCommand
from loguru import logger

from inky_pi import __version__
from inky_pi.__main__ import OUTPUT_DISPATCH_TABLE, DisplayOption, display_data
from inky_pi.util import configure_logging

OUTPUT_PREFIX = "inky_pi cli"


@click.group()
def cli() -> BaseCommand:
    """CLI group for inky_pi."""
    return cli


@cli.command()
@click.version_option(version=__version__)
@click.option(
    "-o", "--option", default="train", help="Display option (train, weather, night)"
)
@click.option(
    "-m", "--output", default="inky", help="Output source (inky, terminal, desktop)"
)
@click.option("--dry-run", is_flag=True, default=False, help="Dry run")
def display(option: str, output: str, dry_run: bool) -> None:
    """Console script for inky_pi train and weather."""
    if dry_run:
        logger.debug(
            "Dry run: {prefix} option = {option} / output = {output}",
            prefix=OUTPUT_PREFIX,
            option=option.lower(),
            output=output.lower(),
        )
        click.echo(
            f"Dry run: {OUTPUT_PREFIX} option ="
            f" {DisplayOption[option.upper()].name.lower()} / output ="
            f" {OUTPUT_DISPATCH_TABLE[output.upper()].model.name.lower()}"
        )
        return

    display_data(DisplayOption[option.upper()], OUTPUT_DISPATCH_TABLE[output.upper()])


def main() -> None:
    """CLI main method."""
    configure_logging()
    logger.debug("InkyPi cli initialized")
    cli()


if __name__ == "__main__":
    main()
