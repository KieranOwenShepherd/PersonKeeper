""" a command line interface for managing records of people

dependencies - click, persons
"""

import click
import os.path
from persons import Record, Records

@click.group()
@click.argument('FILEPATH')
@click.pass_context
def cli(ctx, filepath):
    """Work with people records file (only csv supported currently)

    FILEPATH (str): filepath of a file to load, or save to if using add
    """    
    ctx.ensure_object(dict)
    ctx.obj['FILEPATH'] = filepath

    if os.path.isfile(filepath):
        ctx.obj['RECORDS'] = Records.from_file(filepath)
    else:
        ctx.obj['RECORDS'] = Records()

@cli.command()
@click.pass_context
@click.argument('name')
@click.argument('address')
@click.argument('phone')
def add(ctx, name, address, phone):
    """Add a new Record to the records file
    
    NAME (str): a persons name
    ADDRESS (str): the persons address
    PHONE (str): the persons phone number
    """

    ctx.obj['RECORDS'].add_record(Record(name=name, address=address, phone=phone))
    ctx.obj['RECORDS'].export(ctx.obj['FILEPATH'])


@cli.command()
@click.pass_context
@click.option('-n', '--name', default=None, help='return only results with matching name')
@click.option('-a', '--address', default=None, help='return only results with matching address')
@click.option('-p', '--phone', default=None, help='return only results with matching phone')
def display(ctx, name, address, phone):
    """ Show the contents of the records file, optionally filtering """

    click.echo(ctx.obj['RECORDS'].filter_records(name, address, phone).display())


@cli.command()
@click.pass_context
@click.argument('path')
@click.option('-n', '--name', default=None, help='return only results with matching name')
@click.option('-a', '--address', default=None, help='return only results with matching adress')
@click.option('-p', '--phone', default=None, help='return only results with matching phone')
def export(ctx, path, name, address, phone):
    """ Export to a different file, optionally filtering

    PATH (str): the path to the file to export to
    """ 

    ctx.obj['RECORDS'].filter_records(name, address, phone).export(path)
    

if __name__ == '__main__':
    cli(obj={})