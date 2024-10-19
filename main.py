import click
import pandas as pd


@click.group()
def cli():
    """A UFC Prediction Command Line Tool"""
    pass


@cli.command()
def predict():
    """Return the prediction for the upcoming UFC event."""
    # TODO
    return


if __name__ == '__main__':
    cli()
