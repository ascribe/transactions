# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
from importlib import import_module

import pytest
from bitcoinrpc.authproxy import AuthServiceProxy
from pycoin.key.BIP32Node import BIP32Node


@pytest.mark.parametrize('srv,srv_mod_name,srv_cls_name,is_testnet', [
    ('blockr', 'blockrservice', 'BitcoinBlockrService', False),
    ('daemon', 'daemonservice', 'BitcoinDaemonService', False),
    ('regtest', 'daemonservice', 'RegtestDaemonService', True),
])
def test_init_transactions_class(srv, srv_mod_name, srv_cls_name, is_testnet):
    from transactions import Transactions
    service_module = import_module(
        '.{}'.format(srv_mod_name), package='transactions.services')
    service_class = getattr(service_module, srv_cls_name)
    trxs = Transactions(service=srv)
    assert trxs.testnet is is_testnet
    assert isinstance(trxs._service, service_class)
    assert trxs._min_tx_fee == trxs._service._min_transaction_fee
    assert trxs._dust == trxs._service._min_dust


def test_init_transaction_class_with_non_suported_service():
    from transactions import Transactions
    with pytest.raises(Exception):
        Transactions(service='dummy')


@pytest.mark.usefixtures('init_blockchain')
def test_get_raw_transaction_of_len_64(transaction, rpcurl):
    conn = AuthServiceProxy(rpcurl)
    alice = conn.getnewaddress()
    btc_amount = 1
    tx_hash = conn.sendtoaddress(alice, btc_amount)
    conn.generate(1)
    tx = transaction.get(tx_hash, raw=True)
    assert isinstance(tx, dict)
    assert 'blockhash' in tx
    assert 'vout' in tx
    assert 'hex' in tx
    assert 'vin' in tx
    assert 'txid' in tx
    assert 'blocktime' in tx
    assert 'version' in tx
    assert 'confirmations' in tx
    assert 'time' in tx
    assert 'locktime' in tx
    assert 'size' in tx
    for vout in tx['vout']:
        if vout['scriptPubKey']['addresses'][0] == alice:
            break
    else:
        assert False, 'alice address was not found'
    assert vout['value'] == btc_amount


@pytest.mark.usefixtures('init_blockchain')
def test_transaction_creation_via_simple_transactian(rpcuser,
                                                     rpcpassword,
                                                     host,
                                                     port,
                                                     rpcurl):
    from transactions import Transactions

    # create two users: alice & bob
    conn = AuthServiceProxy(rpcurl)
    alice = conn.getnewaddress()
    bob = conn.getnewaddress()

    # Give alice 3 bitcoins
    conn.sendtoaddress(alice, 3)
    conn.generate(1)

    trxs = Transactions(
        service='daemon',
        username=rpcuser,
        password=rpcpassword,
        host=host,
        port=port,
    )
    simple_transaction = trxs.simple_transaction(
        alice, (bob, 200000000), min_confirmations=1)
    assert simple_transaction


@pytest.mark.usefixtures('init_blockchain')
def test_create_sign_push_transaction(rpcuser,
                                      rpcpassword,
                                      host,
                                      port,
                                      rpcurl):
    from transactions import Transactions

    # create two users: alice & bob
    alice = BIP32Node.from_master_secret('alice-secret',
                                         netcode='XTN').bitcoin_address()
    bob = BIP32Node.from_master_secret('bob-secret',
                                       netcode='XTN').bitcoin_address()

    conn = AuthServiceProxy(rpcurl)
    conn.importaddress(alice)
    conn.importaddress(bob)

    # Give alice 3 bitcoins
    conn.sendtoaddress(alice, 3)
    conn.generate(1)

    trxs = Transactions(
        service='daemon',
        username=rpcuser,
        password=rpcpassword,
        host=host,
        port=port,
        testnet=True,
    )
    raw_tx = trxs.create(alice, (bob, 200000000), min_confirmations=1)
    assert raw_tx
    signed_tx = trxs.sign(raw_tx, 'alice-secret')
    assert signed_tx

    # get bob's balance before tx
    bob_before = conn.getreceivedbyaddress(bob)
    pushed_tx = trxs.push(signed_tx)
    assert pushed_tx
    conn.generate(1)    # pack the transaction into a block
    assert conn.getreceivedbyaddress(bob) - bob_before == 2


@pytest.mark.skipif(os.environ.get('TRAVIS') == 'true',
                    reason='sslv3 alert handshake failure')
def test_transaction_creation_via_simple_transaction_with_blockr(alice, bob):
    from transactions import Transactions
    trxs = Transactions(testnet=True)
    assert trxs.testnet is True
    simple_transaction = trxs.simple_transaction(alice, (bob, 6))
    assert simple_transaction


@pytest.mark.skipif(os.environ.get('TRAVIS') == 'true',
                    reason='sslv3 alert handshake failure')
def test_transaction_creation_via_create_with_blockr(alice, bob):
    from transactions import Transactions
    trxs = Transactions(testnet=True)
    assert trxs.testnet is True
    simple_transaction = trxs.create(alice, (bob, 6))
    assert simple_transaction
