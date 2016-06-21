######
Theory
######

The intent here is to provide some kind of fundamental knowledge with respect
to bitcoin. 

As a starting point the material here is currently heavily inspired by the
draft version of the book `Bitcoin and Cryptocurrency Technologies`_ by

    * `Arvind Narayanan`_, Princeton University
    * `Joseph Bonneau`_, Princeton University
    * `Edward Felten`_, Princeton University
    * `Andrew Miller`_, University of Maryland
    * `Steven Goldfeder`_, Princeton University
    * `Jeremy Clark`_, Concordia University

The long term intention is to extend the material as much as it makes sense
meanwhile weaving a connection to the engineering side of bitcoin.


.. _computer-science-of-bitcoin:

***************************
Computer Science of Bitcoin
***************************
The goal of this section is to dwell on the fundamentals of bitcoin from the
point of view of data structures and algorithms.

Some of the key concepts are:

    * secure hash functions
    * hash pointers and pointer-based acyclic data structures
    * digital signatures
    * cryptocurrencies


Cryptographic Hash Functions
============================
Very briefly, a basic hash function has three main characteristics:

* input value is a string of any size
* output value is of fixed size (i.e.: 256 bits)
* for a string of n bits, the hash function has a running time of O(n)

.. note;; The output value of hash function is also called the hash.

This is more or less good enough to implement a hash table.

In order to make the basic hash function cryptographically secure, three
additional characteristics are required:

* collision‐resistance
* hiding
* puzzle‐friendliness

A hash collition means that for two different input strings the hash function
returns the same hash.

Hash functions have collisions since the number of possible inputs is infinite
whereas the number of possible outputs is finite.

collision‐resistance
  A hash function is collision-resistant if it is computationally `hard`_ to
  find its collisions.

hiding
  Reverse engineering a hash function is computationally `hard`_. That is,
  given the output of a hash function, the input string cannot be found.

puzzle‐friendliness
  Very roughly this means that one can pick a puzzle id, k, and bind it to a
  target result y, such that it is difficult to find a value x, which when fed
  to the hash function in combination with k, will yield y. By difficult, is
  meant that there are no better approaches than random trials, and that
  finding x requires substantial time, more than 2^n for if y has n bits.


