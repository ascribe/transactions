"""
transactions: Bitcoin for Humans

transactions is a small python library to easily create and push transactions
to the bitcoin network.

More information at https://github.com/ascribe/transactions

"""
from setuptools import setup

install_requires = [
    'pybitcointools==1.1.15',
    'pycoin==0.52',
    'requests==2.7.0',
]

tests_require = [
    'pytest',
    'coverage',
    'pep8',
    'pyflakes',
    'pylint',
    'pytest',
    'pytest-cov',
]

dev_require = [
    'ipdb',
    'ipython',
]

docs_require = [
    'Sphinx>=1.3.5',
    'sphinxcontrib-napoleon>=0.4.4',
]

setup(
    name='transactions',
    version='0.1',
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
)
