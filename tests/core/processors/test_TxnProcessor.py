# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
from unittest import TestCase
from mock import Mock, patch

from gc.core.misc import logger
from gc.core.processors.TxnProcessor import TxnProcessor
from gc.core.ChainManager import ChainManager
from gc.core.State import State
from gc.core.OptimizedAddressState import OptimizedAddressState
from gc.core.txs.TransferTransaction import TransferTransaction
from gc.core.TransactionPool import TransactionPool
from tests.misc.helper import replacement_getTime
from gc.core.p2p.p2pfactory import P2PFactory

logger.initialize_default()


def make_tx(txhash=b'hashbrownies', fee=1, autospec=TransferTransaction, PK=b'publickey', **kwargs):
    return Mock(autospec=autospec, txhash=txhash, fee=fee, PK=PK, **kwargs)


@patch('gc.core.processors.TxnProcessor.logger')
@patch('gc.core.txs.Transaction.Transaction.get_slave')
class TestTxnProcessor(TestCase):
    def setUp(self):
        m_state = Mock(name='A Mock State', autospec=State)
        m_state.get_address_state.return_value = Mock(name='A Mock AddressState', autospec=OptimizedAddressState)

        self.chain_manager = Mock(autospec=ChainManager)
        self.chain_manager._state = m_state

        tx_attrs = {
            'validate.return_value': True,  # Custom validation for different Transaction Types
            'validate_extended.return_value': True,  # Master/slave XMSS tree validation; balance & fee, OTS key reuse
            'validate_transaction_pool.return_value': True  # checks for OTS key reuse within TransactionPool only
        }
        self.tx1 = make_tx(name='Mock TX 1', **tx_attrs)
        self.tx2 = make_tx(name='Mock TX 2', **tx_attrs)
        self.tx3 = make_tx(name='Mock TX 3', **tx_attrs)
        self.tx4 = make_tx(name='Mock TX 4', **tx_attrs)

        self.m_txpool = Mock(autospec=TransactionPool)
        self.m_txpool.get_pending_transaction.side_effect = [(self.tx1, replacement_getTime()),
                                                             (self.tx2, replacement_getTime()),
                                                             (self.tx3, replacement_getTime()),
                                                             (self.tx4, replacement_getTime())]

        self.m_broadcast_tx = Mock(autospec=P2PFactory.broadcast_tx)
        self.txnprocessor = TxnProcessor(chain_manager=self.chain_manager,
                                         transaction_pool_obj=self.m_txpool,
                                         broadcast_tx=self.m_broadcast_tx)

    def test_txnprocessor_all_valid(self, m_get_slave, m_logger):
        # Transaction.get_slave() gives you the slave's Qaddress, if the TXN is signed by a slave XMSS tree.
        # If it's a normal TXN signed by the master XMSS tree, it returns None. Since we mocked out validate_extended(),
        # it doesn't really matter what we set here. It's just to make things explicit. Also because class-level patch
        # cannot extend into the setUp() function, only the test_* functions.
        m_get_slave.return_value = b'PUBLICKEY'

        tx_results = [t for t in self.txnprocessor]

        self.assertEqual([True, True, True, True], tx_results)
        self.assertEqual(4, self.m_txpool.add_tx_to_pool.call_count)
        self.assertEqual(4, self.m_broadcast_tx.call_count)

    def test_txnprocessor_tx_validate_fail(self, m_get_slave, m_logger):
        m_get_slave.return_value = None
        self.chain_manager.validate_all.return_value = False
        tx_results = []
        for t in self.txnprocessor:
            tx_results.append(t)
            self.chain_manager.validate_all.return_value = True

        self.assertEqual([False, True, True, True], tx_results)
        self.assertEqual(3, self.m_txpool.add_tx_to_pool.call_count)
        self.assertEqual(3, self.m_broadcast_tx.call_count)

    def test_txnprocessor_tx_validate_extended_fail(self, m_get_slave, m_logger):
        m_get_slave.return_value = None
        self.chain_manager.validate_all.return_value = True
        tx_results = []
        for t in self.txnprocessor:
            tx_results.append(t)
            if len(tx_results) == 3:
                self.chain_manager.validate_all.return_value = True
            else:
                self.chain_manager.validate_all.return_value = False

        m_logger.info.assert_called()
        self.assertEqual([True, False, False, True], tx_results)
        self.assertEqual(2, self.m_txpool.add_tx_to_pool.call_count)
        self.assertEqual(2, self.m_broadcast_tx.call_count)

    def test_txnprocessor_tx_validate_transaction_pool_fail(self, m_get_slave, m_logger):
        m_get_slave.return_value = None
        tx_results = []
        for t in self.txnprocessor:
            tx_results.append(t)
            if len(tx_results) < 2:
                self.chain_manager.validate_all.return_value = True
            else:
                self.chain_manager.validate_all.return_value = False

        m_logger.info.assert_called()
        self.assertEqual([True, True, False, False], tx_results)
        self.assertEqual(2, self.m_txpool.add_tx_to_pool.call_count)
        self.assertEqual(2, self.m_broadcast_tx.call_count)

    def test_txnprocessor_tx_all_failure_modes(self, m_get_slave, m_logger):
        m_get_slave.return_value = None
        tx_results = []
        self.chain_manager.validate_all.return_value = True
        for t in self.txnprocessor:
            tx_results.append(t)
            self.chain_manager.validate_all.return_value = False

        m_logger.info.assert_called()
        self.assertEqual([True, False, False, False], tx_results)
        self.assertEqual(1, self.m_txpool.add_tx_to_pool.call_count)
        self.assertEqual(1, self.m_broadcast_tx.call_count)

    def test_empty(self, m_get_slave, m_logger):
        m_get_slave.return_value = None
        self.m_txpool.get_pending_transaction.side_effect = None
        self.m_txpool.get_pending_transaction.return_value = None

        tx_results = [t for t in self.txnprocessor]

        self.assertEqual([], tx_results)
        self.m_txpool.add_tx_to_pool.assert_not_called()
        self.m_broadcast_tx.assert_not_called()
