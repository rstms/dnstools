#!/usr/bin/env

import click
import os

CONTEXT_SETTINGS = dict(auto_envvar_prefix='DNSTOOLS')

class Context(object):
    def __init__(self):
        self.verbose = False
        self.version = 'Version 1.0'
   
    def echo(self, msg):
        click.echo(msg)

    def vecho(self, msg):
        if self.verbose:
            self.echo(msg)

pass_context = click.make_pass_decorator(Context, ensure=True)
command_dir = os.path.join(os.path.dirname(__file__), 'commands')

class CmdCLI(click.MultiCommand):
    def list_commands(self, ctx):
        cmds = []
        for filename in os.listdir(command_dir):
            if not filename.startswith('_') and filename.endswith('.py'):
                cmds.append(filename[:-3])
        cmds.sort()
        return cmds

    def get_command(self, ctx, name):
        ns = {}
        fn = os.path.join(command_dir, name + '.py')
        with open(fn) as f:
            code = compile(f.read(), fn, 'exec')
            eval(code, ns, ns)
        return ns['cli']

@click.command(cls=CmdCLI, context_settings=CONTEXT_SETTINGS)
@click.option('--verbose', is_flag=True, help='Enables verbose mode.')
@pass_context
def cli(ctx, verbose):
    ctx.verbose = verbose
