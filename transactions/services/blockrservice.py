# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, unicode_literals
from builtins import str

import bitcoin
import requests
import time
from datetime import datetime

from .service import BitcoinService
from transactions.utils import bitcoin_to_satoshi

"""
Blockr Service @ btc.blockr.io
"""


class BitcoinBlockrService(BitcoinService):
    def __init__(self, testnet=False):
        super(BitcoinBlockrService, self).__init__(testnet=testnet)
        self.testnet = testnet

    @property
    def _url(self):
        if self.testnet:
            return 'https://tbtc.blockr.io/api/v1'
        else:
            return 'https://btc.blockr.io/api/v1'

    def make_request(self, url, params=None):
        response = requests.get(url)
        data = response.json()
        if data.get('status') != 'success':
            raise Exception("code: {} message: {}".format(data['code'],
                                                          data['message']))
        return data['data']

    def list_transactions(self, address, raw=False, **kwargs):
        # blockr returns the last 200 transactions
        path = '/address/txs/{}'.format(address)
        url = self._url + path
        results = self.make_request(url)

        if raw:
            return results

        out = []
        for tx in results['txs']:
            out.append({'txid': tx['tx'],
                        'amount': bitcoin_to_satoshi(tx['amount']),
                        'confirmations': tx['confirmations'],
                        'time': self._convert_time(tx['time_utc'])})
        return out

    def list_unspents(self, address, min_confirmations, raw=False):
        unconfirmed = True if min_confirmations == 0 else False
        if unconfirmed:
            path = '/address/unspent/{}?unconfirmed=1'.format(address)
        else:
            path = '/address/unspent/{}'.format(address)
        url = self._url + path
        results = self.make_request(url)

        if raw:
            return results

        out = []
        for unspent in results['unspent']:
            if unspent['confirmations'] >= min_confirmations:
                out.append({'txid': unspent['tx'],
                            'vout': unspent['n'],
                            'amount': bitcoin_to_satoshi(float(unspent['amount'])),
                            'confirmations': unspent['confirmations']})
        return out

    def get_transaction(self, txid, raw=False):
        path = '/tx/info/{}'.format(txid)
        url = self._url + path
        tx = self.make_request(url)
        if raw:
            return tx
        result = self._construct_transaction(tx)
        return result

    def push_tx(self, tx_signed, raw=False):
        # push transactions requires a post to blockr
        path = '/tx/push'
        url = self._url + path
        payload = {'hex': tx_signed}
        response = requests.post(url, data=payload)
        if raw:
            return response
        return bitcoin.txhash(tx_signed)

    def _convert_time(self, time_str):
        """
        Convert a string representation of the time (as returned by blockr.io api) into unix
        timestamp

        :param time_utc_str: string representation of the time
        :return: unix timestamp
        """
        dt = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ")
        return int(time.mktime(dt.utctimetuple()))

    def _construct_transaction(self, tx):
        result = {}
        result.update({'confirmations': tx.get('confirmations', ''),
                       'time': self._convert_time(tx['time_utc']),
                       'txid': tx.get('tx', ''),
                       'vins': [{'txid': vin['vout_tx'], 'n': vin['n'], 'address': vin['address'],
                                 'value': bitcoin_to_satoshi(float(vin['amount']))} for vin in tx.get('vins', [])],
                       'vouts': [{'n': vout['n'], 'value': bitcoin_to_satoshi(float(vout['amount'])),
                                  'asm': vout.get('extras', {}).get('asm', ''),
                                  'hex': vout.get('extras', {}).get('script', ''),
                                  'address': vout['address']} for vout in tx.get('vouts', [])]
                       })
        return result

    def import_address(self, address, account="*", rescan=False):
        """
        param address = address to import
        param label= account name to use
        """
        raise NotImplementedError

    def get_balance(self, addresses, confirmations=None):
        # TODO review
        if not isinstance(addresses, str):
            addresses = ','.join(addresses)
        url = '{}/address/balance/{}'.format(self._url, addresses)
        # TODO add support for confirmations
        return self.make_request(url)

    def decode(self, tx):
        url = self._url + '/tx/decode'
        data = {'hex': tx}
        return requests.post(url, data=data)

    def get_block_raw(self, block):
        """
        Args:
            block: block number (eg: 223212)
                block hash (eg: 0000000000000000210b10d620600dc1cc2380bb58eb2408f9767eb792ed31fa)
                word "last" - this will always return the latest block
                word "first" - this will always return the first block
        Returns:
            raw block data

        """
        url = '{}/block/raw/{}'.format(self._url, block)
        return self.make_request(url)

    def get_block_info(self, block):
        """
        Args:
            block: block number (eg: 223212)
                block hash (eg: 0000000000000000210b10d620600dc1cc2380bb58eb2408f9767eb792ed31fa)
                word "last" - this will always return the latest block
                word "first" - this will always return the first block
        Returns:
            basic block data

        """
        url = '{}/block/info/{}'.format(self._url, block)
        return self.make_request(url)
