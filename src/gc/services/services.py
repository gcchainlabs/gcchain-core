# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
from concurrent.futures import ThreadPoolExecutor

import grpc

from gc.core import config
from gc.core.misc import logger
from gc.core.gcnode import gcNode
from gc.generated.gc_pb2_grpc import add_PublicAPIServicer_to_server, add_AdminAPIServicer_to_server
from gc.generated.gcmining_pb2_grpc import add_MiningAPIServicer_to_server
from gc.generated.gcbase_pb2_grpc import add_BaseServicer_to_server
from gc.generated.gcdebug_pb2_grpc import add_DebugAPIServicer_to_server
from gc.services.BaseService import BaseService
from gc.services.AdminAPIService import AdminAPIService
from gc.services.PublicAPIService import PublicAPIService
from gc.services.MiningAPIService import MiningAPIService
from gc.services.DebugAPIService import DebugAPIService


def start_services(node: gcNode):
    public_server = grpc.server(ThreadPoolExecutor(max_workers=config.user.public_api_threads),
                                maximum_concurrent_rpcs=config.user.public_api_max_concurrent_rpc)
    add_BaseServicer_to_server(BaseService(node), public_server)
    add_PublicAPIServicer_to_server(PublicAPIService(node), public_server)

    if config.user.public_api_enabled:
        public_server.add_insecure_port("{0}:{1}".format(config.user.public_api_host,
                                                         config.user.public_api_port))
        public_server.start()

        logger.info("grpc public service - started !")

    admin_server = grpc.server(ThreadPoolExecutor(max_workers=config.user.admin_api_threads),
                               maximum_concurrent_rpcs=config.user.admin_api_max_concurrent_rpc)
    add_AdminAPIServicer_to_server(AdminAPIService(node), admin_server)

    if config.user.admin_api_enabled:
        admin_server.add_insecure_port("{0}:{1}".format(config.user.admin_api_host,
                                                        config.user.admin_api_port))
        admin_server.start()

        logger.info("grpc admin service - started !")

    mining_server = grpc.server(ThreadPoolExecutor(max_workers=config.user.mining_api_threads),
                                maximum_concurrent_rpcs=config.user.mining_api_max_concurrent_rpc)
    add_MiningAPIServicer_to_server(MiningAPIService(node), mining_server)

    if config.user.mining_api_enabled:
        mining_server.add_insecure_port("{0}:{1}".format(config.user.mining_api_host,
                                                         config.user.mining_api_port))
        mining_server.start()

        logger.info("grpc mining service - started !")

    debug_server = grpc.server(ThreadPoolExecutor(max_workers=config.user.debug_api_threads),
                               maximum_concurrent_rpcs=config.user.debug_api_max_concurrent_rpc)
    add_DebugAPIServicer_to_server(DebugAPIService(node), debug_server)

    if config.user.debug_api_enabled:
        debug_server.add_insecure_port("{0}:{1}".format(config.user.debug_api_host,
                                                        config.user.debug_api_port))
        debug_server.start()

        logger.info("grpc debug service - started !")

    return admin_server, public_server, mining_server, debug_server
