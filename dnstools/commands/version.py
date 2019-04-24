import click
from dnstools.cli import pass_context

@click.command('version')
@pass_context
def cli(ctx):
    """outputs version information"""
    ctx.echo('%s' % ctx.version)
    ctx.vecho('verbose mode')
