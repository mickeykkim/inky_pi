"""Console script for inky_pi."""
import click

import inky_pi.main as inky_main


@click.command()
def main():
    """Console script for inky_pi."""
    inky_main.main()
    return 0


if __name__ == "__main__":
    main()
