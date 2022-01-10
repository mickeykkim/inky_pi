"""Console script for inky_pi."""
import click

import inky_pi.goodnight
import inky_pi.main


@click.group()
def cli():
    """CLI group for inky_pi."""
    ...


@cli.command()
def inky():
    """Console script for inky_pi main."""
    inky_pi.main.main()


@cli.command()
def goodnight():
    """Console script for inky_pi goodnight."""
    inky_pi.goodnight.main()


def main():
    """CLI main method."""
    cli()


if __name__ == "__main__":
    main()
