# -*- coding: utf-8 -*-
"""
Inspired by:

    * https://gist.github.com/shirriff/c9fb5d98e6da79d9a772#file-merkle-py
    * https://github.com/richardkiss/pycoin

"""
from __future__ import absolute_import, division, unicode_literals
from builtins import range

import binascii
import hashlib


def merkleroot(hashes):
    """
    Args:
        hashes: reversed binary form of transactions hashes, e.g.:
            ``binascii.unhexlify(h)[::-1] for h in block['tx']]``
    Returns:
        merkle root in hexadecimal form
    """
    if len(hashes) == 1:
        return binascii.hexlify(bytearray(reversed(hashes[0])))
    if len(hashes) % 2 == 1:
        hashes.append(hashes[-1])
    parent_hashes = []
    for i in range(0, len(hashes)-1, 2):
        first_round_hash = hashlib.sha256(hashes[i] + hashes[i+1]).digest()
        second_round_hash = hashlib.sha256(first_round_hash).digest()
        parent_hashes.append(second_round_hash)
    return merkleroot(parent_hashes)
