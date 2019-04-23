# dnstools
Utility scripts for djbdns, tinydns, dnscache and Cloudflare configuration tasks

This program performs very specific tasks used in configuration and maintenance of a split-horizon public/local DNS server configuration which supports public-facing DNS and serves DNS lookups for the local network from a local server which resolves hosts not visible to the public.

### dns implementation
 - cloudflare as a public nameserver for the public domain
 - dnscache as a resolver for local network hosts
 - tinydns as a local nameserver for local resolver calls to the public domain

### installation
Simple installation:
```pip install --upgrade https://github.com/rstms/dnstools/tarball/master```

### usage:
command line help is available:
```dns --help```

### module dependencies
  - cloudflare
  - click

### cloudflare configuration

  CloudFlare API requires email and token to be configured using the mechanisms described here: https://github.com/cloudflare/python-cloudflare


