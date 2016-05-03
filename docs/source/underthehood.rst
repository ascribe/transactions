.. _under-the-hood:

##############
Under the Hood
##############

The intent of this section is to document what goes on under the hood of
``transactions``.

We'll use three main "pillars" to organize and present the information:

* :ref:`uth-bitcoin-network`
* :ref:`uth-bitcoin-addresses`
* :ref:`uth-bitcoin-transactions`

One additional section will be used to present some key aspects of the
libraries that ``transactions`` rely on, especially the two bitcoin libraries:
``pycoin`` and ``pybitcointools``.

* :ref:`libs-transactions`


.. _uth-bitcoin-network:

***************
Bitcoin Network
***************
There are multiple ways that one may connect to the bitcoin network. For the
sake of simplicity, let's say that they are two main ways:

via a daemon
    that is communicating directly with a node located at a specific host and
    port

via a blockchain explorer
    that is communicating with the bitcoin network via the public API of the
    blockchain explorer service such as `blockr.io`_

Different Modes of the Bitcoin Network
======================================
The bitcoin daemon and other bitcoin core programs can be run in three
different "`network modes`_":

`mainnet`_
    *The original and main* `network`_ *for Bitcoin transactions, where*
    `satoshis`_ *have real economic value.* [#mainnet_ref]_

`testnet`_
    *A global testing environment in which developers can obtain and spend*
    `satoshis`_ *that have no real-world value on a* `network`_ *that is very*
    *similar to the Bitcoin.* [#testnet_ref]_

`regtest`_
    *A local testing environment in which developers can almost instantly*
    *generate* `blocks`_ *on demand for testing events, and can create private*
    `satoshis`_ *with no real-world value.* [#regtest_ref]_

Running a bitcoin node in regtest mode
======================================

bitcoin json rpc
----------------
ref: https://en.bitcoin.it/wiki/API_reference_%28JSON-RPC%29

* via curl
* via python with python-bitcoinrpc
* via python with requests
* via transactions

curl
^^^^

.. code-block:: bash

    $ curl --user user --data-binary  \
        '{"jsonrpc": "1.0", "id":"dummy", "method": "getinfo", "params": [] }'  \ 
        -H 'content-type: text/plain;' http://127.0.0.1:18332/


docker
======

host - container
----------------

Runnign bitcoind in container and making rpc calls to it from the host machine,
(sender_ip)

given the following ``bitcoin.conf``:

.. code-block:: bash

    dnsseed=0
    rpcuser=a
    rpcallowip=<sender_ip>


.. code-block:: bash
    
    docker run --rm --name btc -v ~/.bitcoin-docker:/root/.bitcoin -p <sender_ip>:58332:18332 btc5 bitcoind -regtest -printtoconsole


.. code-block:: bash
    
    curl --user a:b --data-binary '{"jsonrpc": "1.0", "id":"", "method": "getinfo", "params": [] }' -H 'content-type: text/plain;' http://<sender_ip>:58332


container-container
-------------------
Making rpc calls from a container to the bitcoind running in another container.



Connecting to the Bitcoin Network with ``transactions`` 
=======================================================
When using ``transactions``, one can interact with the bitcoin network
via a daemon or via a blockchain explorer. When connecting via a daemon it is
possible to connect to the three networks: mainnet, testnet, or regtest,
whereas when connecting via a blockchain explorer one may connect to the
mainnet or testnet.

The supported blockchain explorer is `blockr.io`_


.. todo:: show code examples


.. _uth-bitcoin-addresses:

*****************
Bitcoin Addresses
*****************

.. todo:: Show how a bitcoin address is created.



.. _uth-bitcoin-transactions:

********************
Bitcoin Transactions
********************

.. todo:: Show the different steps required to publish a transaction in the
    bitcoin network.

    Lifecycle of a transaction: creation, signing, publishing, confirmation

    * Using ``create`` to fetch a transaction
    * Using ``sign`` to fetch a transaction
    * Using ``push`` to publish a transaction
    * Using ``get`` to fetch a transaction

    Elements of the payload of a transaction


Blocks
======
Transactions are assembled into blocks.

credits: 

    * https://gist.github.com/shirriff/c9fb5d98e6da79d9a772#file-merkle-py
    * https://github.com/richardkiss/pycoin

Example:

.. code-block:: bash

    $ curl https://blockexplorer.com/api/block/0000000000000000e067a478024addfecdc93628978aa52d91fabd4292982a50 | python -m json.tool

Or in python:


.. code-block:: python

    import json

    import requests

    
    BLOCKEXPLORER_API_URL = 'https://blockexplorer.com/api'
    BLOCKHASH = '0000000000000000e067a478024addfecdc93628978aa52d91fabd4292982a50q'

    url = '{}/block/{}'.format(BLOCKEXPLORER_API_URL, blockhash)
    response = requests.get(url)
    block = json.loads(response.content)

    block
    {u'bits': u'19015f53',
     u'chainwork': u'000000000000000000000000000000000000000000001a6eca45b2459ce9eed8',
     u'confirmations': 120187,
     u'difficulty': 3129573174.5222874,
     u'hash': u'0000000000000000e067a478024addfecdc93628978aa52d91fabd4292982a50',
     u'height': 286819,
     u'isMainChain': True,
     u'merkleroot': u'871714dcbae6c8193a2bb9b2a69fe1c0440399f38d94b3a0f1b447275a29978a',
     u'nextblockhash': u'0000000000000000b0f08ec6a3d1e84994498ecf993a9981f57982cfdb66c443',
     u'nonce': 856192328,
     u'poolInfo': {u'poolName': u'ghash.io', u'url': u'https://ghash.io/'},
     u'previousblockhash': u'000000000000000117c80378b8da0e33559b5997f2ad55e2f7d18ec1975b9717',
     u'reward': 25,
     u'size': 152509,
     u'time': 1392872245,
     u'tx': [u'00baf6626abc2df808da36a518c69f09b0d2ed0a79421ccfde4f559d2e42128b',
             u'91c5e9f288437262f218c60f986e8bc10fb35ab3b9f6de477ff0eb554da89dea',
             u'46685c94b82b84fa05b6a0f36de6ff46475520113d5cb8c6fb060e043a0dbc5c',
             u'ba7ed2544c78ad793ef5bb0ebe0b1c62e8eb9404691165ffcb08662d1733d7a8',
             u'b8dc1b7b7ed847c3595e7b02dbd7372aa221756b718c5f2943c75654faf48589',
             ...]
     u'version': 2}


    'merkleroot': u'871714dcbae6c8193a2bb9b2a69fe1c0440399f38d94b3a0f1b447275a29978a',


The merkle root corresponds to the cummulative hashing of the transactions
hashes.

That is, each transaction is hashed. Each hash is a leaf of a binary tree. 

A binary tree is built by pairing leaves, concatenating the pair, and computing
the hash of the concatenated pair. The same process is repeated for the parent,
recursively all the way to the root, resulting in the merkle root.

At each level of the tree, if the number of hashes is odd, then the last hash
is included twice.

Progammatically, this means:

.. code-block:: python

    def merkleroot(hashes);
        if len(hashes) == 1:
            return hashes[0]
        if len(hashes) % 2 == 1;
            hashes.append(hashes[-1])
        parent_hashes = []
        for i in range(0, len(hashes), 2);
            h = sec_hash_algo(hashes[i] + hashes[i+1])
            parent_hashes.append(h)
        return merkle_root(parent_hashes)   


.. todo:: bitcoin data dir

    https://en.bitcoin.it/wiki/Data_directory


.. _libs-transactions:

**********************************
Libraries used by ``transactions``
**********************************

.. todo:: Present libraries used; ``requests``, ``pycoin``, ``pybitcointools``

    Dive into the details of how pycoin and pybitcointools are used and work under the hood.



**********
References
**********

.. [#mainnet_ref] https://bitcoin.org/en/glossary/mainnet
.. [#testnet_ref] https://bitcoin.org/en/glossary/testnet
.. [#regtest_ref] https://bitcoin.org/en/glossary/regression-test-mode




.. _network modes: https://bitcoin.org/en/developer-examples#testing-applications
.. _network: https://bitcoin.org/en/developer-guide#term-network
.. _mainnet: https://bitcoin.org/en/glossary/mainnet
.. _testnet: https://bitcoin.org/en/glossary/testnet
.. _regtest: https://bitcoin.org/en/glossary/regression-test-mode
.. _block: https://bitcoin.org/en/glossary/block
.. _blocks: https://bitcoin.org/en/glossary/block
.. _satoshi: https://bitcoin.org/en/glossary/denominations
.. _satoshis: https://bitcoin.org/en/glossary/denominations

.. _blockr.io: https://blockr.io/documentation/api
