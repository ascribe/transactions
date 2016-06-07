# -*- coding: utf-8 -*-
"""
Util functions
"""
from __future__ import unicode_literals

import json

import requests


def bitcoin_to_satoshi(amt_bitcoin):
    return int(round(amt_bitcoin * 100000000))
