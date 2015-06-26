# transactions: Bitcoin for Humans
transactions is a small python library to easily create and push transactions to the bitcoin network.

## Install
```
pip install -r requirements.txt
python setup.py install
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

##### Transactions(self, service='blockr', testnet=False, username='', password='', host='', port='')
- service: currently supports _blockr_ for blockr.io and and _daemon_ for bitcoin daemon. Defaults to _blockr_
- testnet: use True if you want to use tesnet. Defaults to False
- username: username to connect to the bitcoin daemon
- password: password to connect to the bitcoin daemon
- host: host of the bitcoin daemon
- port: port of the bitcoin daemon

##### Transactions.simple_transaction(from_address, to, op_return=None)
- from_address: bitcoin address originating the transaction
- to: tuple of (to_address, amount) or list of tuples [(to_addr1, amount1), (to_addr2, amount2)]. Amounts are in _satoshi_
- op_return: ability to set custom op_return 

##### Transactions.get(hash, max_transactions=100, min_confirmations=6)
- hash: can be a bitcoin address or a transaction id. If its a bitcoin address it will return a list of transactions up to _max_transactions_
and a list of unspents with confirmed transactions greater or equal to _min_confirmantions_

```python
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
```

##### Transactions.sign_transaction(tx_hex, master_password, path='')
- tx_hex: hex transaction to sign
- master_password: master_password for BIP32 wallets
- path: optional path to the leaf address of the BIP32 wallet. This allows us to retrieve private key for the
        leaf address if one was used to construct the transaction.

Currently _transactions_ only supports BIP32 hierarchical deterministic wallets

##### Transactions.push(tx_hex_signed)
- tx_hex_signed: hex transaction signed

##### Transactions.build_transaction(inputs, outputs):
- inputs: inputs in the form of {'output': 'txid:vout', 'value': amount in satoshi}
- outputs: outputs in the form of {'address': to_address, 'value': amount in satoshi}

## Contributing
Pull requests, feedback, suggestions are welcome.

<rodolphe@ascribe.io>

## Background
This was developed by ascribe GmbH as part of the overall ascribe technology stack. http://www.ascribe.io

## Copyright

This code is © 2015 ascribe GmbH.

Licensed under the Apache License, Version 2.0.

