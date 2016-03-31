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

```bash
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
