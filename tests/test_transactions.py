alice = 'n12nZmfTbDGCT3VJF5QhPhyVGXvXPzQkFW'
bob = 'mgaUVCq15uywYsqv7dVM4vxVAkq37c44aW'


def test_init_transactions_class_with_defaults():
    from transactions import Transactions
    from transactions.services.blockrservice import BitcoinBlockrService
    trxs = Transactions()
    assert trxs.testnet is False
    assert isinstance(trxs._service, BitcoinBlockrService)
    assert trxs._min_tx_fee == trxs._service._min_transaction_fee
    assert trxs._dust == trxs._service._min_dust


def test_transaction_creation_via_simple_transaction():
    from transactions import Transactions
    trxs = Transactions(testnet=True)
    assert trxs.testnet is True
    simple_transaction = trxs.simple_transaction(alice, (bob, 6))
    import ipdb; ipdb.set_trace()
    assert simple_transaction
