from unittest import TestCase

import simplejson as json
from mock import patch, PropertyMock
from pygclib.pygclib import bin2hstr

from gc.core import config
from gc.core.Indexer import Indexer
from gc.core.misc import logger
from gc.core.State import State
from gc.core.StateContainer import StateContainer
from gc.core.OptimizedAddressState import OptimizedAddressState
from gc.core.txs.TokenTransaction import TokenTransaction
from gc.core.txs.Transaction import Transaction
from gc.generated import gc_pb2
from tests.core.txs.testdata import test_json_Token, test_signature_Token
from tests.misc.helper import get_alice_xmss, get_bob_xmss, get_slave_xmss, set_gc_dir

logger.initialize_default()


@patch('gc.core.txs.Transaction.logger')
class TestTokenTransaction(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestTokenTransaction, self).__init__(*args, **kwargs)
        with set_gc_dir('no_data'):
            self.state = State()
        self.alice = get_alice_xmss()
        self.bob = get_bob_xmss()
        self._decimals = 15

        self.alice.set_ots_index(10)
        self.maxDiff = None

    def setUp(self):
        self.initial_balances_valid = [gc_pb2.AddressAmount(address=self.alice.address, amount=1000),
                                       gc_pb2.AddressAmount(address=self.bob.address, amount=1000)]

        self.params = {"symbol": b'gc',
                       "name": b'Quantum Resistant Ledger',
                       "owner": self.alice.address,
                       "decimals": self._decimals,
                       "initial_balances": self.initial_balances_valid,
                       "fee": 1,
                       "xmss_pk": self.alice.pk}

    def make_tx(self, **kwargs):
        self.params.update(kwargs)
        tx = TokenTransaction.create(**self.params)
        return tx

    def test_create(self, m_logger):
        # Alice creates Token
        initial_balances = list()
        initial_balances.append(gc_pb2.AddressAmount(address=self.alice.address,
                                                      amount=400000000))
        initial_balances.append(gc_pb2.AddressAmount(address=self.bob.address,
                                                      amount=200000000))

        tx = self.make_tx(decimals=4, initial_balances=initial_balances)

        self.assertTrue(tx)

    def test_create_negative_fee(self, m_logger):
        with self.assertRaises(ValueError):
            TokenTransaction.create(symbol=b'gc',
                                    name=b'Quantum Resistant Ledger',
                                    owner=self.alice.address,
                                    decimals=4,
                                    initial_balances=[],
                                    fee=-1,
                                    xmss_pk=self.alice.pk)

    def test_to_json(self, m_logger):
        initial_balances = list()
        initial_balances.append(gc_pb2.AddressAmount(address=self.alice.address,
                                                      amount=400000000))
        initial_balances.append(gc_pb2.AddressAmount(address=self.bob.address,
                                                      amount=200000000))
        tx = TokenTransaction.create(symbol=b'gc',
                                     name=b'Quantum Resistant Ledger',
                                     owner=b'\x01\x03\x17F=\xcdX\x1bg\x9bGT\xf4ld%\x12T\x89\xa2\x82h\x94\xe3\xc4*Y\x0e\xfbh\x06E\x0c\xe6\xbfRql',
                                     decimals=4,
                                     initial_balances=initial_balances,
                                     fee=1,
                                     xmss_pk=self.alice.pk)
        txjson = tx.to_json()

        self.assertEqual(json.loads(test_json_Token), json.loads(txjson))

    def test_from_json(self, m_logger):
        tx = Transaction.from_json(test_json_Token)
        tx.sign(self.alice)
        self.assertIsInstance(tx, TokenTransaction)

        # Test that common Transaction components were copied over.
        self.assertEqual('010300a1da274e68c88b0ccf448e0b1916fa789b01eb2ed4e9ad565ce264c9390782a9c61ac02f',
                         bin2hstr(tx.addr_from))
        self.assertEqual('01030038ea6375069f8272cc1a6601b3c76c21519455603d370036b97c779ada356'
                         '5854e3983bd564298c49ae2e7fa6e28d4b954d8cd59398f1225b08d6144854aee0e',
                         bin2hstr(tx.PK))
        self.assertEqual(b'gc', tx.symbol)
        self.assertEqual(b'Quantum Resistant Ledger', tx.name)
        self.assertEqual('010317463dcd581b679b4754f46c6425125489a2826894e3c42a590efb6806450ce6bf52716c',
                         bin2hstr(tx.owner))
        self.assertEqual('ff84da605e9c9cd04d68503be7922110b4cc147837f8687ad18aa54b7bc5632d', bin2hstr(tx.txhash))
        self.assertEqual(10, tx.ots_key)

        self.assertEqual(test_signature_Token, bin2hstr(tx.signature))

        total_supply = 0
        for initial_balance in tx.initial_balances:
            total_supply += initial_balance.amount
        self.assertEqual(600000000, total_supply)

        self.assertEqual(1, tx.fee)

    def test_validate_tx(self, m_logger):
        initial_balances = list()
        initial_balances.append(gc_pb2.AddressAmount(address=self.alice.address,
                                                      amount=400000000))
        initial_balances.append(gc_pb2.AddressAmount(address=self.bob.address,
                                                      amount=200000000))

        tx = self.make_tx(decimals=4, initial_balances=initial_balances)

        # We must sign the tx before validation will work.
        tx.sign(self.alice)

        # We have not touched the tx: validation should pass.
        self.assertTrue(tx.validate_or_raise())

    def test_validate_tx2(self, m_logger):
        initial_balances = list()
        initial_balances.append(gc_pb2.AddressAmount(address=self.alice.address,
                                                      amount=10000000000000000001))
        initial_balances.append(gc_pb2.AddressAmount(address=self.bob.address,
                                                      amount=10000000000000000001))

        # Transaction Validation should fail as the decimals is higher than the possible decimals
        with self.assertRaises(ValueError):
            self.make_tx(decimals=4, initial_balances=initial_balances)

    def test_validate_tx3(self, m_logger):
        initial_balances = list()
        initial_balances.append(gc_pb2.AddressAmount(address=self.alice.address,
                                                      amount=1000 * 10 ** self._decimals))
        initial_balances.append(gc_pb2.AddressAmount(address=self.bob.address,
                                                      amount=1000 * 10 ** self._decimals))

        tx = self.make_tx(initial_balances=initial_balances)

        # We must sign the tx before validation will work.
        tx.sign(self.alice)

        # We have not touched the tx: validation should pass.
        self.assertTrue(tx.validate_or_raise())

    def test_validate_tx4(self, m_logger):
        initial_balances = list()
        initial_balances.append(gc_pb2.AddressAmount(address=self.alice.address,
                                                      amount=1000 * 10 ** self._decimals))
        initial_balances.append(gc_pb2.AddressAmount(address=self.bob.address,
                                                      amount=1000 * 10 ** self._decimals))

        tx = self.make_tx(initial_balances=initial_balances)

        tx.sign(self.alice)

        self.assertTrue(tx.validate_or_raise())

        tx._data.transaction_hash = b'abc'

        with self.assertRaises(ValueError):
            tx.validate_or_raise()

    @patch('gc.core.txs.Transaction.Transaction.validate_slave', return_value=True)
    def test_validate_extended(self, m_validate_slave, m_logger):
        """
        TokenTransaction._validate_extended checks for:
        1. valid master/slave
        2. from address is valid
        3. owner address is valid
        4. addresses that own the initial balances are valid
        5. that the AddressState has enough coins to pay the Transaction fee (because no coins are being transferred)
        6. OTS key reuse
        """
        alice_address_state = OptimizedAddressState.get_default(self.alice.address)
        alice_address_state.pbdata.balance = 100

        tx = TokenTransaction.create(**self.params)
        tx.sign(self.alice)
        addresses_state = {
            alice_address_state.address: alice_address_state
        }
        state_container = StateContainer(addresses_state=addresses_state,
                                         tokens=Indexer(b'token', None),
                                         slaves=Indexer(b'slave', None),
                                         lattice_pk=Indexer(b'lattice_pk', None),
                                         multi_sig_spend_txs=dict(),
                                         votes_stats=dict(),
                                         block_number=1,
                                         total_coin_supply=1000,
                                         current_dev_config=config.dev,
                                         write_access=True,
                                         my_db=self.state._db,
                                         batch=None)
        result = tx._validate_extended(state_container)
        self.assertTrue(result)

        m_validate_slave.return_value = False
        result = tx.validate_all(state_container)
        self.assertFalse(result)
        m_validate_slave.return_value = True

        with patch('gc.core.txs.TokenTransaction.TokenTransaction.addr_from',
                   new_callable=PropertyMock) as m_addr_from:
            m_addr_from.return_value = b'Invalid Address'
            result = tx._validate_extended(state_container)
            self.assertFalse(result)

        with patch('gc.core.txs.TokenTransaction.TokenTransaction.owner', new_callable=PropertyMock) as m_owner:
            m_owner.return_value = b'Invalid Address'
            result = tx._validate_extended(state_container)
            self.assertFalse(result)

        with patch('gc.core.txs.TokenTransaction.TokenTransaction.initial_balances',
                   new_callable=PropertyMock) as m_address_balance:
            m_address_balance.return_value = [gc_pb2.AddressAmount(address=b'Invalid Address 1', amount=1000),
                                              gc_pb2.AddressAmount(address=b'Invalid Address 2', amount=1000)]
            result = tx._validate_extended(state_container)
            self.assertFalse(result)

        alice_address_state.pbdata.balance = 0
        result = tx._validate_extended(state_container)
        self.assertFalse(result)
        alice_address_state.pbdata.balance = 100

        addresses_state = {
            self.alice.address: alice_address_state
        }
        # addr_from_pk has used this OTS key before
        state_container.paginated_bitfield.set_ots_key(addresses_state, alice_address_state.address, tx.ots_key)
        result = tx.validate_all(state_container)
        self.assertFalse(result)

        # Token symbol too long
        tx = self.make_tx(symbol=b'gcSgcSgc')
        tx.sign(self.alice)
        self.assertFalse(tx._validate_extended(state_container))

        # Token name too long
        tx = self.make_tx(name=b'Quantum Resistant LedgerQuantum')
        tx.sign(self.alice)
        self.assertFalse(tx._validate_extended(state_container))

        # Token symbol missing
        with self.assertRaises(ValueError):
            tx = self.make_tx(symbol=b'')
            tx.sign(self.alice)
            self.assertFalse(tx._validate_extended(state_container))

        # Token name missing
        with self.assertRaises(ValueError):
            tx = self.make_tx(name=b'')
            tx.sign(self.alice)
            tx._validate_extended(state_container)

        # Empty initial_balances
        with self.assertRaises(ValueError):
            tx = self.make_tx(initial_balances=[])
            tx.sign(self.alice)
            self.assertFalse(tx._validate_extended(state_container))

        # Invalid initial balances... 0!
        with self.assertRaises(ValueError):
            initial_balances_0_0 = [gc_pb2.AddressAmount(address=self.alice.address, amount=0),
                                    gc_pb2.AddressAmount(address=self.bob.address, amount=0)]
            tx = self.make_tx(initial_balances=initial_balances_0_0)
            tx.sign(self.alice)
            self.assertFalse(tx._validate_extended(state_container))

        # Fee is -1
        with patch('gc.core.txs.TokenTransaction.TokenTransaction.fee', new_callable=PropertyMock) as m_fee:
            m_fee.return_value = -1
            with self.assertRaises(ValueError):
                tx = self.make_tx()
                tx.sign(self.alice)

        # Invalid initial balances... -1!
        # tx = self.make_tx()
        # tx.sign(self.alice)
        # with patch('gc.core.txs.TokenTransaction.TokenTransaction.initial_balances', new_callable=PropertyMock) as m_i_balances:
        #     m_i_balances.return_value = [-1, -1]
        #     with self.assertRaises(ValueError):
        #         tx.validate_or_raise()

    def test_affected_address(self, m_logger):
        tx = TokenTransaction.create(**self.params)
        # Default params should result in 2 affected addresses
        result = set()
        tx.set_affected_address(result)
        self.assertEqual(2, len(result))

        # If the slave is a recipient of tokens, he should be included too.
        slave = get_slave_xmss()
        result = set()
        self.initial_balances_valid.append(gc_pb2.AddressAmount(address=slave.address, amount=1000))
        tx = TokenTransaction.create(symbol=b'gc',
                                     name=b'Quantum Resistant Ledger',
                                     owner=self.alice.address,
                                     decimals=15,
                                     initial_balances=self.initial_balances_valid,
                                     fee=1,
                                     xmss_pk=self.alice.pk)
        tx.set_affected_address(result)
        self.assertEqual(3, len(result))
