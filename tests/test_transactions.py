import os
from importlib import import_module

import pytest


alice = 'n12nZmfTbDGCT3VJF5QhPhyVGXvXPzQkFW'
bob = 'mgaUVCq15uywYsqv7dVM4vxVAkq37c44aW'


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


@pytest.mark.skipif(os.environ.get('TRAVIS') == 'true',
                    reason='sslv3 alert handshake failure')
def test_transaction_creation_via_simple_transaction():
    from transactions import Transactions
    trxs = Transactions(testnet=True)
    assert trxs.testnet is True
    simple_transaction = trxs.simple_transaction(alice, (bob, 6))
    assert simple_transaction


@pytest.mark.skipif(os.environ.get('TRAVIS') == 'true',
                    reason='sslv3 alert handshake failure')
def test_transaction_creation_via_create():
    from transactions import Transactions
    trxs = Transactions(testnet=True)
    assert trxs.testnet is True
    simple_transaction = trxs.create(alice, (bob, 6))
    assert simple_transaction
