.. image:: https://img.shields.io/pypi/v/transactions.svg
    :target: https://pypi.python.org/pypi/transactions
.. image:: https://img.shields.io/travis/ascribe/transactions.svg
    :target: https://travis-ci.org/ascribe/transactions
.. image:: https://img.shields.io/codecov/c/github/ascribe/transactions/master.svg
    :target: https://codecov.io/github/ascribe/transactions?branch=master
.. image:: https://readthedocs.org/projects/transactions/badge/?version=latest
    :target: http://transactions.readthedocs.org/en/latest/?badge=latest


transactions: Bitcoin for Humans
================================
``transactions`` is a small python library to easily create and push
transactions to the bitcoin network.

Installation
------------

.. code-block:: bash

    $ pip install transactions


Examples
--------
Assuming the following cast of characters:

.. code-block:: python

    >>> alice = 'mhyCaF2HFk7CVwKmyQ8TahgVdjnHSr1pTv'
    >>> bob = 'mqXz83H4LCxjf2ie8hYNsTRByvtfV43Pa7'
    >>> carol = 'mtWg6ccLiZWw2Et7E5UqmHsYgrAi5wqiov'

Moving ``10000`` satoshis from ``alice`` to ``bob``:

.. code-block:: python

    >>> from transactions import Transactions
    >>> transactions = Transactions(testnet=True)
    >>> tx = transactions.create(alice, (bob, 10000))
    >>> tx_signed = transactions.sign(tx, 'alice master secret')
    >>> transactions.push(tx_signed)

Moving ``600`` satoshis from ``bob`` to ``carol`` with a custom ``op_return``:

.. code-block:: python

    >>> tx = transactions.create(bob, (carol, 600), op_return='HELLOFROMASCRIBE')
    >>> tx_signed = transactions.sign(tx, 'bob master secret')
    >>> transactions.push(tx_signed)

Check it out `fbbd6407b8fc73169918b2fce7f07aff6a486a241c253f0f8eeb942937fbb970 <https://www.blocktrail.com/tBTC/tx/fbbd6407b8fc73169918b2fce7f07aff6a486a241c253f0f8eeb942937fbb970>`_

With ``transactions`` all amounts are in satoshi and we currently only support
`BIP32`_ wallets (hierarchical deterministic wallets, aka "HD Wallets").


Documentation
-------------
https://transactions.readthedocs.org/


Contributing
------------
Pull requests, feedback, and suggestions are welcome.
`Issues <https://github.com/ascribe/transactions/issues>`_ and
`pull requests <https://github.com/ascribe/transactions/pulls>`_ are handled
via github.


Background
----------
This was developed by ascribe GmbH as part of the overall ascribe technology
stack. https://www.ascribe.io


Copyright
---------
This code is © 2015 ascribe GmbH.

Licensed under the Apache License, Version 2.0.


.. _bip32: https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki
