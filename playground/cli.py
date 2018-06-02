# -*- coding: utf-8 -*-

"""Console script for playground."""

import click


@click.command()
def main(args=None):
    """Console script for playground."""
    click.echo("Replace this message by putting your code into "
               "playground.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")

@click.group()
def cli():
    pass

@cli.group()
def install(args=None):
    click.echo("Installing language binary")

@cli.install.command()
def download(args=None):
    click.echo("Downloading binary language version.")

@cli.install.command()
def link(args=None):
    click.echo("Linking to an existing language version.")

@cli.command()
def create(args=None):
    click.echo("Creating playground")

@cli.command()
def activate(args=None):
    click.echo("Activating playground")

@cli.command()
def ls(args=None):
    click.echo("Listing available playgrounds and languages")

@cli.command()
def clean(args=None):
    click.echo("Cleaning out unused playgrounds and language versions")

@cli.command()
def rm(args=None):
    click.echo("Deleting playground or language version")

@cli.command()
def run(args=None):
    click.echo("Run a arbitary command inside the playground environment")


if __name__ == "__main__":
    main()
