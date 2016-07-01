try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Runner Data Load',
    'author': 'Siva Popuri',
    'author_email': 'sivanjaneyulu.popuri@ctl.io',
    'version': '0.0.1',
    'install_requires': [
         'requests>=2.7',
         'pycrypto',
         'porc',
         'hvac>=0.2.7'
    ],
    'packages': [],
    'scripts': [],
    'name': 'rnr-data-load'
}

setup(**config)
