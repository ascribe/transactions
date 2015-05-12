"""
Defines the main BitcoinService class which other services should subclass
"""


class BitcoinService(object):
    # minimum tx accepted by blockr.io
    _min_dust = 600
    # maximum transaction fee
    maxTransactionFee = 50000
    # minimum mining fee
    _min_transaction_fee = 10000

    def __init__(self, testnet=False):
        self.testnet = testnet

    @property
    def name(self):
        return self.__class__.__name__

