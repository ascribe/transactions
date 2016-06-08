# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import pytest


@pytest.fixture
def block_hash():
    return '00000000000003970a9fdd3f774995320c6eb729b01065fd86e210336b4022f3'


@pytest.fixture
def alice_to_bob_tx_data():
    return {
        u'block': 787057,
        u'confirmations': 81822,
        u'days_destroyed': u'0.10',
        u'extras': None,
        u'fee': u'0.00030000',
        u'is_coinbased': 0,
        u'is_unconfirmed': False,
        u'time_utc': u'2016-04-19T21:06:02Z',
        u'trade': {
            u'vins': [
                {u'address': u'mp2YPeFdPufm515qWbmPXzSACxnMVdphnF',
                 u'amount': -0.0004,
                 u'is_nonstandard': False,
                 u'n': 1,
                 u'type': 0,
                 u'vout_tx': u'95a9d8340e17197213bd82a9c4fd453acd9702281168baff34fc1cc4b5342d4f'}
            ],
            u'vouts': [
                {u'address': u'n4mgh5qiBXj7Y3tLu4fqcPf5KubRVmR9Lr',
                 u'amount': 0.0001,
                 u'is_nonstandard': False,
                 u'is_spent': 0,
                 u'n': 0,
                 u'type': 1}
            ]
        },
        u'tx': u'2a77690c8d6d4eb8c49653ce8052fdea903328c095289eb389b6aad760ce6fcd',
        u'vins': [
            {u'address': u'mp2YPeFdPufm515qWbmPXzSACxnMVdphnF',
             u'amount': u'-0.29000000',
             u'is_nonstandard': False,
             u'n': 1,
             u'type': 0,
             u'vout_tx': u'95a9d8340e17197213bd82a9c4fd453acd9702281168baff34fc1cc4b5342d4f'}
        ],
        u'vouts': [
            {u'address': u'n4mgh5qiBXj7Y3tLu4fqcPf5KubRVmR9Lr',
             u'amount': u'0.00010000',
             u'extras': {
                 u'asm': u'OP_DUP OP_HASH160 ff141b97e1bd38ccbafd72fdaed88b34d62337f5 OP_EQUALVERIFY OP_CHECKSIG',
                 u'reqSigs': 1,
                 u'script': u'76a914ff141b97e1bd38ccbafd72fdaed88b34d62337f588ac',
                 u'type': u'pubkeyhash'
             },
             u'is_nonstandard': False,
             u'is_spent': 0,
             u'n': 0,
             u'type': 1},
           {u'address': u'mp2YPeFdPufm515qWbmPXzSACxnMVdphnF',
            u'amount': u'0.28960000',
            u'extras': {
                u'asm': u'OP_DUP OP_HASH160 5d5988080ddb72dcb365755fbc1ea46bbee76287 OP_EQUALVERIFY OP_CHECKSIG',
                u'reqSigs': 1,
                u'script': u'76a9145d5988080ddb72dcb365755fbc1ea46bbee7628788ac',
                u'type': u'pubkeyhash'
            },
            u'is_nonstandard': False,
            u'is_spent': 1,
            u'n': 1,
            u'type': 1}
        ]
    }


def test_url_property_for_mainnet():
    from transactions.services.blockrservice import BitcoinBlockrService
    blockr = BitcoinBlockrService(testnet=False)
    assert blockr._url == 'https://btc.blockr.io/api/v1'


def test_raw_list_transactions(alice, blockr):
    results = blockr.list_transactions(alice, raw=True)
    assert results
    assert 'address' in results
    assert 'limit_txs' in results
    assert 'nb_txs' in results
    assert 'nb_txs_displayed' in results
    assert 'txs' in results
    assert results['address'] == alice


def test_raw_list_unspents_with_zero_confirmation(alice, blockr):
    response = blockr.list_unspents(alice, 0, raw=True)
    assert response
    assert 'address' in response
    assert 'unspent' in response
    assert 'with_unconfirmed' in response
    assert response['address'] == alice
    assert response['with_unconfirmed']


def test_get_transaction(alice, bob, alice_to_bob_txid, blockr):
    tx_data = blockr.get_transaction(alice_to_bob_txid)
    assert tx_data
    assert 'confirmations' in tx_data
    assert 'time' in tx_data
    assert 'txid' in tx_data
    assert 'vins' in tx_data
    assert 'vouts' in tx_data
    assert tx_data['txid'] == alice_to_bob_txid
    assert any((vout['address'] == alice for vout in tx_data['vouts']))
    assert any((vout['address'] == bob for vout in tx_data['vouts']))


def test_raw_get_transaction(alice, bob, alice_to_bob_txid, blockr):
    response = blockr.get_transaction(alice_to_bob_txid, raw=True)
    assert response
    assert 'block' in response
    assert 'confirmations' in response
    assert 'days_destroyed' in response
    assert 'extras' in response
    assert 'fee' in response
    assert 'is_coinbased' in response
    assert 'is_unconfirmed' in response
    assert 'time_utc' in response
    assert 'trade' in response
    assert 'tx' in response
    assert 'vins' in response
    assert 'vouts' in response
    assert response['tx'] == alice_to_bob_txid
    assert any((vout['address'] == alice for vout in response['vouts']))
    assert any((vout['address'] == bob for vout in response['vouts']))


def test_push_tx(alice, bob, alice_secret, blockr):
    from transactions import Transactions
    transactions = Transactions(testnet=True)
    raw_tx = transactions.create(alice, (bob, 1), min_confirmations=1)
    signed_tx = transactions.sign(raw_tx, alice_secret)
    txid = blockr.push_tx(signed_tx)
    assert txid


def test_raw_push_tx(alice, bob, alice_secret, blockr):
    from transactions import Transactions
    transactions = Transactions(testnet=True)
    raw_tx = transactions.create(alice, (bob, 1), min_confirmations=1)
    signed_tx = transactions.sign(raw_tx, alice_secret)
    response = blockr.push_tx(signed_tx, raw=True)
    assert response.status_code == 200
    assert response.json()['status'] == 'success'
    assert response.json()['message'] == ''
    assert response.json()['code'] == 200
    assert response.json()['data']


def test_contruct_transaction(alice_to_bob_tx_data, blockr):
    tx = blockr._construct_transaction(alice_to_bob_tx_data)
    assert tx
    assert tx['confirmations'] == alice_to_bob_tx_data['confirmations']
    assert tx['txid'] == alice_to_bob_tx_data['tx']
    assert 'time' in tx
    assert 'vins' in tx
    assert 'vouts' in tx


def test_import_address(blockr):
    with pytest.raises(NotImplementedError):
        blockr.import_address('dummy')


def test_get_balance_of_one_address(alice, blockr):
    response = blockr.get_balance(alice)
    assert 'balance' in response
    assert 'balance_multisig' in response
    assert response['address'] == alice


def test_get_balance_of_two_addresses(alice, bob, blockr):
    response = blockr.get_balance((alice, bob))
    assert len(response) == 2
    assert all(('balance' in data and 'balance_multisig' in data
                for data in response))
    assert any((data['address'] == alice for data in response))
    assert any((data['address'] == bob for data in response))


def test_get_block_raw(blockr, block_hash):
    block_data = blockr.get_block_raw(block_hash)
    assert block_data['hash'] == block_hash


def test_unsuccessful_make_request(blockr):
    with pytest.raises(Exception) as exc:
        blockr.make_request('https://tbtc.blockr.io/api/v1/tx/info/dummy-tx')
    assert exc.value.args[0] == 'code: 404 message: No records found'
