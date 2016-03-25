.. transactions documentation master file, created by
   sphinx-quickstart on Fri Mar 25 14:51:21 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

transactions
============

transactions is a small python library to easily create and push transactions to the bitcoin network.


Installation
------------

.. code-block:: python

    pip install transactions



Examples
--------
Let's assume the following cast of characters:

* **Alice** with the bitcoin address ``'mhyCaF2HFk7CVwKmyQ8TahgVdjnHSr1pTv'``
* **Bob** with the bitcoin address ``'mqXz83H4LCxjf2ie8hYNsTRByvtfV43Pa7'``
* **Carol** with the bitcoin address ``'mtWg6ccLiZWw2Et7E5UqmHsYgrAi5wqiov'``

Also consider that one bitcoin is made up of `satoshi`_, such that hundred
million satoshi is one bitcoin.


Alice sends 10000 satoshi to Bob
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: python
    
    from transactions import Transactions
    
    transactions = Transactions(testnet=True)
    tx = transactions.simple_transaction(
        'mhyCaF2HFk7CVwKmyQ8TahgVdjnHSr1pTv',
        ('mqXz83H4LCxjf2ie8hYNsTRByvtfV43Pa7', 10000),
    )
    tx_signed = transactions.sign_transaction(tx, 'master secret')
    txid = transactions.push(tx_signed)
    print txid

Bob sends 600 satoshi to Carol with a custom `op_return`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
    
    from transactions import Transactions
    
    transactions = Transactions(testnet=True)
    tx = transactions.simple_transaction(
        'mqXz83H4LCxjf2ie8hYNsTRByvtfV43Pa7',
        ('mtWg6ccLiZWw2Et7E5UqmHsYgrAi5wqiov', 600),
        op_return='HELLOFROMASCRIBE',
    )
    tx_signed = transactions.sign_transaction(tx, 'master secret')
    txid = transactions.push(tx_signed)
    print txid

Check it out `fbbd6407b8fc73169918b2fce7f07aff6a486a241c253f0f8eeb942937fbb970 <https://www.blocktrail.com/tBTC/tx/fbbd6407b8fc73169918b2fce7f07aff6a486a241c253f0f8eeb942937fbb970>`_

With transactions all amounts are in satoshi and we currently only support BIP32 wallets (HD wallets)


.. _satoshi: https://en.bitcoin.it/wiki/Satoshi_%28unit%29


Code
====

.. automodule:: transactions

.. autoclass:: Transactions
    :members: __init__, simple_transaction, get, sign_transaction, push, build_transaction


General Details
===============

.. toctree::
    :maxdepth: 2

    contributing
    background
    license


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
