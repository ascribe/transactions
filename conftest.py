# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os

import pytest

from bitcoinrpc.authproxy import AuthServiceProxy


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
def init_blockchain(rpcurl):
    """
    Initialize the blockchain if needed, making sure that the balance is at
    least 50 bitcoins. The block reward only happens after 100 blocks, and for
    this reason at least 101 blocks are needed.

    """
    conn = AuthServiceProxy(rpcurl)
    block_count = conn.getblockcount()
    if block_count < 101:
        conn.generate(101 - block_count)
    else:
        balance = conn.getbalance()
        if balance < 50:
            conn.generate(1)


@pytest.fixture
def transaction(rpcuser, rpcpassword, host, port, rpcurl):
    from transactions import Transactions
    return Transactions(
        service='daemon',
        username=rpcuser,
        password=rpcpassword,
        host=host,
        port=port,
    )
