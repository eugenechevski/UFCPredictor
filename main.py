import click
import pandas as pd
from scraper import scrape_fighter_data

@click.group()
def cli():
    """A UFC Prediction Command Line Tool"""
    pass

@cli.command()
def scrape():
    """Scrape UFC fighter statistics"""
    df = scrape_fighter_data()
    click.echo("Scraping complete. Fighter data saved to data/fighters_stats.csv")
    df.to_csv('data/fighters_stats.csv', index=False)

@cli.command()
@click.option('--name', help='Fighter name to display stats for')
def show_stats(name):
    """Display fighter statistics by name"""
    df = pd.read_csv('data/fighters_stats.csv')
    fighter = df[df['Name'].str.contains(name, case=False)]
    if not fighter.empty:
        click.echo(fighter.to_string(index=False))
    else:
        click.echo(f"No fighter found with name {name}")

if __name__ == '__main__':
    cli()
