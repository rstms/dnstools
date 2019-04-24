from setuptools import setup

setup(
    name='rstms-dnstools',
    version='1.0',
    packages=['dnstools','dnstools.commands'],
    include_package_data=True,
    install_requires = [
        'click',
        'cloudflare',
    ],
    entry_points = '''
        [console_scripts]
        dns=dnstools.cli:cli
    ''',
)
