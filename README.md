# transactions: Bitcoin for Humans

[![PyPI](https://img.shields.io/pypi/v/transactions.svg)](https://pypi.python.org/pypi/transactions)
[![Travis](https://img.shields.io/travis/ascribe/transactions.svg)](https://travis-ci.org/ascribe/transactions)
[![Documentation Status](https://readthedocs.org/projects/transactions/badge/?version=latest)](http://transactions.readthedocs.org/en/latest/?badge=latest)

transactions is a small python library to easily create and push transactions to the bitcoin network.

## Install
```
pip install transactions
```

## Example
```python
from transactions import Transactions

transactions = Transactions(testnet=True)
tx = transactions.simple_transaction('mhyCaF2HFk7CVwKmyQ8TahgVdjnHSr1pTv', ('mqXz83H4LCxjf2ie8hYNsTRByvtfV43Pa7', 10000))
tx_signed = transactions.sign_transaction(tx, "master secret")
txid = transactions.push(tx_signed)
print txid
```

Transaction with custom op_return
```python
from transactions import Transactions

transactions = Transactions(testnet=True)
tx = transactions.simple_transaction('mqXz83H4LCxjf2ie8hYNsTRByvtfV43Pa7', ('mtWg6ccLiZWw2Et7E5UqmHsYgrAi5wqiov', 600), op_return='HELLOFROMASCRIBE')
tx_signed = transactions.sign_transaction(tx, "master secret")
txid = transactions.push(tx_signed)
print txid
```
Check it out [fbbd6407b8fc73169918b2fce7f07aff6a486a241c253f0f8eeb942937fbb970](https://www.blocktrail.com/tBTC/tx/fbbd6407b8fc73169918b2fce7f07aff6a486a241c253f0f8eeb942937fbb970)

With transactions all amounts are in satoshi and we currently only support BIP32 wallets (HD wallets)

## Documentation
https://transactions.readthedocs.org/


## Contributing
Pull requests, feedback, suggestions are welcome.

<rodolphe@ascribe.io>

## Background
This was developed by ascribe GmbH as part of the overall ascribe technology stack. http://www.ascribe.io

## Copyright

This code is © 2015 ascribe GmbH.

Licensed under the Apache License, Version 2.0.

