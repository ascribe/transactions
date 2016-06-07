# -*- coding: utf-8 -*-

from __future__ import unicode_literals


def test_transaction_not_found():
    from transactions.services.exceptions import TransactionNotFound
    e = TransactionNotFound('The grass was greener')
    assert e.message == 'The grass was greener'
    assert e.__str__() == 'The grass was greener'


def test_transaction_error():
    from transactions.services.exceptions import TransactionError
    e = TransactionError('The light was brighter')
    assert e.message == 'The light was brighter'
    assert e.__str__() == 'The light was brighter'
