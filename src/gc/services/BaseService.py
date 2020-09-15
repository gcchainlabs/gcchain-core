# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.

# FIXME: This is odd...
import sys

import os
from grpc._cython.cygrpc import StatusCode

from gc.core.gcnode import gcNode
from gc.generated.gcbase_pb2 import GetNodeInfoReq, GetNodeInfoResp
from gc.generated.gcbase_pb2_grpc import BaseServicer


class BaseService(BaseServicer):
    def __init__(self, gcnode: gcNode):
        self.gcnode = gcnode

    def GetNodeInfo(self, request: GetNodeInfoReq, context) -> GetNodeInfoResp:
        try:
            resp = GetNodeInfoResp()
            resp.version = self.gcnode.version

            pkgdir = os.path.dirname(sys.modules['gc'].__file__)
            grpcprotopath = os.path.join(pkgdir, "protos", "gc.proto")
            with open(grpcprotopath, 'r') as infile:
                resp.grpcProto = infile.read()

            return resp
        except Exception as e:
            context.set_code(StatusCode.unknown)
            context.set_details(e)
            return GetNodeInfoResp()
