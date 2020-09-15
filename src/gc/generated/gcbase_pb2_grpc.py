# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import gc.generated.gcbase_pb2 as gcbase__pb2


class BaseStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetNodeInfo = channel.unary_unary(
        '/gc.Base/GetNodeInfo',
        request_serializer=gcbase__pb2.GetNodeInfoReq.SerializeToString,
        response_deserializer=gcbase__pb2.GetNodeInfoResp.FromString,
        )


class BaseServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def GetNodeInfo(self, request, context):
    # missing associated documentation comment in .proto file
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_BaseServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetNodeInfo': grpc.unary_unary_rpc_method_handler(
          servicer.GetNodeInfo,
          request_deserializer=gcbase__pb2.GetNodeInfoReq.FromString,
          response_serializer=gcbase__pb2.GetNodeInfoResp.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'gc.Base', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
