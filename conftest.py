# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
from uuid import uuid1

import pytest

from bitcoinrpc.authproxy import AuthServiceProxy
from pycoin.key.BIP32Node import BIP32Node


@pytest.fixture
def alice():
    return 'n12nZmfTbDGCT3VJF5QhPhyVGXvXPzQkFW'


@pytest.fixture
def bob():
    return 'mgaUVCq15uywYsqv7dVM4vxVAkq37c44aW'


@pytest.fixture
def carol():
    return 'mtWg6ccLiZWw2Et7E5UqmHsYgrAi5wqiov'


@pytest.fixture
def random_bip32_wallet():
    return BIP32Node.from_master_secret(uuid1().get_hex(), netcode='XTN')


@pytest.fixture
def random_bip32_address(random_bip32_wallet):
    return random_bip32_wallet.bitcoin_address()


@pytest.fixture
def host():
    return os.environ.get('BITCOIN_HOST', 'localhost')


@pytest.fixture
def port():
    return os.environ.get('BITCOIN_PORT', 18332)


@pytest.fixture
def rpcuser():
    return os.environ.get('BITCOIN_RPCUSER', 'merlin')


@pytest.fixture
def rpcpassword():
    return os.environ.get('BITCOIN_RPCPASSWORD', 'secret')


@pytest.fixture
def rpcurl(rpcuser, rpcpassword, host, port):
    return 'http://{}:{}@{}:{}'.format(rpcuser, rpcpassword, host, port)


@pytest.fixture
def rpcconn(rpcurl):
    return AuthServiceProxy(rpcurl)


@pytest.fixture
def init_blockchain(rpcconn):
    """
    Initialize the blockchain if needed, making sure that the balance is at
    least 50 bitcoins. The block reward only happens after 100 blocks, and for
    this reason at least 101 blocks are needed.

    """
    block_count = rpcconn.getblockcount()
    if block_count < 101:
        rpcconn.generate(101 - block_count)
    else:
        balance = rpcconn.getbalance()
        if balance < 50:
            rpcconn.generate(1)


@pytest.fixture
def transactions(rpcuser, rpcpassword, host, port, rpcurl):
    from transactions import Transactions
    return Transactions(
        service='daemon',
        username=rpcuser,
        password=rpcpassword,
        host=host,
        port=port,
        testnet=True,
    )
