# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from importlib import import_module

import pytest
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
def test_get_raw_transaction_of_len_64(transactions, rpcconn):
    alice = rpcconn.getnewaddress()
    btc_amount = 1
    tx_hash = rpcconn.sendtoaddress(alice, btc_amount)
    rpcconn.generate(1)
    tx = transactions.get(tx_hash, raw=True)
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
def test_transaction_creation_via_simple_transactian(transactions, rpcconn):
    alice = rpcconn.getnewaddress()
    bob = rpcconn.getnewaddress()
    rpcconn.sendtoaddress(alice, 3)
    rpcconn.generate(1)
    simple_transaction = transactions.simple_transaction(
        alice, (bob, 200000000), min_confirmations=1)
    assert simple_transaction


@pytest.mark.usefixtures('init_blockchain')
def test_transaction_creation_with_op_return(transactions, rpcconn):
    alice = rpcconn.getnewaddress()
    bob = rpcconn.getnewaddress()
    rpcconn.sendtoaddress(alice, 3)
    rpcconn.generate(1)
    transaction = transactions.create(
        alice,
        (bob, 200000000),
        min_confirmations=1,
        op_return='micro-combustion',
    )
    assert transaction


@pytest.mark.usefixtures('init_blockchain')
def test_sign_transaction_with_wif(transactions, rpcconn,
                                   alice_hd_wallet, bob_hd_address):
    alice_hd_address = alice_hd_wallet.bitcoin_address()
    rpcconn.importaddress(alice_hd_address)
    rpcconn.importaddress(bob_hd_address)
    rpcconn.sendtoaddress(alice_hd_address, 3)
    rpcconn.generate(1)
    raw_tx = transactions.create(
        alice_hd_address,
        (bob_hd_address, 200000000),
        min_confirmations=1,
    )
    signed_tx = transactions.sign(raw_tx, alice_hd_wallet.wif())
    assert signed_tx


@pytest.mark.usefixtures('init_blockchain')
def test_select_inputs(transactions, rpcconn):
    alice = rpcconn.getnewaddress()
    rpcconn.sendtoaddress(alice, 1)
    rpcconn.generate(1)
    satoshis = 100000000 - transactions._min_tx_fee
    transactions._select_inputs(alice, satoshis, min_confirmations=1)


def test_select_inputs_with_no_funds(transactions, rpcconn):
    alice = rpcconn.getnewaddress()
    with pytest.raises(Exception) as exc:
        transactions._select_inputs(alice, 1)
    assert exc.value.args[0] == 'No spendable outputs found'


@pytest.mark.usefixtures('init_blockchain')
def test_select_inputs_with_insufficient_funds(transactions, rpcconn):
    alice = rpcconn.getnewaddress()
    rpcconn.sendtoaddress(alice, 1)
    rpcconn.generate(1)
    with pytest.raises(Exception) as exc:
        transactions._select_inputs(alice, 100000000, min_confirmations=1)
    assert exc.value.args[0] == 'Not enough balance in the wallet'


@pytest.mark.usefixtures('init_blockchain')
def test_create_sign_push_transaction(transactions, rpcconn):
    alice = BIP32Node.from_master_secret(b'alice-secret',
                                         netcode='XTN').bitcoin_address()
    bob = BIP32Node.from_master_secret(b'bob-secret',
                                       netcode='XTN').bitcoin_address()
    rpcconn.importaddress(alice)
    rpcconn.importaddress(bob)
    rpcconn.sendtoaddress(alice, 3)
    rpcconn.generate(1)
    raw_tx = transactions.create(alice, (bob, 200000000), min_confirmations=1)
    assert raw_tx
    signed_tx = transactions.sign(raw_tx, b'alice-secret')
    assert signed_tx
    bob_before = rpcconn.getreceivedbyaddress(bob)
    pushed_tx = transactions.push(signed_tx)
    assert pushed_tx
    rpcconn.generate(1)    # pack the transaction into a block
    assert rpcconn.getreceivedbyaddress(bob) - bob_before == 2


def test_import_address(rpcconn, random_bip32_address, transactions):
    assert not rpcconn.validateaddress(random_bip32_address)['iswatchonly']
    transactions.import_address(random_bip32_address)
    assert rpcconn.validateaddress(random_bip32_address)['iswatchonly']


def test_decode_transaction_with_blockr(signed_tx_hex):
    from transactions import Transactions
    transactions = Transactions(testnet=True)
    decoded_tx = transactions.decode(signed_tx_hex)
    assert decoded_tx


def test_decode_transaction_with_jsonrpc(transactions):
    with pytest.raises(NotImplementedError) as exc:
        transactions.decode('dummy-tx')
    assert exc.value.args[0] == 'Currently only supported for "blockr.io"'


def test_get_block_raw(rpcconn, transactions):
    block_hash = rpcconn.generate(1)[0]
    block_data = transactions.get_block_raw(block_hash)
    assert block_data


def test_get_block_info(rpcconn, transactions):
    block_hash = rpcconn.generate(1)[0]
    block_data = transactions.get_block_info(block_hash)
    assert block_data


def test_get_block_raw_with_blockr(block_hash):
    from transactions import Transactions
    transactions = Transactions(testnet=True)
    block_data = transactions.get_block_info(block_hash)
    assert block_data


def test_get_block_info_with_blockr(block_hash):
    from transactions import Transactions
    transactions = Transactions(testnet=True)
    block_data = transactions.get_block_info(block_hash)
    assert block_data


def test_transaction_creation_via_simple_transaction_with_blockr(alice, bob):
    from transactions import Transactions
    trxs = Transactions(testnet=True)
    assert trxs.testnet is True
    simple_transaction = trxs.simple_transaction(alice,
                                                 (bob, 6),
                                                 min_confirmations=1)
    assert simple_transaction


def test_transaction_creation_via_create_with_blockr(alice, bob):
    from transactions import Transactions
    trxs = Transactions(testnet=True)
    assert trxs.testnet is True
    simple_transaction = trxs.create(alice, (bob, 6), min_confirmations=1)
    assert simple_transaction
