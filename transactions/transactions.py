import pybitcointools

from pycoin.key.BIP32Node import BIP32Node

from services.daemonservice import BitcoinDaemonService
from services.blockrservice import BitcoinBlockrService


SERVICES = ['daemon', 'blockr']


class Transactions(object):
    """
    Transactions: Bitcoin for Humans

    All amounts are in satoshi
    """

    # Transaction fee per 1k bytes
    _min_tx_fee = 10000
    # dust
    _dust = 600

    def __init__(self, service='blockr', testnet=False, username='', password='', host='', port=''):
        if service not in SERVICES:
            raise Exception("Service '{}' not supported".format(service))
        if service == 'daemon':
            self._service = BitcoinDaemonService(username, password, host, port)
        elif service == 'blockr':
            self._service = BitcoinBlockrService(testnet)

    def push(self, tx):
        self._service.push_tx(tx)
        return pybitcointools.txhash(tx)

    def get(self, hash, max_transactions=100, min_confirmations=6):
        # hash can be an address or txid of a transaction
        if len(hash) < 64:
            txs = self._service.list_transactions(hash, max_transactions=max_transactions)
            unspents = self._service.list_unspents(hash, min_confirmations=min_confirmations)
            return {'transactions': txs, 'unspents': unspents}
        else:
            return self._service.get_transaction(hash)

    def _import_address(self, address, label="", rescan=False):
        if self._service.name == 'BitcoinDaemonService':
            self._service.import_address(address, label, rescan=rescan)

    def simple_transaction(self, from_address, to, op_return=None, min_confirmations=6):
        # amount in satoshi
        # to is a tuple of (to_address, amount)
        # or a list of tuples [(to_addr1, amount1), (to_addr2, amount2)]

        to = [to] if not isinstance(to, list) else to
        amount = sum([amount for addr, amount in to])
        n_outputs = len(to) + 1     # change
        if op_return:
            n_outputs += 1

        # select inputs
        inputs, change = self._select_inputs(from_address, amount, n_outputs, min_confirmations=min_confirmations)
        outputs = [{'address': to_address, 'value': amount} for to_address, amount in to]
        outputs += [{'address': from_address, 'value': change}]

        #add op_return
        if op_return:
            outputs += [{'script': self._op_return_hex(op_return), 'value': 0}]
        tx = self.build_transaction(inputs, outputs)
        return tx

    def build_transaction(self, inputs, outputs):
        # prepare inputs and outputs for pybitcointools
        inputs = [{'output': '{}:{}'.format(input['txid'], input['vout']),
                   'value': input['amount']} for input in inputs]
        tx = pybitcointools.mktx(inputs, outputs)
        return tx

    def sign_transaction(self, tx, master_password):
        return pybitcointools.signall(tx, BIP32Node.from_master_secret(master_password).wif())

    def _select_inputs(self, address, amount, n_outputs=2, min_confirmations=6):
        # selects the inputs to fulfill the amount
        # returns a list of inputs and the change
        unspents = self.get(address, min_confirmations=min_confirmations)['unspents']
        if len(unspents) == 0:
            raise Exception("No spendable outputs found")

        unspents = sorted(unspents, key=lambda d: d['amount'])
        balance = 0
        inputs = []
        fee = self._service._min_transaction_fee
        try:
            # get coins to fulfill the amount
            while balance < amount + fee:
                unspent = unspents.pop()
                balance += unspent['amount']
                inputs.append(unspent)
                # update estimated fee
                fee = self._service.estimate_fee(len(inputs), n_outputs)
        except IndexError:
            raise Exception("Not enough balance in the wallet")

        change = balance - amount - fee
        change = change if change > self._dust else 0

        return inputs, change

    def _op_return_hex(self, op_return):
        return "6a%x%s" % (len(op_return), op_return.encode('hex'))