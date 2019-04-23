#!/usr/bin/env

import click
import os
import sys
import socket
import CloudFlare
from pprint import pprint

def _getzone(zone_name):
    """list records for a zone"""

    cf = CloudFlare.CloudFlare()
    # query for the zone name and expect only one value back
    try:
        zones = cf.zones.get(params = {'name':zone_name,'per_page':1})
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        exit('/zones.get %d %s - api call failed' % (e, e))
    except Exception as e:
        exit('/zones.get - %s - api call failed' % (e))

    if len(zones) == 0:
        exit('No zones found')

    # extract the zone_id which is needed to process that zone
    zone = zones[0]
    zone_id = zone['id']

    # request the DNS records from that zone
    try:
        dns_records = cf.zones.dns_records.get(zone_id)
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        exit('/zones/dns_records.get %d %s - api call failed' % (e, e))

    # print the results - first the zone name
    #print('id=%s' % repr(zone_id))
    #print('name=%s' % repr(zone_name))

    # then all the DNS records for that zone
    for dns_record in dns_records:
        r_name = dns_record['name']
        r_type = dns_record['type']
        r_value = dns_record['content']
        r_id = dns_record['id']
        #print('  %s' % repr((r_id, r_name, r_type, r_value)))
        #print('  %s' % repr(dns_record))

    return dns_records

def _process_cname(r):
    print('C%s:%s' %( r['name'], r['content']))

def _process_txt(r):
    print('\'%s:%s' %( r['name'], r['content']))

def _process_mx(r):
    # ignore MX
    #print('@%s:%s:%s' %( r['name'], r['content']))
    pass

def _process_a(r):
    print('=%s:%s' %( r['name'], r['content']))

@click.group()
@click.option('--verbose', is_flag=True, default=False)
@click.pass_context
def cli(ctx, verbose):
    ctx.verbose = verbose

@cli.command()
@click.argument('domain')
@click.argument('ip_address')
@click.pass_context
def cftodjb(ctx, domain, ip_address):
    """outputs DOMAIN's cloudflare zone as djb tinydns data using IP-ADDRESS"""
    zone = _getzone(domain)
    fqdn = socket.gethostname().split('.')[0]
    if not '.' in fqdn:
        fqdn = '%s.%s' % (fqdn, domain)
    print('.%s:%s:%s' % (domain, ip_address, fqdn))
    for r in zone:
        if r['type'] == 'CNAME':
            _process_cname(r)
        elif r['type'] == 'TXT':
            _process_txt(r)
        elif r['type'] == 'MX':
            _process_mx(r)
        elif r['type'] == 'A':
            _process_a(r)
        else:
            exit('unknown DNS record type: %s' % r['type'])
