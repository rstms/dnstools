from setuptools import setup

setup(
    name='rstms-dnstools',
    version='1.0',
    py_modules = ['dnstools'],
    install_requires = [
        'click',
        'cloudflare',
    ],
    entry_points = '''
        [console_scripts]
        dns=dnstools:cli
    ''',
)
