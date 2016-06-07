# -*- coding: utf-8 -*-
"""
Custom exceptions
"""
from __future__ import unicode_literals


class TransactionNotFound(Exception):

    """
    Raised when no transaction is found when querying the bitcoin
    daemon for the transaction.
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class TransactionError(Exception):

    """
    Raised when the bitcoin daemon returns an error when trying
    to push a transaction.

    e.g. error = -25 usually indicates a double spend
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
