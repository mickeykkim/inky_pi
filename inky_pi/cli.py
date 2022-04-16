"""Console script for inky_pi."""
import click

import inky_pi.goodnight
import inky_pi.main
import inky_pi.main_weather


@click.group()
def cli():
    """CLI group for inky_pi."""


@cli.command()
def inky():
    """Console script for inky_pi train and weather."""
    inky_pi.main.main()


@cli.command()
def weather():
    """Console script for inky_pi weather extended forecast."""
    inky_pi.main_weather.main()


@cli.command()
def night():
    """Console script for inky_pi night mode."""
    inky_pi.goodnight.main()


def main():
    """CLI main method."""
    cli()


if __name__ == "__main__":
    main()
