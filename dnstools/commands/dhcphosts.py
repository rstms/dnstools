import click
from dnstools.cli import pass_context
from isc_dhcp_leases import IscDhcpLeases

import platform

if platform.system()=='OpenBSD':
   LEASE_FILE='/var/db/dhcpd.leases'
else:
   LEASE_FILE='/var/lib/dhcpd/dhcpd.leases'

@click.command()
@pass_context
@click.argument('domain')
@click.argument('leasefile', default=LEASE_FILE)
def cli(ctx, leasefile, domain):
    """output active dhcp clients from dhcpd.leases in tinydns-data format"""
    leases=IscDhcpLeases(leasefile)
    for r in leases.get_current().values():
        hostname = r.hostname or 'host%s' % r.ip.split('.')[-1]
        ctx.echo('=%s.%s:%s' % (hostname, domain, r.ip)) 
