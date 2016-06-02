# -*- coding: utf-8 -*-
"""
Util functions
"""
from __future__ import unicode_literals

import json

import requests


def bitcoin_to_satoshi(amt_bitcoin):
    return int(round(amt_bitcoin * 100000000))


def jsonrpc(url, method=None, params=None, version='1.1'):
    data = json.dumps({
        'jsonrpc': version,
        'params': params,
        'id': '',
        'method': method,
    })
    return requests.post(
        url,
        data=data,
        headers={'Content-type': 'application/json'},
        timeout=30,
        verify=False,
    )
