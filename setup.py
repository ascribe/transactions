"""
transactions: Bitcoin for Humans

transactions is a small python library to easily create and push transactions
to the bitcoin network.

More information at https://github.com/ascribe/transactions

"""
import io
import os
import re

from setuptools import setup


def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(
        r'^__version__ = [\'"]([^\'"]*)[\'"]', version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


install_requires = [
    'bitcoin>=1.1.42',
    'pycoin>=0.62',
    'requests>=2.9.1',
]

tests_require = [
    'pytest',
    'coverage',
    'pep8',
    'pyflakes',
    'pylint',
    'pytest',
    'pytest-cov',
    'python-bitcoinrpc>=0.3.1',
]

dev_require = [
    'ipdb',
    'ipython',
    'python-bitcoinrpc>=0.3.1',
]

docs_require = [
    'Sphinx>=1.3.5',
    'sphinx-autobuild',
    'sphinxcontrib-napoleon>=0.4.4',
    'sphinx_rtd_theme',
]

setup(
    name='transactions',
    version=find_version('transactions', '__init__.py'),
    url='https://github.com/ascribe/transactions',
    license='Apache Software License',
    author='Rodolphe Marques',
    author_email='rodolphe@ascribe.io',
    packages=['transactions',
              'transactions.services'],
    description='transactions: Bitcoin for Humans',
    long_description=__doc__,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development',
    ],
    install_requires=install_requires,
    setup_requires=['pytest-runner'],
    tests_require=tests_require,
    extras_require={
        'test': tests_require,
        'dev':  dev_require + tests_require + docs_require,
        'docs':  docs_require,
    },
    dependency_links=[
        'git+https://github.com/sbellem/python-bitcoinrpc.git@setup#egg=python_bitcoinrpc-0.3.1',
    ],
)
