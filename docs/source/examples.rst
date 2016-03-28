Examples
========
Let's assume the following cast of characters:

* **Alice** with the bitcoin address ``'mhyCaF2HFk7CVwKmyQ8TahgVdjnHSr1pTv'``
* **Bob** with the bitcoin address ``'mqXz83H4LCxjf2ie8hYNsTRByvtfV43Pa7'``
* **Carol** with the bitcoin address ``'mtWg6ccLiZWw2Et7E5UqmHsYgrAi5wqiov'``

Also consider that one bitcoin is made up of `satoshi`_, such that hundred
million satoshi is one bitcoin.

.. note::

    With ``transactions`` all amounts are in satoshi and we currently only
    support `BIP32`_ wallets (hierarchical deterministic wallets, aka
    "HD Wallets").

.. _bip32: https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki

Alice sends 10000 satoshi to Bob
--------------------------------
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
--------------------------------------------------------
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


Get transactions of Alice
-------------------------

.. code-block:: python
    
    from transactions import Transactions
    
    transactions = Transactions(testnet=True)

    transactions.get('mhyCaF2HFk7CVwKmyQ8TahgVdjnHSr1pTv')

    {'transactions': [{'amount': -20000,
       'confirmations': 5,
       'time': 1431333905,
       'txid': u'7f4902599ac9e5c9db347228b489c25fe5095f812c979dd84cc4e88f6812db9e'},
      {'amount': -40000,
       'confirmations': 11,
       'time': 1431329129,
       'txid': u'382639448115e859b0dc4092892bc0921edc8851a2b7adbd7b5ab39ccefb73ee'},
     ...
     'unspents': [{'amount': 809760000,
       'confirmations': 5,
       'txid': u'7f4902599ac9e5c9db347228b489c25fe5095f812c979dd84cc4e88f6812db9e',
       'vout': 1}]}


Get details of a transaction between Alice and Bob
--------------------------------------------------

.. code-block:: python
    
    from transactions import Transactions
    
    transactions = Transactions(testnet=True)

    transactions.get('382639448115e859b0dc4092892bc0921edc8851a2b7adbd7b5ab39ccefb73ee')

    {u'block': 395966,
     u'confirmations': 11,
     u'days_destroyed': u'0.00',
     u'extras': None,
     u'fee': u'0.00010000',
     u'is_coinbased': 0,
     u'is_unconfirmed': False,
     u'time_utc': u'2015-05-11T09:25:29Z',
     u'trade': {u'vins': [{u'address': u'mhyCaF2HFk7CVwKmyQ8TahgVdjnHSr1pTv',
        u'amount': -0.0004,
        u'is_nonstandard': False,
        u'n': 3,
        u'type': 0,
        u'vout_tx': u'dece4f3d0de255bb53c20e89271d1236929d72e426e6e7860d97564c6b9e26ab'}],
      u'vouts': [{u'address': u'mqXz83H4LCxjf2ie8hYNsTRByvtfV43Pa7',
        u'amount': 0.0001,
        u'is_nonstandard': False,
        u'is_spent': 0,
        u'n': 0,
        u'type': 1},
    ...
    u'type': 1}]}


.. _satoshi: https://en.bitcoin.it/wiki/Satoshi_%28unit%29
