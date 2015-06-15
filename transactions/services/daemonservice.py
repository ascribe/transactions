"""
Bitcoin Daemon Service
"""
import json
import requests

from transactions.services.service import BitcoinService
from transactions.utils import bitcoin_to_satoshi


class BitcoinDaemonService(BitcoinService):
    def __init__(self, username, password, host, port):
        super(BitcoinDaemonService, self).__init__()
        self._username = username
        self._password = password
        self._host = host
        self._port = port

    @property
    def _url(self):
        return 'http://%s:%s@%s:%s' % (self._username, self._password,
                                       self._host, self._port)

    def make_request(self, method, params=[]):
        try:
            data = json.dumps({"jsonrpc": "1.0", "params": params, "id": "", "method": method})
            r = requests.post(self._url, data=data, headers={'Content-type': 'application/json'}, verify=False)
            return json.loads(r.content)
        except ValueError as e:
            print "Some parameters were wrong, please check the request"
            raise
        except requests.exceptions.RequestException as e:
            print "Bitcoin service can not be accessed. Check username, password or host"
            raise

    def push_tx(self, tx):
        """

        :param tx = signed tx hash:
        :return: if successful info on tx, else error tx wasn't pushed
        """
        response = self.make_request("sendrawtransaction", [tx, True])
        error = response.get('error')
        if error is not None:
            raise Exception(error)

        return response

    def import_address(self, address, account="*", rescan=False):
        """
        param address = address to import
        param label= account name to use
        """
        response = self.make_request("importaddress", [address, account, rescan])
        error = response.get('error')
        if error is not None:
            raise Exception(error)
        return response

    def list_transactions(self, address, account="*", max_transactions=200):
        response = self.make_request("listtransactions", [account, max_transactions, 0, True])
        error = response.get('error')
        if error is not None:
            raise Exception(error)

        results = response.get('result', [])
        results = [tx for tx in results if tx.get('address', '') == address and tx.get('category', '') == 'receive']

        out = []
        for tx in results:
            out.append({'txid': tx['txid'],
                        'amount': bitcoin_to_satoshi(tx['amount']),
                        'confirmations': tx['confirmations'],
                        'time': tx['time']})
        return out

    def list_unspents(self, address, min_confirmations):
        response = self.make_request('listunspent', [min_confirmations, 9999999, [address]])
        error = response.get('error')
        if error is not None:
            raise Exception(error)

        results = response.get('result', [])
        out = []
        for unspent in results:
            out.append({'txid': unspent['txid'],
                        'vout': unspent['vout'],
                        'amount': bitcoin_to_satoshi(unspent['amount']),
                        'confirmations': unspent['confirmations']})
        return out

    def get_raw_transaction(self, txid):
        response = self.make_request('getrawtransaction', [txid, 1])
        error = response.get('error')
        if error:
            raise Exception(error)

        raw_transaction = response.get('result')
        return raw_transaction

    def get_transaction(self, txid):
        raw_tx = self.get_raw_transaction(txid)
        result = self._construct_transaction(raw_tx)
        return result

    def _get_address_for_vout(self, txid, vout_n):
        raw_tx = self.get_raw_transaction(txid)
        return [vout['scriptPubKey']['addresses'][0] for vout in raw_tx['vout'] if vout['n'] == vout_n][0]

    def _get_value_from_vout(self, txid, vout_n):
        raw_tx = self.get_raw_transaction(txid)
        return [vout['value'] for vout in raw_tx['vout'] if vout['n'] == vout_n][0]

    def _construct_transaction(self, tx):
        result = {}
        result.update({'confirmations': tx.get('confirmations', ''),
                       'time': tx.get('time', ''),
                       'txid': tx.get('txid', ''),
                       'vins': [{'txid': vin['txid'], 'n': vin['vout'], 'value': bitcoin_to_satoshi(self._get_value_from_vout(vin['txid'], vin['vout'])),
                                 'address': self._get_address_for_vout(vin['txid'], vin['vout'])} for vin in tx.get('vin', [])],
                       'vouts': [{'n': vout['n'], 'value': bitcoin_to_satoshi(vout['value']),
                                  'asm': vout['scriptPubKey']['asm'],
                                  'hex': vout['scriptPubKey']['hex'],
                                  'address': vout['scriptPubKey'].get('addresses', ['NONSTANDARD'])[0]} for vout in tx.get('vout', [])]
                       })
        return result