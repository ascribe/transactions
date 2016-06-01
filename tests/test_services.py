import os


def test_bitcoin_service_attributes():
    from transactions.services.service import BitcoinService
    assert BitcoinService._min_dust == 3000
    assert BitcoinService.maxTransactionFee == 50000
    assert BitcoinService._min_transaction_fee == 30000


def test_bitcoin_service_default_init():
    from transactions.services.service import BitcoinService
    bitcoin_service = BitcoinService()
    assert bitcoin_service.testnet is False
    assert bitcoin_service.name == BitcoinService.__name__


def test_bitcoin_service_init_testnet():
    from transactions.services.service import BitcoinService
    bitcoin_service = BitcoinService(testnet=True)
    assert bitcoin_service.testnet is True
    assert bitcoin_service.name == BitcoinService.__name__ + 'Testnet'


def test_make_request():
    from transactions.services.daemonservice import BitcoinDaemonService
    host = os.environ.get('BITCOIN_HOST', 'localhost')
    rpcuser = os.environ.get('BITCOIN_RPCUSER', 'merlin')
    rpcpassword = os.environ.get('BITCOIN_RPCPASSWORD', 'secret')
    port = os.environ.get('BITCOIN_PORT', 18332)
    s = BitcoinDaemonService(rpcuser, rpcpassword, host, port)
    response = s.make_request('getinfo')
    assert 'id' in response
    assert 'error' in response
    assert 'result' in response
