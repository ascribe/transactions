import json
import pybitcointools
import requests
import time

from transactions.services.service import BitcoinService
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

    def make_request(self, url):
        response = requests.get(url)
        data = json.loads(response.content)
        if data.get('status') != 'success':
            raise Exception("code: {} message: {}".format(data['code'],
                                                          data['message']))
        return data['data']

    def list_transactions(self, address, **kwargs):
        # blockr returns the last 200 transactions
        path = '/address/txs/{}'.format(address)
        url = self._url + path
        results = self.make_request(url)

        out = []
        for tx in results['txs']:
            out.append({'txid': tx['tx'],
                        'amount': bitcoin_to_satoshi(tx['amount']),
                        'confirmations': tx['confirmations'],
                        'time': self._convert_time(tx['time_utc'])})
        return out

    def list_unspents(self, address, min_confirmations):
        unconfirmed = True if min_confirmations == 0 else False
        if unconfirmed:
            path = '/address/unspent/{}?unconfirmed=1'.format(address)
        else:
            path = '/address/unspent/{}'.format(address)
        url = self._url + path
        results = self.make_request(url)

        out = []
        for unspent in results['unspent']:
            if unspent['confirmations'] >= min_confirmations:
                out.append({'txid': unspent['tx'],
                            'vout': unspent['n'],
                            'amount': bitcoin_to_satoshi(float(unspent['amount'])),
                            'confirmations': unspent['confirmations']})
        return out

    def get_transaction(self, txid):
        path = '/tx/info/{}'.format(txid)
        url = self._url + path
        results = self.make_request(url)
        return results

    def push_tx(self, tx_signed):
        # push transactions requires a post to blockr
        path = '/tx/push'
        url = self._url + path
        payload = {'hex': tx_signed}
        response = requests.post(url, data=payload)
        return pybitcointools.txhash(tx_signed)

    def _convert_time(self, time_str):
        return int(time.mktime(time.strptime(time_str, '%Y-%m-%dT%H:%M:%SZ')))
