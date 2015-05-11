"""
Util functions
"""


def bitcoin_to_satoshi(amt_bitcoin):
    return int(round(amt_bitcoin * 100000000))
