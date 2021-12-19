# -*- coding: utf-8 -*-
import json
import click
import iscc
from iscc_core.codec import Code
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
    code_obj = Code(iscc_code)
    idx: iscc.index.Index = ctx.obj.index
    key = idx.add(code_obj)
    click.echo("Added with key: %s" % key)


@click.command(name="get")
@click.argument("iscc_code", nargs=1)
@click.pass_context
def get(ctx, iscc_code):
    """Get ISCC from database."""
    code_obj = Code(iscc_code)
    idx: iscc.index.Index = ctx.obj.index
    key = idx.get_key(code_obj)
    result = idx.get_metadata(key)
    if result:
        click.echo(json.dumps(result, indent=2))


@click.command(name="search")
@click.argument("iscc_code", nargs=1)
@click.pass_context
def search(ctx, iscc_code):
    """Search ISCC (nearest neighbors)."""
    code_obj = Code(iscc_code)
    idx: iscc.index.Index = ctx.obj.index
    result = idx.query(code_obj)
    click.echo(result.json(indent=2))


@click.command(name="list")
@click.pass_context
def list(ctx):
    """List ISCCs from database."""
    idx: iscc.index.Index = ctx.obj.index
    for entry in idx.iter_isccs():
        code_obj = Code(entry)
        click.echo(code_obj)


@click.command(name="stats")
@click.pass_context
def stats(ctx):
    """Show database statistics."""
    idx: iscc.index.Index = ctx.obj.index
    click.echo(json.dumps(idx.stats, indent=2))


@click.command(name="destroy")
@click.pass_context
def destroy(ctx):
    """Delete database from disk."""
    idx: iscc.index.Index = ctx.obj.index
    idx.destroy()


db.add_command(list)
db.add_command(add)
db.add_command(get)
db.add_command(search)
db.add_command(stats)
db.add_command(destroy)
