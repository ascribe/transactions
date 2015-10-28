"""
Defines the main BitcoinService class which other services should subclass
"""


class BitcoinService(object):
    # minimum tx accepted by blockr.io
    _min_dust = 3000
    # maximum transaction fee
    maxTransactionFee = 50000
    # minimum mining fee
    _min_transaction_fee = 30000

    def __init__(self, testnet=False):
        self.testnet = testnet

    @property
    def name(self):
        test_str = 'Testnet' if self.testnet else ''
        return self.__class__.__name__ + test_str

