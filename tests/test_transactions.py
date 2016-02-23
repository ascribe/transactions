def test_init_transactions_class_with_defaults():
    from transactions import Transactions
    from transactions.services.blockrservice import BitcoinBlockrService
    trxs = Transactions()
    assert trxs.testnet is False
    assert isinstance(trxs._service, BitcoinBlockrService)
    assert trxs._min_tx_fee == trxs._service._min_transaction_fee
    assert trxs._dust == trxs._service._min_dust
