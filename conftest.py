# -*- coding: utf-8 -*-

import pytest

@pytest.fixture
def alice():
    return 'n12nZmfTbDGCT3VJF5QhPhyVGXvXPzQkFW';


@pytest.fixture
def bob():
    return 'mgaUVCq15uywYsqv7dVM4vxVAkq37c44aW';


@pytest.fixture
def carol():
    return 'mtWg6ccLiZWw2Et7E5UqmHsYgrAi5wqiov';


@pytest.fixture
def service_username():
    return 'username'


@pytest.fixture
def service_password():
    return 'password'


@pytest.fixture
def service_host():
    return 'localhost'


@pytest.fixture
def service_port():
    return '8000'


@pytest.fixture
def bitcoin_base_service_default():
    from transactions.services.service import BitcoinService
    return BitcoinService()


@pytest.fixture
def bitcoin_base_service_testnet():
    from transactions.services.service import BitcoinService
    return BitcoinService(testnet=True)


@pytest.fixture
def bitcoin_daemon_service_default(service_username, service_password, service_host, service_port):
    from transactions.services.daemonservice import BitcoinDaemonService
    return BitcoinDaemonService(service_username, service_password, service_host, service_port)


@pytest.fixture
def bitcoin_daemon_service_testnet(service_username, service_password, service_host, service_port):
    from transactions.services.daemonservice import BitcoinDaemonService
    return BitcoinDaemonService(service_username, service_password, service_host, service_port, testnet=True)


@pytest.fixture
def bitcoin_daemon_service_url(service_username, service_password, service_host, service_port):
    return 'http://%s:%s@%s:%s' % (service_username, service_password, service_host, service_port)

@pytest.fixture
def bitcoin_blockr_service_default():
    from transactions.services.blockrservice import BitcoinBlockrService
    return BitcoinBlockrService()


@pytest.fixture
def bitcoin_blockr_service_testnet():
    from transactions.services.blockrservice import BitcoinBlockrService
    return BitcoinBlockrService(testnet=True)
