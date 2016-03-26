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


.. _uth-bitcoin-transactions:

********************
Bitcoin Transactions
********************

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
