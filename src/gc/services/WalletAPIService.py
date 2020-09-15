# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
from pygclib.pygclib import bin2hstr
from gc.generated import gcwallet_pb2
from gc.generated.gcwallet_pb2_grpc import WalletAPIServicer
from gc.services.grpcHelper import GrpcExceptionWrapper


class WalletAPIService(WalletAPIServicer):
    MAX_REQUEST_QUANTITY = 100

    # TODO: Separate the Service from the node model
    def __init__(self, walletd):
        self._walletd = walletd

    @GrpcExceptionWrapper(gcwallet_pb2.AddNewAddressResp)
    def AddNewAddress(self, request: gcwallet_pb2.AddNewAddressReq, context) -> gcwallet_pb2.AddNewAddressResp:
        resp = gcwallet_pb2.AddNewAddressResp()
        try:
            resp.address = self._walletd.add_new_address(request.height, request.hash_function.lower())
        except Exception as e:
            resp.code = 1
            resp.error = str(e)

        return resp

    @GrpcExceptionWrapper(gcwallet_pb2.AddNewAddressResp)
    def AddNewAddressWithSlaves(self, request: gcwallet_pb2.AddNewAddressWithSlavesReq, context) -> gcwallet_pb2.AddNewAddressResp:
        resp = gcwallet_pb2.AddNewAddressResp()
        try:
            resp.address = self._walletd.add_new_address_with_slaves(request.height,
                                                                     request.number_of_slaves,
                                                                     request.hash_function.lower())
        except Exception as e:
            resp.code = 1
            resp.error = str(e)

        return resp

    @GrpcExceptionWrapper(gcwallet_pb2.AddAddressFromSeedResp)
    def AddAddressFromSeed(self, request: gcwallet_pb2.AddAddressFromSeedReq, context) -> gcwallet_pb2.AddAddressFromSeedResp:
        resp = gcwallet_pb2.AddAddressFromSeedResp()
        try:
            resp.address = self._walletd.add_address_from_seed(seed=request.seed)
        except Exception as e:
            resp.code = 1
            resp.error = str(e)

        return resp

    @GrpcExceptionWrapper(gcwallet_pb2.ListAddressesResp)
    def ListAddresses(self, request: gcwallet_pb2.ListAddressesReq, context) -> gcwallet_pb2.ListAddressesResp:
        resp = gcwallet_pb2.ListAddressesResp()
        try:
            resp.addresses.extend(self._walletd.list_address())
        except Exception as e:
            resp.code = 1
            resp.error = str(e)

        return resp

    @GrpcExceptionWrapper(gcwallet_pb2.RemoveAddressResp)
    def RemoveAddress(self, request: gcwallet_pb2.RemoveAddressReq, context) -> gcwallet_pb2.RemoveAddressResp:
        resp = gcwallet_pb2.RemoveAddressResp()
        try:
            if not self._walletd.remove_address(request.address):
                resp.code = 1
                resp.error = "No such address found"
        except Exception as e:
            resp.code = 1
            resp.error = str(e)

        return resp

    @GrpcExceptionWrapper(gcwallet_pb2.ValidAddressResp)
    def IsValidAddress(self, request: gcwallet_pb2.ValidAddressReq, context) -> gcwallet_pb2.ValidAddressResp:
        resp = gcwallet_pb2.ValidAddressResp()
        try:
            if not self._walletd.validate_address(request.address):
                resp.code = 1
                resp.error = "Invalid gc Address"
                resp.valid = "False"
            else:
                resp.valid = "True"
        except Exception as e:
            resp.code = 1
            resp.error = str(e)

        return resp

    @GrpcExceptionWrapper(gcwallet_pb2.GetRecoverySeedsResp)
    def GetRecoverySeeds(self, request: gcwallet_pb2.GetRecoverySeedsReq, context) -> gcwallet_pb2.GetRecoverySeedsResp:
        resp = gcwallet_pb2.GetRecoverySeedsResp()
        try:
            resp.hexseed, resp.mnemonic = self._walletd.get_recovery_seeds(request.address)
        except Exception as e:
            resp.code = 1
            resp.error = str(e)

        return resp

    @GrpcExceptionWrapper(gcwallet_pb2.GetWalletInfoResp)
    def GetWalletInfo(self, request: gcwallet_pb2.GetWalletInfoReq, context) -> gcwallet_pb2.GetWalletInfoResp:
        resp = gcwallet_pb2.GetWalletInfoResp()
        try:
            resp.version, resp.address_count, resp.is_encrypted = self._walletd.get_wallet_info()
        except Exception as e:
            resp.code = 1
            resp.error = str(e)

        return resp

    @GrpcExceptionWrapper(gcwallet_pb2.RelayTxnResp)
    def RelayTransferTxn(self, request: gcwallet_pb2.RelayTransferTxnReq, context) -> gcwallet_pb2.RelayTxnResp:
        resp = gcwallet_pb2.RelayTxnResp()
        try:
            resp.tx.MergeFrom(self._walletd.relay_transfer_txn(request.addresses_to,
                                                               request.amounts,
                                                               request.fee,
                                                               request.master_address,
                                                               request.signer_address,
                                                               request.ots_index))
        except Exception as e:
            resp.code = 1
            resp.error = str(e)

        return resp

    @GrpcExceptionWrapper(gcwallet_pb2.RelayTxnResp)
    def RelayTransferTxnBySlave(self,
                                request: gcwallet_pb2.RelayTransferTxnBySlaveReq,
                                context) -> gcwallet_pb2.RelayTxnResp:
        resp = gcwallet_pb2.RelayTxnResp()
        try:
            resp.tx.MergeFrom(self._walletd.relay_transfer_txn_by_slave(request.addresses_to,
                                                                        request.amounts,
                                                                        request.fee,
                                                                        request.master_address))
        except Exception as e:
            resp.code = 1
            resp.error = str(e)

        return resp

    @GrpcExceptionWrapper(gcwallet_pb2.RelayTxnResp)
    def RelayMessageTxn(self, request: gcwallet_pb2.RelayMessageTxnReq, context) -> gcwallet_pb2.RelayTxnResp:
        resp = gcwallet_pb2.RelayTxnResp()
        try:
            resp.tx.MergeFrom(self._walletd.relay_message_txn(request.message,
                                                              request.fee,
                                                              request.master_address,
                                                              request.signer_address,
                                                              request.ots_index))
        except Exception as e:
            resp.code = 1
            resp.error = str(e)

        return resp

    @GrpcExceptionWrapper(gcwallet_pb2.RelayTxnResp)
    def RelayMessageTxnBySlave(self,
                               request: gcwallet_pb2.RelayMessageTxnBySlaveReq,
                               context) -> gcwallet_pb2.RelayTxnResp:
        resp = gcwallet_pb2.RelayTxnResp()
        try:
            resp.tx.MergeFrom(self._walletd.relay_message_txn_by_slave(request.message,
                                                                       request.fee,
                                                                       request.master_address))
        except Exception as e:
            resp.code = 1
            resp.error = str(e)

        return resp

    @GrpcExceptionWrapper(gcwallet_pb2.RelayTxnResp)
    def RelayTokenTxn(self, request: gcwallet_pb2.RelayTokenTxnReq, context) -> gcwallet_pb2.RelayTxnResp:
        resp = gcwallet_pb2.RelayTxnResp()
        try:
            resp.tx.MergeFrom(self._walletd.relay_token_txn(request.symbol,
                                                            request.name,
                                                            request.owner,
                                                            request.decimals,
                                                            request.addresses,
                                                            request.amounts,
                                                            request.fee,
                                                            request.master_address,
                                                            request.signer_address,
                                                            request.ots_index))
        except Exception as e:
            resp.code = 1
            resp.error = str(e)

        return resp

    @GrpcExceptionWrapper(gcwallet_pb2.RelayTxnResp)
    def RelayTokenTxnBySlave(self,
                             request: gcwallet_pb2.RelayTokenTxnBySlaveReq,
                             context) -> gcwallet_pb2.RelayTxnResp:
        resp = gcwallet_pb2.RelayTxnResp()
        try:
            resp.tx.MergeFrom(self._walletd.relay_token_txn_by_slave(request.symbol,
                                                                     request.name,
                                                                     request.owner,
                                                                     request.decimals,
                                                                     request.addresses,
                                                                     request.amounts,
                                                                     request.fee,
                                                                     request.master_address))
        except Exception as e:
            resp.code = 1
            resp.error = str(e)

        return resp

    @GrpcExceptionWrapper(gcwallet_pb2.RelayTxnResp)
    def RelayTransferTokenTxn(self, request: gcwallet_pb2.RelayTransferTokenTxnReq, context) -> gcwallet_pb2.RelayTxnResp:
        resp = gcwallet_pb2.RelayTxnResp()
        try:
            resp.tx.MergeFrom(self._walletd.relay_transfer_token_txn(request.addresses_to,
                                                                     request.amounts,
                                                                     request.token_txhash,
                                                                     request.fee,
                                                                     request.master_address,
                                                                     request.signer_address,
                                                                     request.ots_index))
        except Exception as e:
            resp.code = 1
            resp.error = str(e)

        return resp

    @GrpcExceptionWrapper(gcwallet_pb2.RelayTxnResp)
    def RelayTransferTokenTxnBySlave(self,
                                     request: gcwallet_pb2.RelayTransferTokenTxnBySlaveReq,
                                     context) -> gcwallet_pb2.RelayTxnResp:
        resp = gcwallet_pb2.RelayTxnResp()
        try:
            resp.tx.MergeFrom(self._walletd.relay_transfer_token_txn_by_slave(request.addresses_to,
                                                                              request.amounts,
                                                                              request.token_txhash,
                                                                              request.fee,
                                                                              request.master_address))
        except Exception as e:
            resp.code = 1
            resp.error = str(e)

        return resp

    @GrpcExceptionWrapper(gcwallet_pb2.RelayTxnResp)
    def RelaySlaveTxn(self, request: gcwallet_pb2.RelaySlaveTxnReq, context) -> gcwallet_pb2.RelayTxnResp:
        resp = gcwallet_pb2.RelayTxnResp()
        try:
            resp.tx.MergeFrom(self._walletd.relay_slave_txn(request.slave_pks,
                                                            request.access_types,
                                                            request.fee,
                                                            request.master_address,
                                                            request.signer_address,
                                                            request.ots_index))
        except Exception as e:
            resp.code = 1
            resp.error = str(e)

        return resp

    @GrpcExceptionWrapper(gcwallet_pb2.RelayTxnResp)
    def RelaySlaveTxnBySlave(self, request: gcwallet_pb2.RelaySlaveTxnBySlaveReq, context) -> gcwallet_pb2.RelayTxnResp:
        resp = gcwallet_pb2.RelayTxnResp()
        try:
            resp.tx.MergeFrom(self._walletd.relay_slave_txn_by_slave(request.slave_pks,
                                                                     request.access_types,
                                                                     request.fee,
                                                                     request.master_address))
        except Exception as e:
            resp.code = 1
            resp.error = str(e)

        return resp

    @GrpcExceptionWrapper(gcwallet_pb2.EncryptWalletResp)
    def EncryptWallet(self, request: gcwallet_pb2.EncryptWalletReq, context) -> gcwallet_pb2.EncryptWalletResp:
        resp = gcwallet_pb2.EncryptWalletResp()
        try:
            self._walletd.encrypt_wallet(request.passphrase)
        except Exception as e:
            resp.code = 1
            resp.error = str(e)

        return resp

    @GrpcExceptionWrapper(gcwallet_pb2.LockWalletResp)
    def LockWallet(self, request: gcwallet_pb2.LockWalletReq, context) -> gcwallet_pb2.LockWalletResp:
        resp = gcwallet_pb2.LockWalletResp()
        try:
            self._walletd.lock_wallet()
        except Exception as e:
            resp.code = 1
            resp.error = str(e)

        return resp

    @GrpcExceptionWrapper(gcwallet_pb2.UnlockWalletResp)
    def UnlockWallet(self, request: gcwallet_pb2.UnlockWalletReq, context) -> gcwallet_pb2.UnlockWalletResp:
        resp = gcwallet_pb2.UnlockWalletResp()
        try:
            self._walletd.unlock_wallet(request.passphrase)
        except Exception as e:
            resp.code = 1
            resp.error = str(e)

        return resp

    @GrpcExceptionWrapper(gcwallet_pb2.ChangePassphraseResp)
    def ChangePassphrase(self,
                         request: gcwallet_pb2.ChangePassphraseReq,
                         context) -> gcwallet_pb2.ChangePassphraseResp:
        resp = gcwallet_pb2.ChangePassphraseResp()
        try:
            self._walletd.change_passphrase(request.oldPassphrase, request.newPassphrase)
        except Exception as e:
            resp.code = 1
            resp.error = str(e)

        return resp

    @GrpcExceptionWrapper(gcwallet_pb2.TransactionsByAddressResp)
    def GetTransactionsByAddress(self,
                                 request: gcwallet_pb2.TransactionsByAddressReq,
                                 context) -> gcwallet_pb2.TransactionsByAddressResp:
        resp = gcwallet_pb2.TransactionsByAddressResp()
        try:
            mini_transactions, balance = self._walletd.get_mini_transactions_by_address(qaddress=request.address,
                                                                                        item_per_page=1000000,
                                                                                        page_number=1)
            resp.mini_transactions.extend(mini_transactions)
            resp.balance = balance
        except Exception as e:
            resp.code = 1
            resp.error = str(e)

        return resp

    @GrpcExceptionWrapper(gcwallet_pb2.TransactionResp)
    def GetTransaction(self, request: gcwallet_pb2.TransactionReq, context) -> gcwallet_pb2.TransactionResp:
        resp = gcwallet_pb2.TransactionResp()
        try:
            tx, confirmations, block_number, block_header_hash = self._walletd.get_transaction(request.tx_hash)
            resp.tx.MergeFrom(tx)
            resp.confirmations = confirmations
            resp.block_number = block_number
            if block_header_hash:
                resp.block_header_hash = block_header_hash
        except Exception as e:
            resp.code = 1
            resp.error = str(e)

        return resp

    @GrpcExceptionWrapper(gcwallet_pb2.BalanceResp)
    def GetBalance(self, request: gcwallet_pb2.BalanceReq, context) -> gcwallet_pb2.BalanceResp:
        resp = gcwallet_pb2.BalanceResp()
        try:
            resp.balance = str(self._walletd.get_balance(request.address))
        except Exception as e:
            resp.code = 1
            resp.error = str(e)

        return resp

    @GrpcExceptionWrapper(gcwallet_pb2.TotalBalanceResp)
    def GetTotalBalance(self, request: gcwallet_pb2.TotalBalanceReq, context) -> gcwallet_pb2.TotalBalanceResp:
        resp = gcwallet_pb2.TotalBalanceResp()
        try:
            resp.balance = str(self._walletd.get_total_balance())
        except Exception as e:
            resp.code = 1
            resp.error = str(e)

        return resp

    @GrpcExceptionWrapper(gcwallet_pb2.OTSResp)
    def GetOTS(self, request: gcwallet_pb2.OTSReq, context) -> gcwallet_pb2.OTSResp:
        try:
            ots_bitfield_by_page, next_unused_ots_index, unused_ots_index_found = self._walletd.get_ots(request.address)
            resp = gcwallet_pb2.OTSResp(ots_bitfield_by_page=ots_bitfield_by_page,
                                         next_unused_ots_index=next_unused_ots_index,
                                         unused_ots_index_found=unused_ots_index_found)
        except Exception as e:
            resp.code = 1
            resp.error = str(e)

        return resp

    @GrpcExceptionWrapper(gcwallet_pb2.HeightResp)
    def GetHeight(self, request: gcwallet_pb2.HeightReq, context) -> gcwallet_pb2.HeightResp:
        resp = gcwallet_pb2.HeightResp()
        try:
            resp.height = self._walletd.get_height()
        except Exception as e:
            resp.code = 1
            resp.error = str(e)

        return resp

    @GrpcExceptionWrapper(gcwallet_pb2.BlockResp)
    def GetBlock(self, request: gcwallet_pb2.BlockReq, context) -> gcwallet_pb2.BlockResp:
        resp = gcwallet_pb2.BlockResp()
        try:
            resp.block.MergeFrom(self._walletd.get_block(request.header_hash))
        except Exception as e:
            resp.code = 1
            resp.error = str(e)

        return resp

    @GrpcExceptionWrapper(gcwallet_pb2.BlockResp)
    def GetBlockByNumber(self, request: gcwallet_pb2.BlockByNumberReq, context) -> gcwallet_pb2.BlockResp:
        resp = gcwallet_pb2.BlockResp()
        try:
            resp.block.MergeFrom(self._walletd.get_block_by_number(request.block_number))
        except Exception as e:
            resp.code = 1
            resp.error = str(e)

        return resp

    @GrpcExceptionWrapper(gcwallet_pb2.AddressFromPKResp)
    def GetAddressFromPK(self, request: gcwallet_pb2.AddressFromPKReq, context) -> gcwallet_pb2.AddressFromPKResp:
        resp = gcwallet_pb2.AddressFromPKResp()
        try:
            resp.address = self._walletd.get_address_from_pk(request.pk)
        except Exception as e:
            resp.code = 1
            resp.error = str(e)

        return resp

    @GrpcExceptionWrapper(gcwallet_pb2.NodeInfoResp)
    def GetNodeInfo(self, request: gcwallet_pb2.NodeInfoReq, context) -> gcwallet_pb2.NodeInfoResp:
        resp = gcwallet_pb2.NodeInfoResp()
        try:
            node_info = self._walletd.get_node_info()

            resp.version = node_info.info.version
            resp.num_connections = str(node_info.info.num_connections)
            resp.num_known_peers = str(node_info.info.num_known_peers)
            resp.uptime = node_info.info.uptime
            resp.block_height = node_info.info.block_height
            resp.block_last_hash = bin2hstr(node_info.info.block_last_hash)
            resp.network_id = node_info.info.network_id
        except Exception as e:
            resp.code = 1
            resp.error = str(e)

        return resp
