from unittest import TestCase
from mock import Mock, patch, PropertyMock, mock

from gc.core import config
from gc.core.misc import logger
from gc.core.OptimizedAddressState import OptimizedAddressState
from gc.core.Block import Block
from gc.core.BlockMetadata import BlockMetadata
from gc.core.ESyncState import ESyncState
from gc.core.gcnode import gcNode
from gc.core.State import State
from gc.core.ChainManager import ChainManager
from gc.core.TransactionPool import TransactionPool
from gc.core.txs.CoinBase import CoinBase
from gc.core.txs.TransferTransaction import TransferTransaction
from gc.core.p2p.p2pprotocol import P2PProtocol
from gc.core.p2p.p2pPeerManager import P2PPeerManager
from gc.core.p2p.p2pChainManager import P2PChainManager
from gc.core.node import POW
from gc.generated import gc_pb2
from pygclib.pygclib import hstr2bin

from tests.misc.MockHelper.mock_get_tx_metadata import GetTXMetadata
from tests.core.test_State import gen_blocks
from tests.misc.helper import set_gc_dir, get_alice_xmss, get_slave_xmss, replacement_getTime, get_random_xmss

logger.initialize_default()


alice = get_alice_xmss()
slave = get_slave_xmss()


@patch('gc.core.misc.ntp.getTime', new=replacement_getTime)
class TestgcNodeReal(TestCase):
    @patch('gc.core.misc.ntp.getTime', new=replacement_getTime)
    def setUp(self):
        # You have to set_gc_dir to an empty one, otherwise State will have some Transactions from disk
        with set_gc_dir('no_data'):
            self.db_state = State()
            self.chainmanager = ChainManager(self.db_state)
            self.gcnode = gcNode(mining_address=b'')
            self.gcnode.set_chain_manager(self.chainmanager)

    @patch('gc.core.gcnode.gcNode.block_height', new_callable=PropertyMock, return_value=19)
    def test_get_latest_blocks(self, m_height):
        # [Block 0, Block 1, Block 2... Block 19]
        blocks = gen_blocks(20, self.db_state, alice.address)

        # get_latest_blocks(offset=0, count=1) from [Block 0.... Block 19] should return [Block 19]
        latest_blocks = self.gcnode.get_latest_blocks(0, 1)
        self.assertTrue(latest_blocks[0] == blocks[19])  # These are different instances, so cannot use assertEqual

        # get_latest_blocks(offset=0, count=2) from [Block 0.... Block 19] should return [Block 18, Block 19]
        latest_blocks = self.gcnode.get_latest_blocks(0, 2)
        self.assertTrue(latest_blocks[0] == blocks[18])
        self.assertTrue(latest_blocks[1] == blocks[19])

        # get_latest_blocks(offset=10, count=3) from [Block 0.... Block 19] should return [Block 7 - Block 9]
        latest_blocks = self.gcnode.get_latest_blocks(10, 3)
        self.assertTrue(latest_blocks[0] == blocks[7])
        self.assertTrue(latest_blocks[1] == blocks[8])
        self.assertTrue(latest_blocks[2] == blocks[9])


