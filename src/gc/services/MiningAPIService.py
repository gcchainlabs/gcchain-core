# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
from grpc import StatusCode

from pygclib.pygclib import bin2hstr

from gc.core import config
from gc.core.gcnode import gcNode
from gc.crypto.Qryptonight import Qryptonight
from gc.generated import gcmining_pb2
from gc.generated.gcmining_pb2_grpc import MiningAPIServicer
from gc.services.grpcHelper import GrpcExceptionWrapper


class MiningAPIService(MiningAPIServicer):
    MAX_REQUEST_QUANTITY = 100

    def __init__(self, gcnode: gcNode):
        self.gcnode = gcnode
        self._qn = Qryptonight()

    @GrpcExceptionWrapper(gcmining_pb2.GetBlockMiningCompatibleResp, StatusCode.UNKNOWN)
    def GetBlockMiningCompatible(self,
                                 request: gcmining_pb2.GetBlockMiningCompatibleReq,
                                 context) -> gcmining_pb2.GetBlockMiningCompatibleResp:

        blockheader, block_metadata = self.gcnode.get_blockheader_and_metadata(request.height)

        response = gcmining_pb2.GetBlockMiningCompatibleResp()
        if blockheader is not None and block_metadata is not None:
            response = gcmining_pb2.GetBlockMiningCompatibleResp(
                blockheader=blockheader.pbdata,
                blockmetadata=block_metadata.pbdata)

        return response

    @GrpcExceptionWrapper(gcmining_pb2.GetLastBlockHeaderResp, StatusCode.UNKNOWN)
    def GetLastBlockHeader(self,
                           request: gcmining_pb2.GetLastBlockHeaderReq,
                           context) -> gcmining_pb2.GetLastBlockHeaderResp:
        response = gcmining_pb2.GetLastBlockHeaderResp()

        blockheader, block_metadata = self.gcnode.get_blockheader_and_metadata(request.height)

        response.difficulty = int(bin2hstr(block_metadata.block_difficulty), 16)
        response.height = blockheader.block_number
        response.timestamp = blockheader.timestamp
        response.reward = blockheader.block_reward + blockheader.fee_reward
        response.hash = bin2hstr(blockheader.headerhash)
        response.depth = self.gcnode.block_height - blockheader.block_number

        return response

    @GrpcExceptionWrapper(gcmining_pb2.GetBlockToMineResp, StatusCode.UNKNOWN)
    def GetBlockToMine(self,
                       request: gcmining_pb2.GetBlockToMineReq,
                       context) -> gcmining_pb2.GetBlockToMineResp:

        response = gcmining_pb2.GetBlockToMineResp()

        blocktemplate_blob_and_difficulty = self.gcnode.get_block_to_mine(request.wallet_address)

        if blocktemplate_blob_and_difficulty:
            response.blocktemplate_blob = blocktemplate_blob_and_difficulty[0]
            response.difficulty = blocktemplate_blob_and_difficulty[1]
            response.height = self.gcnode.block_height + 1
            response.reserved_offset = config.dev.extra_nonce_offset
            seed_block_number = self._qn.get_seed_height(response.height)
            response.seed_hash = bin2hstr(self.gcnode.get_block_header_hash_by_number(seed_block_number))

        return response

    @GrpcExceptionWrapper(gcmining_pb2.GetBlockToMineResp, StatusCode.UNKNOWN)
    def SubmitMinedBlock(self,
                         request: gcmining_pb2.SubmitMinedBlockReq,
                         context) -> gcmining_pb2.SubmitMinedBlockResp:
        response = gcmining_pb2.SubmitMinedBlockResp()

        response.error = not self.gcnode.submit_mined_block(request.blob)

        return response
