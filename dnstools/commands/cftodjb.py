import click
from dnstools.commands._cf import getzone
from dnstools.cli import pass_context

@click.command('cftodjb')
@click.argument('domain')
@click.argument('ip_address')
@click.option('-h', '--hostname', default='')
@pass_context
def cli(ctx, domain, ip_address, hostname):
    """outputs DOMAIN's cloudflare zone as djb tinydns data using IP-ADDRESS"""
    zone = getzone(domain)
    #print('.%s:%s:%s' % (domain, ip_address, hostname))
    for r in zone:
        if r['type'] == 'CNAME':
            print('C%s:%s' %( r['name'], r['content']))
        elif r['type'] == 'TXT':
            print('\'%s:%s' %( r['name'], r['content']))
        elif r['type'] == 'MX':
            pass
        elif r['type'] == 'A':
            print('=%s:%s' %( r['name'], r['content']))
        else:
            exit('unknown DNS record type: %s' % r['type'])
