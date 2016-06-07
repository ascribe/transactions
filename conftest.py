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
def alice_hd_wallet():
    return BIP32Node.from_master_secret('alice-secret', netcode='XTN')


@pytest.fixture
def bob_hd_wallet():
    return BIP32Node.from_master_secret('bob-secret', netcode='XTN')


@pytest.fixture
def alice_hd_address(alice_hd_wallet):
    return alice_hd_wallet.bitcoin_address()


@pytest.fixture
def bob_hd_address(bob_hd_wallet):
    return bob_hd_wallet.bitcoin_address()


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


@pytest.fixture
def bitcoin_daemon_service(rpcuser, rpcpassword, host, port, rpcurl):
    from transactions.services.daemonservice import BitcoinDaemonService
    return BitcoinDaemonService(rpcuser, rpcpassword, host, port)


@pytest.fixture
def regtest_daemon_service(rpcuser, rpcpassword, host, port, rpcurl):
    from transactions.services.daemonservice import RegtestDaemonService
    return RegtestDaemonService(rpcuser, rpcpassword, host, port)


@pytest.fixture
def signed_tx_hex():
    return (
        '01000000014f2d34b5c41cfc34ffba6811280297cd3a45fdc4a982bd137219170e34d'
        '8a995010000006b483045022100f52d33589ac95fda263d35a694dffcc9626d4c371a'
        '3140c020cf22956adc9e14022073c833d254a13620ff0b4d9e0f8c52643962f1cdc7d'
        '684cbacf1a82692cee1ed01210256e335d68d2f4f9561985fb061a5c36ff9510b7300'
        '5cf81e2f7a26e7bce0d8ceffffffff0210270000000000001976a914ff141b97e1bd3'
        '8ccbafd72fdaed88b34d62337f588ac00e5b901000000001976a9145d5988080ddb72'
        'dcb365755fbc1ea46bbee7628788ac00000000'
    )


@pytest.fixture
def block_hash():
    """
    Hash of a block on testnet.

    See https://www.blocktrail.com/tBTC/block/787057 for example.

    """
    return '00000000000003970a9fdd3f774995320c6eb729b01065fd86e210336b4022f3'
