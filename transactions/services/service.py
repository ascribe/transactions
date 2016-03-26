"""
Defines the main ``BitcoinService`` class which other services should subclass.

"""


class BitcoinService(object):
    """
    Attributes:
        _min_dust (int): Minimum tx accepted by
            `blockr.io <https://blockr.io/>`_. Defaults to``3000``.
        maxTransactionFee (int): Maximum transaction fee. Defaults to
            ``50000``.
        _min_transaction_fee (int): Minimum mining fee. Defaults to ``30000``.

    .. todo:: Give a bit more explanations about each attribute.

    """
    _min_dust = 3000
    maxTransactionFee = 50000
    _min_transaction_fee = 30000

    def __init__(self, testnet=False):
        """
        Args:
            testnet (bool): Set to ``True`` to use the
                `testnet <https://bitcoin.org/en/glossary/testnet>`_. Defaults
                to False, meaning that the
                `mainnet <https://bitcoin.org/en/glossary/mainnet>`_ will be
                used.

        """
        self.testnet = testnet

    @property
    def name(self):
        test_str = 'Testnet' if self.testnet else ''
        return self.__class__.__name__ + test_str
