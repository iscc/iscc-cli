# -*- coding: utf-8 -*-
import json

import click
import iscc
from click_default_group import DefaultGroup


@click.group(cls=DefaultGroup)
@click.pass_context
def db(ctx):
    """Manage ISCC database"""
    pass


@click.command(name="add")
@click.argument("iscc_code", nargs=1)
@click.pass_context
def add(ctx, iscc_code):
    """Add ISCC to database."""
    code_obj = iscc.Code(iscc_code)
    idx = ctx.obj.index
    key = idx.add(code_obj)
    click.echo("Added with key: %s" % key)


@click.command(name="search")
@click.argument("iscc_code", nargs=1)
@click.pass_context
def search(ctx, iscc_code):
    """Search ISCC (nearest neighbors)."""
    code_obj = iscc.Code(iscc_code)
    idx: iscc.Index = ctx.obj.index
    result = idx.query(code_obj)
    click.echo(result.json(indent=2))


@click.command(name="list")
@click.pass_context
def list(ctx):
    """List ISCCs from database."""
    idx = ctx.obj.index
    for entry in idx.iter_isccs():
        code_obj = iscc.Code(entry)
        click.echo(code_obj)


@click.command(name="stats")
@click.pass_context
def stats(ctx):
    """Show database statistics."""
    idx = ctx.obj.index
    click.echo(json.dumps(idx.stats, indent=2))


@click.command(name="destroy")
@click.pass_context
def destroy(ctx):
    """Delete database from disk."""
    idx = ctx.obj.index
    idx.destroy()


db.add_command(list)
db.add_command(add)
db.add_command(search)
db.add_command(stats)
db.add_command(destroy)
