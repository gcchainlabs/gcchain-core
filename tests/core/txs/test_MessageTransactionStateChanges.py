from unittest import TestCase

from mock import Mock

from gc.core import config
from gc.core.Indexer import Indexer
from gc.core.misc import logger
from gc.core.State import State
from gc.core.StateContainer import StateContainer
from gc.core.OptimizedAddressState import OptimizedAddressState
from gc.core.ChainManager import ChainManager
from gc.core.txs.MessageTransaction import MessageTransaction
from tests.misc.helper import get_alice_xmss, set_gc_dir

logger.initialize_default()


class TestMessageTransactionStateChanges(TestCase):
    def setUp(self):
        with set_gc_dir('no_data'):
            self.state = State()

        self.alice = get_alice_xmss()
        alice_address_state = OptimizedAddressState.get_default(self.alice.address)
        alice_address_state.pbdata.balance = 100
        self.addresses_state = {
            self.alice.address: alice_address_state
        }

        self.params = {
            "message_hash": b'Test Message',
            "addr_to": None,
            "fee": 1,
            "xmss_pk": self.alice.pk
        }
        self.unused_chain_manager_mock = Mock(autospec=ChainManager, name='unused ChainManager')

    def test_apply_message_txn(self):
        tx = MessageTransaction.create(**self.params)
        tx.sign(self.alice)
        addresses_state = dict(self.addresses_state)
        state_container = StateContainer(addresses_state=addresses_state,
                                         tokens=Indexer(b'token', None),
                                         slaves=Indexer(b'slave', None),
                                         lattice_pk=Indexer(b'lattice_pk', None),
                                         multi_sig_spend_txs=dict(),
                                         votes_stats=dict(),
                                         block_number=1,
                                         total_coin_supply=100,
                                         current_dev_config=config.dev,
                                         write_access=True,
                                         my_db=self.state._db,
                                         batch=None)
        tx.apply(self.state, state_container)

        self.assertEqual(addresses_state[self.alice.address].balance, 99)
        storage_key = state_container.paginated_tx_hash.generate_key(self.alice.address, 1)
        self.assertIn(storage_key, state_container.paginated_tx_hash.key_value)
        self.assertEqual([tx.txhash], state_container.paginated_tx_hash.key_value[storage_key])

    def test_revert_message_txn(self):
        tx = MessageTransaction.create(**self.params)
        tx.sign(self.alice)
        addresses_state = dict(self.addresses_state)

        state_container = StateContainer(addresses_state=addresses_state,
                                         tokens=Indexer(b'token', None),
                                         slaves=Indexer(b'slave', None),
                                         lattice_pk=Indexer(b'lattice_pk', None),
                                         multi_sig_spend_txs=dict(),
                                         votes_stats=dict(),
                                         block_number=1,
                                         total_coin_supply=100,
                                         current_dev_config=config.dev,
                                         write_access=True,
                                         my_db=self.state._db,
                                         batch=None)
        tx.apply(self.state, state_container)
        tx.revert(self.state, state_container)

        self.assertEqual(addresses_state[self.alice.address].balance, 100)
        storage_key = state_container.paginated_tx_hash.generate_key(self.alice.address, 1)
        self.assertIn(storage_key, state_container.paginated_tx_hash.key_value)
        self.assertEqual([], state_container.paginated_tx_hash.key_value[storage_key])

    def test_validate_tx(self):
        tx = MessageTransaction.create(**self.params)
        tx.sign(self.alice)

        self.assertTrue(tx.validate_or_raise())

        tx._data.transaction_hash = b'abc'

        # Should fail, as we have modified with invalid transaction_hash
        with self.assertRaises(ValueError):
            tx.validate_or_raise()