@patch('gc.core.misc.ntp.getTime', new=replacement_getTime)
class TestgcNode(TestCase):
    @patch('gc.core.misc.ntp.getTime', new=replacement_getTime)
    def setUp(self):
        self.db_state = Mock(autospec=State, name='mocked State')
        # self.db_state = State()

        self.gcnode = gcNode(mining_address=b'')

        # As the gcNode is instantiated and torn down for each test, the minuscule or negative diff between present
        # time and start_time can cause problems.
        self.gcnode.start_time -= 10

        self.gcnode._pow = Mock(autospec=POW)
        self.gcnode._pow.miner.lock.__enter__ = Mock()
        self.gcnode._pow.miner.lock.__exit__ = Mock()

        self.gcnode.peer_manager = Mock(autospec=P2PPeerManager, name='mock P2PPeerManager',
                                         known_peer_addresses=set())
        self.gcnode.p2pchain_manager = Mock(autospec=P2PChainManager, name='mock P2PChainManager')

        self.chain_manager = ChainManager(self.db_state)
        self.chain_manager.tx_pool = Mock(autospec=TransactionPool)
        mock_last_block = Mock(autospec=Block, name='mock last Block', block_number=2, headerhash=b'deadbeef')
        self.chain_manager._last_block = mock_last_block
        self.chain_manager.get_unconfirmed_transaction = Mock()

        self.gcnode.set_chain_manager(self.chain_manager)

    @patch('gc.core.BlockMetadata.BlockMetadata.get_block_metadata')
    def test_monitor_chain_state_no_peer_with_higher_difficulty_found(self, mock_get_block_metadata):
        """
        gcNode.monitor_chain_state() basically:
        1. Tells P2PPeerManager to clean the list of channels/P2PProtocols, i.e. remove any we haven't heard
        from for a long time, and make sure our list of channels and the list of their statuses is in sync.
        2. Gets the last block from the State
        3. Broadcasts our State based on the last Block to our peers
        4. Ask P2PPeerManager to return the channel (if any) who has a higher difficulty than our chain.
        If no channel with a higher difficulty is found, nothing else happens.
        """
        m_block = Mock(autospec=Block, name='mock last Block', block_number=2, headerhash=b'deadbeef')
        m_block_metadata = Mock(autospec=BlockMetadata, cumulative_difficulty=hstr2bin('01'))
        self.gcnode.peer_manager.get_better_difficulty.return_value = None
        mock_get_block_metadata.return_value = m_block_metadata
        self.chain_manager.last_block.return_value = m_block

        self.gcnode.monitor_chain_state()

        self.gcnode.peer_manager.monitor_chain_state.assert_called_once()
        self.gcnode.peer_manager.get_better_difficulty.assert_called_once()

    @patch('gc.core.BlockMetadata.BlockMetadata.get_block_metadata')
    def test_monitor_chain_state_peer_with_higher_difficulty_found(self, mock_get_block_metadata):
        """
        gcNode.monitor_chain_state() basically:
        1. Tells P2PPeerManager to clean the list of channels/P2PProtocols, i.e. remove any we haven't heard
        from for a long time, and make sure our list of channels and the list of their statuses is in sync.
        2. Gets the last block from the State
        3. Broadcasts our State based on the last Block to our peers
        4. Ask P2PPeerManager to return the channel (if any) who has a higher difficulty than our chain.
        If a channel with a higher difficulty is found, get its list of headerhashes.
        """
        m_block = Mock(autospec=Block, name='mock last Block', block_number=2, headerhash=b'deadbeef')
        m_block_metadata = Mock(autospec=BlockMetadata, cumulative_difficulty=hstr2bin('01'))
        m_channel = Mock(autospec=P2PProtocol, addr_remote='1.1.1.1')
        self.gcnode.peer_manager.get_better_difficulty.return_value = m_channel
        mock_get_block_metadata.return_value = m_block_metadata
        self.chain_manager._last_block = m_block

        self.gcnode.monitor_chain_state()

        self.gcnode.peer_manager.monitor_chain_state.assert_called_once()
        self.gcnode.peer_manager.get_better_difficulty.assert_called_once()
        m_channel.send_get_headerhash_list.assert_called_once()

    def test_start_listening(self):
        """
        start_listening() is a convenience function that creates a P2PFactory and connects various components to it
        so that the P2PFactory can function.
        It connects itself, the ChainManager, and the PeerManager to the P2PFactory.
        Then it just tells the P2PFactory to start listening.
        Not much to test here.
        """
        self.assertIsNone(self.gcnode._p2pfactory)
        self.gcnode.start_listening()
        self.assertIsNotNone(self.gcnode._p2pfactory)

    def test_get_address_is_used(self):
        """
        gcNode.get_address_is_used() asks the DB (State) if a particular address has ever been used.
        It also validates the address before sending it to the State.
        """
        self.db_state.get_address_is_used.return_value = True
        result = self.gcnode.get_address_is_used(alice.address)
        self.assertTrue(result)

        self.db_state.get_address_is_used.return_value = False
        result = self.gcnode.get_address_is_used(alice.address)
        self.assertFalse(result)

        with self.assertRaises(ValueError):
            self.gcnode.get_address_is_used(b'fdsa')

    @patch('gc.core.PaginatedData.PaginatedData.get_paginated_data')
    @patch('gc.core.OptimizedAddressState.OptimizedAddressState.get_optimized_address_state')
    @patch('gc.core.TransactionMetadata.TransactionMetadata.get_tx_metadata')
    def test_get_mini_transactions_by_address(self,
                                              mock_get_tx_metadata,
                                              mock_get_optimized_address_state,
                                              mock_get_paginated_data):
        """
        gcNode.get_transactions_by_address() returns all the changes in balance caused by a transaction.
        """
        get_tx_metadata = GetTXMetadata()

        xmss = get_alice_xmss()
        xmss2 = get_random_xmss()
        addr_state = OptimizedAddressState.get_default(xmss.address)
        addr_state.pbdata.balance = 100
        addr_state.pbdata.transaction_hash_count = 3
        mock_get_optimized_address_state.return_value = addr_state

        tx1 = CoinBase.create(config.dev, 100, xmss.address, 5)
        get_tx_metadata.register_tx_metadata(tx1, 1)

        tx2 = TransferTransaction.create(addrs_to=[xmss2.address],
                                         amounts=[10],
                                         message_data=None,
                                         fee=1,
                                         xmss_pk=xmss.pk)
        tx2.sign(xmss)
        get_tx_metadata.register_tx_metadata(tx2, 1)

        tx3 = TransferTransaction.create(addrs_to=[xmss.address],
                                         amounts=[100],
                                         message_data=None,
                                         fee=1,
                                         xmss_pk=xmss2.pk)
        tx3.sign(xmss)
        get_tx_metadata.register_tx_metadata(tx3, 2)

        mock_get_paginated_data.return_value = [tx1.txhash, tx2.txhash, tx3.txhash]
        mock_get_tx_metadata.side_effect = get_tx_metadata.get_tx_metadata
        response = self.gcnode.get_mini_transactions_by_address(alice.address, 3, 1)
        result, balance = response.mini_transactions, response.balance
        self.assertEqual(len(result), 3)

        self.assertEqual(result[0].amount, 100)
        self.assertEqual(result[0].out, False)

        self.assertEqual(result[1].amount, 11)
        self.assertEqual(result[1].out, True)

        self.assertEqual(result[2].amount, 100)
        self.assertEqual(result[2].out, False)

        self.assertEqual(balance, 100)

    @patch('gc.core.OptimizedAddressState.OptimizedAddressState.get_optimized_address_state')
    def test_get_optimized_address_state(self, mock_get_optimized_address_state):
        """
        gcNode.get_address_state() asks the DB (State) for an Address's AddressState, like its nonce, ots index...
        It also validates the address before sending it to the State.
        """
        m_addr_state = Mock(autospec=OptimizedAddressState)
        mock_get_optimized_address_state.return_value = m_addr_state
        result = self.gcnode.get_optimized_address_state(alice.address)
        self.assertEqual(m_addr_state, result)

        # Fetching AddressState for Coinbase Address
        m_addr_state = Mock(autospec=OptimizedAddressState)
        mock_get_optimized_address_state.return_value = m_addr_state
        result = self.gcnode.get_optimized_address_state(config.dev.coinbase_address)
        self.assertEqual(m_addr_state, result)

        with self.assertRaises(ValueError):
            self.gcnode.get_optimized_address_state(b'fdsa')

    def test_get_addr_from(self):
        """
        A master XMSS tree may use a slave XMSS tree to sign for it. If this is the case, we still want to say that the
        TX came from the master XMSS tree, not the slave.
        """
        answer = self.gcnode.get_addr_from(slave.pk, alice.address)
        self.assertEqual(answer, alice.address)

        answer = self.gcnode.get_addr_from(slave.pk, None)
        self.assertEqual(answer, slave.address)

    # Just testing that these wrapper functions are doing what they're supposed to do.
    @patch("gc.core.TransactionMetadata.TransactionMetadata.get_tx_metadata")
    def test_get_transaction(self, mock_get_tx_metadata):
        self.gcnode.get_transaction(b'a txhash')
        mock_get_tx_metadata.assert_called_once_with(self.db_state, b'a txhash')

    def test_get_unconfirmed_transaction(self):
        self.gcnode.get_unconfirmed_transaction(b'a txhash')
        self.chain_manager.get_unconfirmed_transaction.assert_called_once_with(b'a txhash')

    def test_get_block_last(self):
        self.assertEqual(self.gcnode.get_block_last().block_number, 2)

    @patch('gc.core.Block.Block.get_block')
    def test_get_block_from_hash(self, mock_get_block):
        self.gcnode.get_block_from_hash(b'a blockhash')
        mock_get_block.assert_called_once_with(self.db_state, b'a blockhash')

    @patch('gc.core.Block.Block.get_block_by_number')
    def test_get_block_from_index(self, mock_get_block_by_number):
        self.gcnode.get_block_from_index(3)
        mock_get_block_by_number.assert_called_once_with(self.db_state, 3)

    @patch('gc.core.TransactionMetadata.TransactionMetadata.get_tx_metadata')
    def test_get_blockidx_from_txhash(self, mock_get_tx_metadata):
        # self.db_state.get_tx_metadata.return_value = (Mock(name='Mock TX'), 3)
        mock_get_tx_metadata.return_value = (Mock(name='Mock TX'), 3)
        result = self.gcnode.get_blockidx_from_txhash(b'a txhash')
        self.assertEqual(result, 3)

        mock_get_tx_metadata.return_value = None
        result = self.gcnode.get_blockidx_from_txhash(b'a txhash')
        self.assertIsNone(result)

    @patch('gc.core.BlockMetadata.BlockMetadata.get_block_metadata')
    def test_get_block_to_mine(self, m_get_block_metadata):
        m_block = Mock(autospec=Block, name='mock Block')
        m_block_metadata = Mock(autospec=BlockMetadata, name='mock BlockMetadata', block_difficulty=0)

        with mock._patch_object(ChainManager, 'last_block') as m_last_block:
            m_last_block.__get__ = Mock(return_value=m_block)
            m_get_block_metadata.return_value = m_block_metadata

            self.gcnode.get_block_to_mine(alice.address)

            m_last_block.__get__.assert_called_once()
            m_get_block_metadata.assert_called_once()
            self.gcnode._pow.miner.get_block_to_mine.assert_called_once_with(alice.address, self.chain_manager.tx_pool,
                                                                              m_block, 0)

    def test_submit_mined_block(self):
        self.gcnode.submit_mined_block(b'blob')
        self.gcnode._pow.miner.submit_mined_block.assert_called_once_with(b'blob')

    def test_get_node_info(self):
        # I guess this test is useful for making sure every part of gcNode is adequately mocked
        ans = self.gcnode.get_node_info()
        self.assertIsInstance(ans, gc_pb2.NodeInfo)

    @patch('gc.core.LastTransactions.LastTransactions.get_last_txs')
    def test_get_latest_transactions(self, mock_get_last_txs):
        """
        This returns the last n txs, just like get_latest_blocks().
        Useful for the Block Explorer, presumably.
        """
        # get_last_txs returns the latest transactions
        mock_get_last_txs.return_value = [Mock(name='mock TX {}'.format(i), i=i) for i in range(19, -1, -1)]

        # Given [0, 1, 2... 19], with offset 0 count 1 should return [19]
        result = self.gcnode.get_latest_transactions(0, 1)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].i, 19)

        # Given [0, 1, 2... 19], with offset 2 count 3 should return [15, 16, 17]
        result = self.gcnode.get_latest_transactions(2, 3)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].i, 17)
        self.assertEqual(result[1].i, 16)
        self.assertEqual(result[2].i, 15)

    def test_get_block_timeseries(self):
        """
        get_block_timeseries() returns a list of stats for the last n blocks.
        The resultant list is in ascending order of time.
        Useful for the Block Explorer, definitely.
        """
        m_blockdps = {
            b'1': Mock(name='BlockDatapoint 1', header_hash=b'1', header_hash_prev=None),
            b'2': Mock(name='BlockDatapoint 2', header_hash=b'2', header_hash_prev=b'1'),
            b'3': Mock(name='BlockDatapoint 3', header_hash=b'3', header_hash_prev=b'2'),
            b'4': Mock(name='BlockDatapoint 4', header_hash=b'4', header_hash_prev=b'3'),
            b'5': Mock(name='BlockDatapoint 5', header_hash=b'5', header_hash_prev=b'4')
        }
        m_blockdps_as_list = [m_blockdps[key] for key in sorted(m_blockdps.keys())]

        self.chain_manager._last_block = Mock(name='Block 5', headerhash=b'5', block_number=5)

        def replacement_get_block_datapoint(headerhash_current):
            return m_blockdps.get(headerhash_current)

        self.chain_manager.get_block_datapoint = replacement_get_block_datapoint

        # Get last 5 blocks should return [BlockDatapoint 1, BlockDatapoint 2... BlockDatapoint 5]
        result = self.gcnode.get_block_timeseries(5)
        result_converted_from_iterator = [r for r in result]
        self.assertEqual(result_converted_from_iterator, m_blockdps_as_list)

        # Get last 3 blocks should return [BlockDatapoint 3, BlockDatapoint 4... BlockDatapoint 5]
        result = self.gcnode.get_block_timeseries(3)
        result_converted_from_iterator = [r for r in result]
        self.assertEqual(result_converted_from_iterator, m_blockdps_as_list[2:])

        # If we have a blockheight of 0, return []
        with patch('gc.core.gcnode.gcNode.block_height', new_callable=PropertyMock, return_value=0):
            result = self.gcnode.get_block_timeseries(3)
            result_converted_from_iterator = [r for r in result]  # []
            self.assertFalse(result_converted_from_iterator)

        # If chain_manager.last_block() returns a None, return [] (how is this different from blockheight=0?)
        self.chain_manager._last_block = None
        result = self.gcnode.get_block_timeseries(5)
        result_converted_from_iterator = [r for r in result]
        self.assertFalse(result_converted_from_iterator)
        self.chain_manager._last_block = Mock(name='Block 5', headerhash=b'5', block_number=5)

        # If we request 6 blocks when we actually have 5, it should still return 5 objects.
        result = self.gcnode.get_block_timeseries(6)
        result_converted_from_iterator = [r for r in result]
        self.assertEqual(result_converted_from_iterator, m_blockdps_as_list)

    @patch('gc.core.BlockMetadata.BlockMetadata.get_block_metadata')
    @patch('gc.core.Block.Block.get_block_by_number')
    @patch('gc.core.ChainManager.ChainManager.height', new_callable=PropertyMock, return_value=3)
    def test_get_blockheader_and_metadata(self, m_height, m_get_block_by_number, m_get_block_metadata):
        blocks = []
        for i in range(0, 4):
            m = Mock(name='mock Block {}'.format(i), i=i)
            m.blockheader.headerhash = str(i).encode()
            blocks.append(m)

        block_metadata = {
            b'0': Mock(name='mock BlockMetadata 0', i=0),
            b'1': Mock(name='mock BlockMetadata 1', i=1),
            b'2': Mock(name='mock BlockMetadata 2', i=2),
            b'3': Mock(name='mock BlockMetadata 3', i=3),
        }

        def replacement_get_block_by_number(state, idx):
            return blocks[idx]

        def replacement_get_block_metadata(state, headerhash):
            return block_metadata[headerhash]

        m_get_block_by_number.side_effect = replacement_get_block_by_number
        m_get_block_metadata.side_effect = replacement_get_block_metadata

        # Because we're just using indexes of a list, we can't actually ever return blocks[0]
        # But this shouldn't be a problem because IRL this uses hashes, not indexes.
        # get_blockheader_and_metadata(0) means get the latest block, which is #3
        result_header, result_metadata = self.gcnode.get_blockheader_and_metadata(0)
        self.assertEqual(result_header, blocks[-1].blockheader)
        self.assertEqual(result_metadata, block_metadata[b'3'])

        # get block 1 returns the second element of blocks[], which happens to be #1
        result_header, result_metadata = self.gcnode.get_blockheader_and_metadata(1)
        self.assertEqual(result_header, blocks[1].blockheader)
        self.assertEqual(result_metadata, block_metadata[b'1'])

        # get block 3 returns the fourth element of blocks[], which happens to be #3
        result_header, result_metadata = self.gcnode.get_blockheader_and_metadata(3)  # get block #3
        self.assertEqual(result_header, blocks[3].blockheader)
        self.assertEqual(result_metadata, block_metadata[b'3'])

        # If get_block_by_number() couldn't find the corresponding block, we should get a (None, None)
        m_get_block_by_number.side_effect = Mock(return_value=None)
        result_header, result_metadata = self.gcnode.get_blockheader_and_metadata(2)
        self.assertIsNone(result_header)
        self.assertIsNone(result_metadata)

    def test_submit_send_tx(self):
        # We verify that P2PFactory.add_unprocessed_txn() won't be called when:
        # TX is None OR
        # pending TXPool is full
        with self.assertRaises(ValueError):
            self.gcnode.submit_send_tx(None)

        self.chain_manager.tx_pool.is_full_pending_transaction_pool.return_value = True
        m_tx = Mock(name='mock Transaction')
        with self.assertRaises(ValueError):
            self.gcnode.submit_send_tx(m_tx)

        self.chain_manager.tx_pool.is_full_pending_transaction_pool.return_value = False
        self.gcnode._p2pfactory = Mock(name='mock P2PFactory')
        self.gcnode.submit_send_tx(m_tx)
        self.gcnode._p2pfactory.add_unprocessed_txn.assert_called_once()


