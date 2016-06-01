# -*- coding: utf-8 -*-

def test_bitcoin_service_attributes():
    from transactions.services.service import BitcoinService
    assert BitcoinService._min_dust == 3000
    assert BitcoinService.maxTransactionFee == 50000
    assert BitcoinService._min_transaction_fee == 30000


def test_bitcoin_base_service_init_default(bitcoin_base_service_default):
    from transactions.services.service import BitcoinService
    assert bitcoin_base_service_default.testnet is False
    assert bitcoin_base_service_default.name == BitcoinService.__name__


def test_bitcoin_base_service_init_testnet(bitcoin_base_service_testnet):
    from transactions.services.service import BitcoinService
    assert bitcoin_base_service_testnet.testnet is True
    assert bitcoin_base_service_testnet.name == BitcoinService.__name__ + 'Testnet'


def test_bitcoin_daemon_service_init_default(bitcoin_daemon_service_default,
                                             service_username,
                                             service_password,
                                             service_host,
                                             service_port,
                                             bitcoin_daemon_service_url):
    from transactions.services.daemonservice import BitcoinDaemonService
    assert bitcoin_daemon_service_default.testnet is False
    assert bitcoin_daemon_service_default.name == BitcoinDaemonService.__name__
    assert bitcoin_daemon_service_default._username == service_username
    assert bitcoin_daemon_service_default._password == service_password
    assert bitcoin_daemon_service_default._host == service_host
    assert bitcoin_daemon_service_default._port == service_port
    assert bitcoin_daemon_service_default._url == bitcoin_daemon_service_url
    assert bitcoin_daemon_service_default._session


def test_bitcoin_daemon_service_init_default(bitcoin_daemon_service_testnet,
                                             service_username,
                                             service_password,
                                             service_host,
                                             service_port,
                                             bitcoin_daemon_service_url):
    from transactions.services.daemonservice import BitcoinDaemonService
    assert bitcoin_daemon_service_testnet.testnet is True
    assert bitcoin_daemon_service_testnet.name == BitcoinDaemonService.__name__ + 'Testnet'
    assert bitcoin_daemon_service_testnet._username == service_username
    assert bitcoin_daemon_service_testnet._password == service_password
    assert bitcoin_daemon_service_testnet._host == service_host
    assert bitcoin_daemon_service_testnet._port == service_port
    assert bitcoin_daemon_service_testnet._url == bitcoin_daemon_service_url
    assert bitcoin_daemon_service_testnet._session


def test_bitcoin_blockr_service_init_default(bitcoin_blockr_service_default):
    from transactions.services.blockrservice import BitcoinBlockrService
    assert bitcoin_blockr_service_default.testnet is False
    assert bitcoin_blockr_service_default.name == BitcoinBlockrService.__name__
    assert bitcoin_blockr_service_default._url == 'https://btc.blockr.io/api/v1'


def test_bitcoin_base_service_init_default(bitcoin_blockr_service_testnet):
    from transactions.services.blockrservice import BitcoinBlockrService
    assert bitcoin_blockr_service_testnet.testnet is True
    assert bitcoin_blockr_service_testnet.name == BitcoinBlockrService.__name__ + 'Testnet'
    assert bitcoin_blockr_service_testnet._url == 'https://tbtc.blockr.io/api/v1'


def test_make_request(bitcoin_daemon_service_default):
    response = bitcoin_daemon_service_default.make_request('getinfo')
    assert 'id' in response
    assert 'error' in response
    assert 'result' in response
