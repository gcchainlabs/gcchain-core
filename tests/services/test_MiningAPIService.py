# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
from unittest import TestCase

from mock import Mock, MagicMock, patch

from gc.core.Block import Block
from gc.core.BlockHeader import BlockHeader
from gc.core.BlockMetadata import BlockMetadata
from gc.core.ChainManager import ChainManager
from gc.core import config
from gc.core.misc import logger
from gc.core.node import SyncState
from gc.core.p2p.p2pfactory import P2PFactory
from gc.core.gcnode import gcNode
from gc.crypto.misc import sha256
from gc.generated import gcmining_pb2
from gc.services.MiningAPIService import MiningAPIService
from tests.misc.helper import replacement_getTime

logger.initialize_default()


@patch('gc.core.misc.ntp.getTime', new=replacement_getTime)
class TestMiningAPI(TestCase):
    def setUp(self):
        p2p_factory = Mock(spec=P2PFactory)
        p2p_factory.sync_state = SyncState()
        p2p_factory.num_connections = 23
        p2p_factory.pow = Mock()
        b = Block()
        self.chain_manager = Mock(spec=ChainManager)
        self.chain_manager.height = 0
        self.chain_manager.get_last_block = MagicMock(return_value=b)
        self.chain_manager.get_block_header_hash_by_number = MagicMock(return_value=b.headerhash)

        self.gcnode = gcNode(mining_address=b'')
        self.gcnode.set_chain_manager(self.chain_manager)
        self.gcnode._p2pfactory = p2p_factory
        self.gcnode._pow = p2p_factory.pow

        self.block_header_params = {
            "dev_config": config.dev,
            "blocknumber": 10,
            "prev_headerhash": sha256(b'prevblock'),
            "prev_timestamp": 1234567890,
            "hashedtransactions": sha256(b'tx1'),
            "fee_reward": 1,
            "seed_height": 0,
            "seed_hash": None,
        }

        self.service = MiningAPIService(self.gcnode)

    def test_GetBlockMiningCompatible(self):
        block_header = BlockHeader.create(**self.block_header_params)
        self.gcnode.get_blockheader_and_metadata = MagicMock(return_value=[block_header, BlockMetadata()])

        req = gcmining_pb2.GetBlockMiningCompatibleReq(height=10)
        answer = self.service.GetBlockMiningCompatible(request=req, context=None)

        self.assertEqual(10, answer.blockheader.block_number)
        self.assertEqual(1, answer.blockheader.reward_fee)

        # if gcNode responds with None, None, the GRPC response should be blank too
        self.gcnode.get_blockheader_and_metadata = MagicMock(return_value=[None, None])
        answer = self.service.GetBlockMiningCompatible(request=req, context=None)
        self.assertEqual(0, answer.blockheader.block_number)
        self.assertEqual(0, answer.blockheader.reward_fee)

    def test_GetLastBlockHeader(self):
        self.block_header_params["blocknumber"] = 20
        block_header = BlockHeader.create(**self.block_header_params)
        self.chain_manager.height = 200
        self.gcnode.get_blockheader_and_metadata = MagicMock(return_value=[block_header, BlockMetadata()])

        req = gcmining_pb2.GetLastBlockHeaderReq(height=20)
        answer = self.service.GetLastBlockHeader(request=req, context=None)

        self.assertEqual(180, answer.depth)
        self.assertEqual(20, answer.height)

    def test_GetBlockToMine(self):
        blocktemplate_blob = b'blob'
        difficulty = 100
        self.gcnode.get_block_to_mine = MagicMock(return_value=(blocktemplate_blob, difficulty))

        req = gcmining_pb2.GetBlockToMineReq(wallet_address=b'fake address')
        answer = self.service.GetBlockToMine(request=req, context=None)

        self.assertEqual(answer.height, 1)
        self.assertEqual(answer.reserved_offset, config.dev.extra_nonce_offset)

        # What happens if gcNode could not generate a blocktemplate? Then the response should be blank.
        self.gcnode.get_block_to_mine.return_value = None
        answer = self.service.GetBlockToMine(request=req, context=None)
        self.assertEqual('', answer.blocktemplate_blob)
        self.assertEqual(0, answer.height)
        self.assertEqual(0, answer.reserved_offset)
        self.assertEqual(0, answer.difficulty)

    def test_SubmitMinedBlock(self):
        req = gcmining_pb2.SubmitMinedBlockReq(blob=b'minedblob')

        # Submit mined block encountered an error
        self.gcnode.submit_mined_block = MagicMock(return_value=False)
        answer = self.service.SubmitMinedBlock(req, context=None)
        self.assertTrue(answer.error)

        # This time it was successful
        self.gcnode.submit_mined_block = MagicMock(return_value=True)
        answer = self.service.SubmitMinedBlock(req, context=None)
        self.assertFalse(answer.error)