Hash function in use in Bitcoin
-------------------------------
Several cryptocurrencies like Bitcoin use a hash function named SHA-256 for
verifying transactions and calculating proof-of-work or proof-of-stake. [#sha256_bitcoin]_

For a more in-depth study of the SHA-256 hash function one may consult
`Descriptions of SHA-256, SHA-384, and SHA-512`_ by NIST.


Hash Pointer -based Data Structures
===================================
A hash pointer points to a location where data is stored along with the hash
of that data at a given point in time.

Using a hash pointer one can retrieve the data, and verify that the data hasn't
changed.

Using hash pointers, one can build various pointer-based acyclic data
structures such as linked lists, trees, and more generally directed acyclic
graphs.

The bitcoin blockchain can be viewed as a linked list of binary trees, relying
on hash pointers. The hash pointer -based linked list is more precisely called
a hash chain, whereas the hash pointer -based binary tree is called a hash
tree, or `Merkle tree`_, named after its inventor `Ralph Merkle`_.

Transactions are assembled into a hash tree to form a "block." Those blocks are
then linked to form a hash chain (block chain).


.. note:: Binary hash trees make it relatively efficient to show the chain of
    transactions a transaction is linked to within a tree. For a tree with n
    transactions, only about log(n) transactions are necessary.


.. _merkle tree: https://en.wikipedia.org/wiki/Merkle_tree
.. _ralph merkle: https://en.wikipedia.org/wiki/Ralph_Merkle


Digital Signatures
==================
A digital signature requires three steps:

* private / public key pair generation
* signature
* verification

Expressed in code:

.. code-block:: python

    private_key, public_key = generate_key_pair(key_size, passphrase=None)

    signature = sign(private_key, message)

    is_valid = verify(public_key, message, signature)

There are two important requirements, one somewhat obvious, and the other more
complex.

* Valid signatures must verify. That is:

.. code-block:: python

    verify(public_key, message, sign(private_key, message)) is True

* Reverse engineering the digital signature scheme, aka forging signatures
  is computationally impossible. That is, for any given message for which the
  the signature, and public key are known, it is not possible to find the
  private key, or to figure out how to create new valid signatures for
  different messages.


ECDSA: digital signature used in Bitcoin
----------------------------------------
For its digital signatures Bitcoin uses the Elliptic Curve Digital Signature
Algorithm (`ECDSA`_) [#bitcoin_ecdsa]_ with a specific curve that is fine-tuned
via the domain parameters known as `secp256k1`_.

Sizes of keys, message, and signature when using ECDSA [#bitcoincryptotech]_

    * Private key:  256 bits
    * Public key, uncompressed:  512 bits
    * Public key, compressed:  257 bits
    * Message to be signed:  256 bits
    * Signature:  512 bits


Public Keys as Identities & Bitcoin Addresses
---------------------------------------------
Using a digital signature scheme, public keys can be used as identities. In
Bitcoin, public keys are used to identify the sender and receiver in a
transaction. Bitcoin refers to these public keys as "addresses". The sender
can sign the transaction with their private key, meanwhile the receiver can
verify the signature of the transaction using the public key of the sender.


Two Simple Cryptocurrency Models
================================
To make it easier to understand how bitcoin works, *Narayanan et al.*
[#bitcoincryptotech]_ present two simplified cryptocurrency models, which they
call "GoofyCoin", and "ScroogeCoin". The first model (GoofyCoin) is somewhat
naive, especially with respect to double-spending attacks, and is therefore
insecure. The second model (ScroogeCoin) resolves the double-spending attack
problem, but depends on the honesty of Scrooge, and is therefore centralized.
This section briefly reviews these two models, which are somewhat useful to
build upon to understand how bitcoin works.

.. note:: **Double-spending attacks**

    "Double-spending is the result of successfully spending some money more than
    once. Bitcoin protects against double spending by verifying each
    transaction added to the block chain to ensure that the inputs for the
    transaction had not previously already been spent." [#doublespend]_


GoofyCoin: a ledger-less cryptocurrency
---------------------------------------
The GoofyCoin cryptocurrency model is based on two main principles:

1. One authority (Goofy) can create coins at will, and assign these newly
   created coins to themself.
2. The owner of a coin can transfer their coin to whomever they wish.

Coin Creation
-------------
The creation of a ``goofycoin`` works like so:

.. code-block:: python

    coin_id = generate_unique_coin_id()
    coin_creation_msg = 'create_coin [coin_id]'
    coin_creation_signature = sign(goofy_private_key, coin_creation_msg)

The ``coin_creation_msg`` and ``coin_creation_signature``, taken together, form
a coin. For this example, let's say that a coin is a tuple:

.. code-block:: python

    goofycoin = (coin_creation_msg, coin_creation_signature)

In a more explicit manner:

.. code-block:: python

    goofycoin = (
        'create_coin [coin_id]',
        sign(goofy_private_key,  'create_coin [coin_id]'),
    )

Using the public key of Goofy, anyone can verify whether a ``goofycoin`` is
valid:

.. code-block:: python

    is_valid = verify(goofy_public_key, goofy_coin[0], goofy_coin[1])


or more explicitly:

.. code-block:: python

    is_valid = verify(
        goofy_public_key,
        'create_coin [coin_id]',
        coin_creation_signature,
    )

Lastly, in order to be able to refrence the coin, in future transactions, we
can hash the information of the coin, such that referencing the coin will be
done via the hash. So let's assume the following dictionary, for the coin
creation transaction:

.. code-block:: python

    transaction = {
        coin_hash: 'a9f268dbfda',
        coin : (
            'create_coin [coin_id]',
            sign(goofy_private_key,  'create_coin [coin_id]'),
        )
    }


Coin Transfer
-------------
To transfer the above coin (``a9f268dbfda``) to Alice, Goofy would create the
following transaction:

.. code-block:: python

    transaction = {
        coin_hash: 'b3a364d1a1z',
        coin : (
            'pay_to alice_pubkey: a9f268dbfda',
            sign(goofy_private_key, 'pay_to alice_pubkey: a9f268dbfda'),
        )
    }

If Alice wanted to transfer her new coin (``b3a364d1a1z``) to Bob, she would
then create the following transaction:

.. code-block:: python

    transaction = {
        coin_hash: '86b9dd63864',
        coin : (
            'pay_to bob_pubkey: b3a364d1a1z',
            sign(alice_private_key, 'pay_to bob_pubkey: b3a364d1a1z'),
        )
    }

Double-spending
^^^^^^^^^^^^^^^
The GoofyCoin model does not prevent Alice from transferring the same coin to
multiple recipients. Hence, in addition to the previous transfer she made to
Bob, Alice could transfer the same coin to Carol:

.. code-block:: python

    transaction = {
        coin_hash: 'a1z2g5pw34',
        coin : (
            'pay_to carol_pubkey: b3a364d1a1z',
            sign(alice_private_key, 'pay_to carol_pubkey: b3a364d1a1z'),
        )
    }

The two transactions (``86b9dd63864``, ``a1z2g5pw34``) are conflicting, because
two people can't own the same coin at the same time.

Next section will show how double-spending attacks can be prevented via a
centralized ledger, which keeps track of past transactions.


ScroogeCoin -- a ledger-based cryptocurrency
--------------------------------------------
The ScroogeCoin model relies on an append-only public ledger in which
transactions are permanently recorded.

The ledger is maintained by a trusted authority, Scrooge, who can also issue
new coins.

A rough sketch of the data structure of the ledger is as follwos;

.. code-block:: python

    {'prev': 0,
     'tx_id': 0,
     'tx': {...}},

    {'prev': hash_function(tx_0),
     'tx_id': 1,
     'tx': {...}},

    {'prev': hash_function(tx_1),
     'tx_id': 2,
     'tx': {...}},

    ...

The chain of transactions cannot be tempered with because of the use of hash
pointers. For example, if the content of transaction `1` was changed, the
pointer in transaction `2` would no longer point to transaction `1`, and the
chain would be broken.

The final hash pointer of the chain is signed by the trusted authority,
Scrooge, who then publishes the chain. In this model, a transaction that is not
in the signed chain is ignored. Ii is the responsibility of the trusted
authority to verify that a transaction is not a double spend.

The ScroogeCoin model supports two types of transactions;

``create_coins``
    Creates new coins, and is valid if signed by the trusted authority,
    Scrooge.

``pay_coins``
    Consumes coins, and produces new coins of the same value, that may belong
    to new people. The transaction must be signed by each owner of the consumed
    coins. Moreover, each input coin must not have been already spent.

A new transaction must be validated by the trusted authority, and once
validated will be signed and added to the chain of transactions, at which
point, and only then, the new transaction will be considered to have occurred.

This model works reasonably well, except for the dependence on a trusted
authority. In brief:

* The very existence of the chain relies on one central power.
* The central power can create unlimited amount of coins for itself.
* The central power can deny service to whomever it wishes by simply ignoring
  transactions.
* The central power can require users of the system to pay fees in order for
  their transactions to be considered.

The above problems seem sufficient to motivate efforts to decentralize the
ScroogeCoin model. This brings the next topic of study: how can such a system
be efficiently decentralized?


**********
References
**********

.. [#sha256_bitcoin] https://en.wikipedia.org/wiki/SHA-2#Applications
.. [#bitcoincryptotech] https://d28rh4a8wq0iu5.cloudfront.net/bitcointech/readings/princeton_bitcoin_book.pdf
.. [#bitcoin_ecdsa] https://en.bitcoin.it/wiki/Elliptic_Curve_Digital_Signature_Algorithm
.. [#doublespend] https://en.bitcoin.it/wiki/Double-spending

.. _Bitcoin and Cryptocurrency Technologies: https://d28rh4a8wq0iu5.cloudfront.net/bitcointech/readings/princeton_bitcoin_book.pdf
.. _Arvind Narayanan: http://randomwalker.info/
.. _Joseph Bonneau: http://jbonneau.com/
.. _Edward Felten: https://www.cs.princeton.edu/~felten/
.. _Andrew Miller: https://cs.umd.edu/~amiller/
.. _Steven Goldfeder: https://www.cs.princeton.edu/~stevenag/
.. _Jeremy Clark: http://users.encs.concordia.ca/~clark/

.. _hard: https://en.wikipedia.org/wiki/Security_of_cryptographic_hash_functions#The_meaning_of_.22hard.22
.. _Descriptions of SHA-256, SHA-384, and SHA-512:  https://web.archive.org/web/20130526224224/http://csrc.nist.gov/groups/STM/cavp/documents/shs/sha256-384-512.pdf
.. _merkle tree: https://en.wikipedia.org/wiki/Merkle_tree
.. _ralph merkle: https://en.wikipedia.org/wiki/Ralph_Merkle
.. _ecdsa: https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm
.. _secp256k1: https://en.bitcoin.it/wiki/Secp256k1
