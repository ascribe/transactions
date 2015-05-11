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

    def estimate_fee(self, n_inputs, n_outputs):
        # estimates transaction fee based on number of inputs and outputs
        estimated_size = 10 + 148 * n_inputs + 34 * n_outputs
        return (estimated_size / 1000 + 1) * self._min_transaction_fee

