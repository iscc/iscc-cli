# -*- coding: utf-8 -*-
import click


@click.command()
def cli():
    click.echo('Hello ISCC!')


if __name__ == '__main__':
    cli()
