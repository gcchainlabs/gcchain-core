# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
from gc.core import config
from gc.core.gcnode import gcNode
from gc.generated import gcdebug_pb2
from gc.generated.gcdebug_pb2_grpc import DebugAPIServicer
from gc.services.grpcHelper import GrpcExceptionWrapper


class DebugAPIService(DebugAPIServicer):
    MAX_REQUEST_QUANTITY = 100

    def __init__(self, gcnode: gcNode):
        self.gcnode = gcnode

    @GrpcExceptionWrapper(gcdebug_pb2.GetFullStateResp)
    def GetFullState(self, request: gcdebug_pb2.GetFullStateReq, context) -> gcdebug_pb2.GetFullStateResp:
        return gcdebug_pb2.GetFullStateResp(
            coinbase_state=self.gcnode.get_address_state(config.dev.coinbase_address).pbdata,
            addresses_state=self.gcnode.get_all_address_state()
        )