@patch('gc.core.misc.ntp.getTime', new=replacement_getTime)
class TestgcNodeProperties(TestCase):
    @patch('gc.core.misc.ntp.getTime', new=replacement_getTime)
    def setUp(self):
        state = Mock()
        self.m_chain_manager = ChainManager(state=state)
        self.m_chain_manager._last_block = None
        self.m_chain_manager._state.get_block_by_number.return_value = None

        self.m_peer_manager = Mock(name='mock P2PPeerManager')

        self.gcnode = gcNode(mining_address=b'')
        self.gcnode.set_chain_manager(self.m_chain_manager)
        self.gcnode.peer_manager = self.m_peer_manager

    def test_state(self):
        # If gcnode._p2pfactory is None, then this should be this value
        self.assertEqual(self.gcnode.state, ESyncState.unknown.value)

        # Else, it should be whatever this part of p2pfactory says
        m_p2pfactory = Mock()
        m_p2pfactory.sync_state.state.value = "test"
        self.gcnode._p2pfactory = m_p2pfactory
        self.assertEqual(self.gcnode.state, "test")

    def test_num_connections(self):
        # If gcnode._p2pfactory is None, then this should return 0
        self.assertEqual(self.gcnode.num_connections, 0)

        # otherwise it should return what p2pfactory's num_connections says
        m_p2pfactory = Mock(num_connections=5)
        self.gcnode._p2pfactory = m_p2pfactory
        self.assertEqual(self.gcnode.num_connections, 5)

    def test_epoch(self):
        self.assertEqual(self.gcnode.epoch, 0)

        self.m_chain_manager._last_block = Mock(block_number=5)
        self.assertEqual(self.gcnode.epoch, (5 // config.dev.blocks_per_epoch))

        self.m_chain_manager._last_block = Mock(block_number=256)
        self.assertEqual(self.gcnode.epoch, (256 // config.dev.blocks_per_epoch))

    @patch('gc.core.Block.Block.get_block_by_number')
    def test_uptime_network(self, mock_get_block_by_number):
        # If there is no block after the genesis block, this property should return 0
        mock_get_block_by_number.return_value = None
        self.assertEqual(self.gcnode.uptime_network, 0)

        # However, if there is a block after the genesis block, use its timestamp to calculate our uptime.
        with patch('gc.core.misc.ntp.getTime') as m_getTime:
            mock_get_block_by_number.return_value = Mock(timestamp=1000000)
            m_getTime.return_value = 1500000
            self.assertEqual(self.gcnode.uptime_network, 500000)

    def test_block_last_reward(self):
        # If last_block() returned None, of course the last reward was 0.
        self.assertEqual(self.gcnode.block_last_reward, 0)

        # Else it is what the block_reward says it is.
        self.m_chain_manager._last_block = Mock(block_reward=53)
        self.assertEqual(self.gcnode.block_last_reward, 53)

    @patch('gc.core.ChainManager.ChainManager.get_measurement')
    @patch('gc.core.BlockMetadata.BlockMetadata.get_block_metadata')
    def test_block_time_mean(self, mock_get_block_metadata, mock_get_measurement):
        # FIXME
        # For this function to work, last_block() must not return a None. If it does, bad things will happen.
        self.m_chain_manager._last_block = Mock(name='mock Block')

        # If this particular function returns None, this property should just return the config value
        mock_get_block_metadata.return_value = None
        self.assertEqual(self.gcnode.block_time_mean, config.dev.block_timing_in_seconds)

        # Else, it should consult state.get_measurement()
        mock_get_block_metadata.return_value = Mock(name='mock BlockMetadata')
        self.gcnode.block_time_mean()
        mock_get_measurement.assert_called_once()

    def test_coin_supply(self):
        with mock._patch_object(ChainManager, 'total_coin_supply') as m_total_coin_supply:
            m_total_coin_supply.__get__ = Mock(return_value=100)
            self.assertEqual(100, self.gcnode.coin_supply)
            m_total_coin_supply.__get__.assert_called_once()

    def test_coin_supply_max(self):
        # This property should be whatever config says it is.
        self.assertEqual(self.gcnode.coin_supply_max, config.dev.max_coin_supply)

    def test_get_peers_stat(self):
        self.gcnode.get_peers_stat()
        self.m_peer_manager.get_peers_stat.assert_called_once()
