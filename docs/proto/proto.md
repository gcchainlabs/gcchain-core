# Protocol Documentation
<a name="top"/>

## Table of Contents

- [gc.proto](#gc.proto)
    - [AddressList](#gc.AddressList)
    - [AddressState](#gc.AddressState)
    - [Block](#gc.Block)
    - [BlockExtended](#gc.BlockExtended)
    - [BlockHeader](#gc.BlockHeader)
    - [BlockHeaderExtended](#gc.BlockHeaderExtended)
    - [BlockMetaData](#gc.BlockMetaData)
    - [BlockMetaDataList](#gc.BlockMetaDataList)
    - [EphemeralMessage](#gc.EphemeralMessage)
    - [GenesisBalance](#gc.GenesisBalance)
    - [GetAddressStateReq](#gc.GetAddressStateReq)
    - [GetAddressStateResp](#gc.GetAddressStateResp)
    - [GetBlockReq](#gc.GetBlockReq)
    - [GetBlockResp](#gc.GetBlockResp)
    - [GetKnownPeersReq](#gc.GetKnownPeersReq)
    - [GetKnownPeersResp](#gc.GetKnownPeersResp)
    - [GetLatestDataReq](#gc.GetLatestDataReq)
    - [GetLatestDataResp](#gc.GetLatestDataResp)
    - [GetLocalAddressesReq](#gc.GetLocalAddressesReq)
    - [GetLocalAddressesResp](#gc.GetLocalAddressesResp)
    - [GetNodeStateReq](#gc.GetNodeStateReq)
    - [GetNodeStateResp](#gc.GetNodeStateResp)
    - [GetObjectReq](#gc.GetObjectReq)
    - [GetObjectResp](#gc.GetObjectResp)
    - [GetStakersReq](#gc.GetStakersReq)
    - [GetStakersResp](#gc.GetStakersResp)
    - [GetStatsReq](#gc.GetStatsReq)
    - [GetStatsResp](#gc.GetStatsResp)
    - [GetWalletReq](#gc.GetWalletReq)
    - [GetWalletResp](#gc.GetWalletResp)
    - [LatticePublicKeyTxnReq](#gc.LatticePublicKeyTxnReq)
    - [MR](#gc.MR)
    - [MsgObject](#gc.MsgObject)
    - [NodeInfo](#gc.NodeInfo)
    - [Peer](#gc.Peer)
    - [PingReq](#gc.PingReq)
    - [PongResp](#gc.PongResp)
    - [PushTransactionReq](#gc.PushTransactionReq)
    - [PushTransactionResp](#gc.PushTransactionResp)
    - [StakeValidator](#gc.StakeValidator)
    - [StakeValidatorsList](#gc.StakeValidatorsList)
    - [StakeValidatorsTracker](#gc.StakeValidatorsTracker)
    - [StakeValidatorsTracker.ExpiryEntry](#gc.StakeValidatorsTracker.ExpiryEntry)
    - [StakeValidatorsTracker.FutureStakeAddressesEntry](#gc.StakeValidatorsTracker.FutureStakeAddressesEntry)
    - [StakeValidatorsTracker.FutureSvDictEntry](#gc.StakeValidatorsTracker.FutureSvDictEntry)
    - [StakeValidatorsTracker.SvDictEntry](#gc.StakeValidatorsTracker.SvDictEntry)
    - [StakerData](#gc.StakerData)
    - [StoredPeers](#gc.StoredPeers)
    - [Timestamp](#gc.Timestamp)
    - [Transaction](#gc.Transaction)
    - [Transaction.CoinBase](#gc.Transaction.CoinBase)
    - [Transaction.Destake](#gc.Transaction.Destake)
    - [Transaction.Duplicate](#gc.Transaction.Duplicate)
    - [Transaction.LatticePublicKey](#gc.Transaction.LatticePublicKey)
    - [Transaction.Stake](#gc.Transaction.Stake)
    - [Transaction.Transfer](#gc.Transaction.Transfer)
    - [Transaction.Vote](#gc.Transaction.Vote)
    - [TransactionCount](#gc.TransactionCount)
    - [TransactionCount.CountEntry](#gc.TransactionCount.CountEntry)
    - [TransactionExtended](#gc.TransactionExtended)
    - [TransferCoinsReq](#gc.TransferCoinsReq)
    - [TransferCoinsResp](#gc.TransferCoinsResp)
    - [Wallet](#gc.Wallet)
    - [WalletStore](#gc.WalletStore)

    - [GetLatestDataReq.Filter](#gc.GetLatestDataReq.Filter)
    - [GetStakersReq.Filter](#gc.GetStakersReq.Filter)
    - [NodeInfo.State](#gc.NodeInfo.State)
    - [Transaction.Type](#gc.Transaction.Type)


    - [AdminAPI](#gc.AdminAPI)
    - [P2PAPI](#gc.P2PAPI)
    - [PublicAPI](#gc.PublicAPI)


- [gcbase.proto](#gcbase.proto)
    - [GetNodeInfoReq](#gc.GetNodeInfoReq)
    - [GetNodeInfoResp](#gc.GetNodeInfoResp)



    - [Base](#gc.Base)


- [gclegacy.proto](#gclegacy.proto)
    - [BKData](#gc.BKData)
    - [FBData](#gc.FBData)
    - [LegacyMessage](#gc.LegacyMessage)
    - [MRData](#gc.MRData)
    - [NoData](#gc.NoData)
    - [PBData](#gc.PBData)
    - [PLData](#gc.PLData)
    - [PONGData](#gc.PONGData)
    - [SYNCData](#gc.SYNCData)
    - [VEData](#gc.VEData)

    - [LegacyMessage.FuncName](#gc.LegacyMessage.FuncName)




- [Scalar Value Types](#scalar-value-types)



<a name="gc.proto"/>
<p align="right"><a href="#top">Top</a></p>

## gc.proto



<a name="gc.AddressList"/>

### AddressList



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| addresses | [bytes](#bytes) | repeated |  |






<a name="gc.AddressState"/>

### AddressState



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| address | [bytes](#bytes) |  |  |
| balance | [uint64](#uint64) |  |  |
| nonce | [uint64](#uint64) |  | FIXME: Discuss. 32 or 64 bits? |
| pubhashes | [bytes](#bytes) | repeated |  |
| transaction_hashes | [bytes](#bytes) | repeated |  |






<a name="gc.Block"/>

### Block



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| header | [BlockHeader](#gc.BlockHeader) |  |  |
| transactions | [Transaction](#gc.Transaction) | repeated |  |
| dup_transactions | [Transaction](#gc.Transaction) | repeated | TODO: Review this |
| vote | [Transaction](#gc.Transaction) | repeated |  |
| genesis_balance | [GenesisBalance](#gc.GenesisBalance) | repeated | This is only applicable to genesis blocks |






<a name="gc.BlockExtended"/>

### BlockExtended



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| block | [Block](#gc.Block) |  |  |
| voted_weight | [uint64](#uint64) |  |  |
| total_stake_weight | [uint64](#uint64) |  |  |






<a name="gc.BlockHeader"/>

### BlockHeader



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| block_number | [uint64](#uint64) |  | Header |
| epoch | [uint64](#uint64) |  |  |
| timestamp | [Timestamp](#gc.Timestamp) |  | FIXME: Temporary |
| hash_header | [bytes](#bytes) |  |  |
| hash_header_prev | [bytes](#bytes) |  |  |
| reward_block | [uint64](#uint64) |  |  |
| reward_fee | [uint64](#uint64) |  |  |
| merkle_root | [bytes](#bytes) |  |  |
| hash_reveal | [bytes](#bytes) |  |  |
| stake_selector | [bytes](#bytes) |  |  |






<a name="gc.BlockHeaderExtended"/>

### BlockHeaderExtended



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| header | [BlockHeader](#gc.BlockHeader) |  |  |
| transaction_count | [TransactionCount](#gc.TransactionCount) |  |  |
| voted_weight | [uint64](#uint64) |  |  |
| total_stake_weight | [uint64](#uint64) |  |  |






<a name="gc.BlockMetaData"/>

### BlockMetaData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| block_number | [uint64](#uint64) |  |  |
| hash_header | [bytes](#bytes) |  |  |






<a name="gc.BlockMetaDataList"/>

### BlockMetaDataList



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| block_number_hashes | [BlockMetaData](#gc.BlockMetaData) | repeated |  |






<a name="gc.EphemeralMessage"/>

### EphemeralMessage



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [bytes](#bytes) |  |  |
| ttl | [uint64](#uint64) |  |  |
| data | [bytes](#bytes) |  | Encrypted String containing aes256_symkey, prf512_seed, xmss_address, signature |






<a name="gc.EphemeralMessage.Data"/>

### EphemeralMessage.Data



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| aes256_symkey | [bytes](#bytes) |  |  |
| prf512_seed | [bytes](#bytes) |  |  |
| xmss_address | [bytes](#bytes) |  |  |
| xmss_signature | [bytes](#bytes) |  |  |






<a name="gc.GenesisBalance"/>

### GenesisBalance



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| address | [string](#string) |  | Address is string only here to increase visibility |
| balance | [uint64](#uint64) |  |  |






<a name="gc.GetAddressStateReq"/>

### GetAddressStateReq



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| address | [bytes](#bytes) |  |  |






<a name="gc.GetAddressStateResp"/>

### GetAddressStateResp



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| state | [AddressState](#gc.AddressState) |  |  |






<a name="gc.GetBlockReq"/>

### GetBlockReq



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| index | [uint64](#uint64) |  | Indicates the index number in mainchain |
| after_hash | [bytes](#bytes) |  | request the node that comes after hash |






<a name="gc.GetBlockResp"/>

### GetBlockResp



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| node_info | [NodeInfo](#gc.NodeInfo) |  |  |
| block | [Block](#gc.Block) |  |  |






<a name="gc.GetKnownPeersReq"/>

### GetKnownPeersReq







<a name="gc.GetKnownPeersResp"/>

### GetKnownPeersResp



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| node_info | [NodeInfo](#gc.NodeInfo) |  |  |
| known_peers | [Peer](#gc.Peer) | repeated |  |






<a name="gc.GetLatestDataReq"/>

### GetLatestDataReq



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| filter | [GetLatestDataReq.Filter](#gc.GetLatestDataReq.Filter) |  |  |
| offset | [uint32](#uint32) |  | Offset in the result list (works backwards in this case) |
| quantity | [uint32](#uint32) |  | Number of items to retrive. Capped at 100 |






<a name="gc.GetLatestDataResp"/>

### GetLatestDataResp



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| blockheaders | [BlockHeaderExtended](#gc.BlockHeaderExtended) | repeated |  |
| transactions | [TransactionExtended](#gc.TransactionExtended) | repeated |  |
| transactions_unconfirmed | [TransactionExtended](#gc.TransactionExtended) | repeated |  |






<a name="gc.GetLocalAddressesReq"/>

### GetLocalAddressesReq







<a name="gc.GetLocalAddressesResp"/>

### GetLocalAddressesResp



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| addresses | [bytes](#bytes) | repeated |  |






<a name="gc.GetNodeStateReq"/>

### GetNodeStateReq







<a name="gc.GetNodeStateResp"/>

### GetNodeStateResp



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| info | [NodeInfo](#gc.NodeInfo) |  |  |






<a name="gc.GetObjectReq"/>

### GetObjectReq



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| query | [bytes](#bytes) |  |  |






<a name="gc.GetObjectResp"/>

### GetObjectResp



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| found | [bool](#bool) |  |  |
| address_state | [AddressState](#gc.AddressState) |  |  |
| transaction | [TransactionExtended](#gc.TransactionExtended) |  |  |
| block | [Block](#gc.Block) |  |  |






<a name="gc.GetStakersReq"/>

### GetStakersReq



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| filter | [GetStakersReq.Filter](#gc.GetStakersReq.Filter) |  | Indicates which group of stakers (current / next) |
| offset | [uint32](#uint32) |  | Offset in the staker list |
| quantity | [uint32](#uint32) |  | Number of stakers to retrive. Capped at 100 |






<a name="gc.GetStakersResp"/>

### GetStakersResp



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| stakers | [StakerData](#gc.StakerData) | repeated |  |






<a name="gc.GetStatsReq"/>

### GetStatsReq







<a name="gc.GetStatsResp"/>

### GetStatsResp



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| node_info | [NodeInfo](#gc.NodeInfo) |  |  |
| epoch | [uint64](#uint64) |  | Current epoch |
| uptime_network | [uint64](#uint64) |  | Indicates uptime in seconds |
| stakers_count | [uint64](#uint64) |  | Number of active stakers |
| block_last_reward | [uint64](#uint64) |  |  |
| block_time_mean | [uint64](#uint64) |  |  |
| block_time_sd | [uint64](#uint64) |  |  |
| coins_total_supply | [uint64](#uint64) |  |  |
| coins_emitted | [uint64](#uint64) |  |  |
| coins_atstake | [uint64](#uint64) |  |  |






<a name="gc.GetWalletReq"/>

### GetWalletReq



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| address | [bytes](#bytes) |  |  |






<a name="gc.GetWalletResp"/>

### GetWalletResp



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| wallet | [Wallet](#gc.Wallet) |  | FIXME: Encrypt |






<a name="gc.LatticePublicKeyTxnReq"/>

### LatticePublicKeyTxnReq



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| address_from | [bytes](#bytes) |  |  |
| kyber_pk | [bytes](#bytes) |  |  |
| dilithium_pk | [bytes](#bytes) |  |  |
| xmss_pk | [bytes](#bytes) |  |  |
| xmss_ots_index | [uint64](#uint64) |  |  |






<a name="gc.MR"/>

### MR
FIXME: This is legacy. Plan removal


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| hash | [bytes](#bytes) |  | FIXME: rename this to block_headerhash |
| type | [string](#string) |  | FIXME: type/string what is this |
| stake_selector | [bytes](#bytes) |  |  |
| block_number | [uint64](#uint64) |  |  |
| prev_headerhash | [bytes](#bytes) |  |  |
| reveal_hash | [bytes](#bytes) |  |  |






<a name="gc.MsgObject"/>

### MsgObject



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| ephemeral | [EphemeralMessage](#gc.EphemeralMessage) |  | Overlapping - objects used for 2-way exchanges P2PRequest request = 1; P2PResponse response = 2; |






<a name="gc.NodeInfo"/>

### NodeInfo



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| version | [string](#string) |  |  |
| state | [NodeInfo.State](#gc.NodeInfo.State) |  |  |
| num_connections | [uint32](#uint32) |  |  |
| num_known_peers | [uint32](#uint32) |  |  |
| uptime | [uint64](#uint64) |  | Uptime in seconds |
| block_height | [uint64](#uint64) |  |  |
| block_last_hash | [bytes](#bytes) |  |  |
| stake_enabled | [bool](#bool) |  |  |
| network_id | [string](#string) |  |  |






<a name="gc.Peer"/>

### Peer



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| ip | [string](#string) |  |  |






<a name="gc.PingReq"/>

### PingReq







<a name="gc.PongResp"/>

### PongResp







<a name="gc.PushTransactionReq"/>

### PushTransactionReq



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| transaction_signed | [Transaction](#gc.Transaction) |  |  |






<a name="gc.PushTransactionResp"/>

### PushTransactionResp



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| some_response | [string](#string) |  |  |






<a name="gc.StakeValidator"/>

### StakeValidator



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| address | [bytes](#bytes) |  |  |
| slave_public_key | [bytes](#bytes) |  |  |
| terminator_hash | [bytes](#bytes) |  |  |
| balance | [uint64](#uint64) |  |  |
| activation_blocknumber | [uint64](#uint64) |  |  |
| nonce | [uint64](#uint64) |  |  |
| is_banned | [bool](#bool) |  |  |
| is_active | [bool](#bool) |  |  |






<a name="gc.StakeValidatorsList"/>

### StakeValidatorsList



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| stake_validators | [StakeValidator](#gc.StakeValidator) | repeated |  |






<a name="gc.StakeValidatorsTracker"/>

### StakeValidatorsTracker



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| sv_dict | [StakeValidatorsTracker.SvDictEntry](#gc.StakeValidatorsTracker.SvDictEntry) | repeated |  |
| future_stake_addresses | [StakeValidatorsTracker.FutureStakeAddressesEntry](#gc.StakeValidatorsTracker.FutureStakeAddressesEntry) | repeated |  |
| expiry | [StakeValidatorsTracker.ExpiryEntry](#gc.StakeValidatorsTracker.ExpiryEntry) | repeated |  |
| future_sv_dict | [StakeValidatorsTracker.FutureSvDictEntry](#gc.StakeValidatorsTracker.FutureSvDictEntry) | repeated |  |
| total_stake_amount | [uint64](#uint64) |  |  |






<a name="gc.StakeValidatorsTracker.ExpiryEntry"/>

### StakeValidatorsTracker.ExpiryEntry



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| key | [uint64](#uint64) |  |  |
| value | [AddressList](#gc.AddressList) |  |  |






<a name="gc.StakeValidatorsTracker.FutureStakeAddressesEntry"/>

### StakeValidatorsTracker.FutureStakeAddressesEntry



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| key | [string](#string) |  |  |
| value | [StakeValidator](#gc.StakeValidator) |  |  |






<a name="gc.StakeValidatorsTracker.FutureSvDictEntry"/>

### StakeValidatorsTracker.FutureSvDictEntry



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| key | [uint64](#uint64) |  |  |
| value | [StakeValidatorsList](#gc.StakeValidatorsList) |  |  |






<a name="gc.StakeValidatorsTracker.SvDictEntry"/>

### StakeValidatorsTracker.SvDictEntry



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| key | [string](#string) |  |  |
| value | [StakeValidator](#gc.StakeValidator) |  |  |






<a name="gc.StakerData"/>

### StakerData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| address_state | [AddressState](#gc.AddressState) |  |  |
| terminator_hash | [bytes](#bytes) |  |  |






<a name="gc.StoredPeers"/>

### StoredPeers



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| peers | [Peer](#gc.Peer) | repeated |  |






<a name="gc.Timestamp"/>

### Timestamp
TODO: Avoid using timestamp until the github issue is fixed
import &#34;google/protobuf/timestamp.proto&#34;;


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| seconds | [int64](#int64) |  |  |
| nanos | [int32](#int32) |  |  |






<a name="gc.Transaction"/>

### Transaction



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| type | [Transaction.Type](#gc.Transaction.Type) |  |  |
| nonce | [uint64](#uint64) |  |  |
| addr_from | [bytes](#bytes) |  |  |
| public_key | [bytes](#bytes) |  |  |
| transaction_hash | [bytes](#bytes) |  |  |
| ots_key | [uint32](#uint32) |  |  |
| signature | [bytes](#bytes) |  |  |
| transfer | [Transaction.Transfer](#gc.Transaction.Transfer) |  |  |
| stake | [Transaction.Stake](#gc.Transaction.Stake) |  |  |
| coinbase | [Transaction.CoinBase](#gc.Transaction.CoinBase) |  |  |
| latticePK | [Transaction.LatticePublicKey](#gc.Transaction.LatticePublicKey) |  |  |
| duplicate | [Transaction.Duplicate](#gc.Transaction.Duplicate) |  |  |
| vote | [Transaction.Vote](#gc.Transaction.Vote) |  |  |






<a name="gc.Transaction.CoinBase"/>

### Transaction.CoinBase



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| addr_to | [bytes](#bytes) |  |  |
| amount | [uint64](#uint64) |  |  |






<a name="gc.Transaction.Destake"/>

### Transaction.Destake







<a name="gc.Transaction.Duplicate"/>

### Transaction.Duplicate



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| block_number | [uint64](#uint64) |  |  |
| prev_header_hash | [uint64](#uint64) |  |  |
| coinbase1_hhash | [bytes](#bytes) |  |  |
| coinbase2_hhash | [bytes](#bytes) |  |  |
| coinbase1 | [Transaction](#gc.Transaction) |  |  |
| coinbase2 | [Transaction](#gc.Transaction) |  |  |






<a name="gc.Transaction.LatticePublicKey"/>

### Transaction.LatticePublicKey



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| kyber_pk | [bytes](#bytes) |  |  |
| dilithium_pk | [bytes](#bytes) |  |  |






<a name="gc.Transaction.Stake"/>

### Transaction.Stake



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| activation_blocknumber | [uint64](#uint64) |  |  |
| slavePK | [bytes](#bytes) |  |  |
| hash | [bytes](#bytes) |  |  |






<a name="gc.Transaction.Transfer"/>

### Transaction.Transfer



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| addr_to | [bytes](#bytes) |  |  |
| amount | [uint64](#uint64) |  |  |
| fee | [uint64](#uint64) |  |  |






<a name="gc.Transaction.Vote"/>

### Transaction.Vote



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| block_number | [uint64](#uint64) |  |  |
| hash_header | [bytes](#bytes) |  |  |






<a name="gc.TransactionCount"/>

### TransactionCount



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| count | [TransactionCount.CountEntry](#gc.TransactionCount.CountEntry) | repeated |  |






<a name="gc.TransactionCount.CountEntry"/>

### TransactionCount.CountEntry



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| key | [uint32](#uint32) |  |  |
| value | [uint32](#uint32) |  |  |






<a name="gc.TransactionExtended"/>

### TransactionExtended



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| header | [BlockHeader](#gc.BlockHeader) |  |  |
| tx | [Transaction](#gc.Transaction) |  |  |






<a name="gc.TransferCoinsReq"/>

### TransferCoinsReq



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| address_from | [bytes](#bytes) |  | Transaction source address |
| address_to | [bytes](#bytes) |  | Transaction destination address |
| amount | [uint64](#uint64) |  | Amount. It should be expressed in Shor |
| fee | [uint64](#uint64) |  | Fee. It should be expressed in Shor |
| xmss_pk | [bytes](#bytes) |  | XMSS Public key |
| xmss_ots_index | [uint64](#uint64) |  | XMSS One time signature index |






<a name="gc.TransferCoinsResp"/>

### TransferCoinsResp



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| transaction_unsigned | [Transaction](#gc.Transaction) |  |  |






<a name="gc.Wallet"/>

### Wallet



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| address | [string](#string) |  | FIXME move to bytes |
| mnemonic | [string](#string) |  |  |
| xmss_index | [int32](#int32) |  |  |






<a name="gc.WalletStore"/>

### WalletStore



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| wallets | [Wallet](#gc.Wallet) | repeated |  |








<a name="gc.GetLatestDataReq.Filter"/>

### GetLatestDataReq.Filter


| Name | Number | Description |
| ---- | ------ | ----------- |
| ALL | 0 |  |
| BLOCKHEADERS | 1 |  |
| TRANSACTIONS | 2 |  |
| TRANSACTIONS_UNCONFIRMED | 3 |  |



<a name="gc.GetStakersReq.Filter"/>

### GetStakersReq.Filter


| Name | Number | Description |
| ---- | ------ | ----------- |
| CURRENT | 0 |  |
| NEXT | 1 |  |



<a name="gc.NodeInfo.State"/>

### NodeInfo.State


| Name | Number | Description |
| ---- | ------ | ----------- |
| UNKNOWN | 0 |  |
| UNSYNCED | 1 |  |
| SYNCING | 2 |  |
| SYNCED | 3 |  |
| FORKED | 4 |  |



<a name="gc.Transaction.Type"/>

### Transaction.Type


| Name | Number | Description |
| ---- | ------ | ----------- |
| UNKNOWN | 0 |  |
| TRANSFER | 1 |  |
| STAKE | 2 |  |
| DESTAKE | 3 |  |
| COINBASE | 4 |  |
| LATTICE | 5 |  |
| DUPLICATE | 6 |  |
| VOTE | 7 |  |







<a name="gc.AdminAPI"/>

### AdminAPI
This is a place holder for testing/instrumentation APIs

| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| GetLocalAddresses | [GetLocalAddressesReq](#gc.GetLocalAddressesReq) | [GetLocalAddressesResp](#gc.GetLocalAddressesReq) | FIXME: Use TLS and some signature scheme to validate the cli? At the moment, it will run locally |


<a name="gc.P2PAPI"/>

### P2PAPI
This service describes the P2P API

| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| GetNodeState | [GetNodeStateReq](#gc.GetNodeStateReq) | [GetNodeStateResp](#gc.GetNodeStateReq) |  |
| GetKnownPeers | [GetKnownPeersReq](#gc.GetKnownPeersReq) | [GetKnownPeersResp](#gc.GetKnownPeersReq) |  |
| GetBlock | [GetBlockReq](#gc.GetBlockReq) | [GetBlockResp](#gc.GetBlockReq) | rpc PublishBlock(PublishBlockReq) returns (PublishBlockResp); |
| ObjectExchange | [MsgObject](#gc.MsgObject) | [MsgObject](#gc.MsgObject) | A bidirectional streaming channel is used to avoid any firewalling/NAT issues. |


<a name="gc.PublicAPI"/>

### PublicAPI
This service describes the Public API used by clients (wallet/cli/etc)

| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| GetNodeState | [GetNodeStateReq](#gc.GetNodeStateReq) | [GetNodeStateResp](#gc.GetNodeStateReq) |  |
| GetKnownPeers | [GetKnownPeersReq](#gc.GetKnownPeersReq) | [GetKnownPeersResp](#gc.GetKnownPeersReq) |  |
| GetStats | [GetStatsReq](#gc.GetStatsReq) | [GetStatsResp](#gc.GetStatsReq) |  |
| GetAddressState | [GetAddressStateReq](#gc.GetAddressStateReq) | [GetAddressStateResp](#gc.GetAddressStateReq) |  |
| GetObject | [GetObjectReq](#gc.GetObjectReq) | [GetObjectResp](#gc.GetObjectReq) |  |
| GetLatestData | [GetLatestDataReq](#gc.GetLatestDataReq) | [GetLatestDataResp](#gc.GetLatestDataReq) |  |
| GetStakers | [GetStakersReq](#gc.GetStakersReq) | [GetStakersResp](#gc.GetStakersReq) |  |
| TransferCoins | [TransferCoinsReq](#gc.TransferCoinsReq) | [TransferCoinsResp](#gc.TransferCoinsReq) |  |
| PushTransaction | [PushTransactionReq](#gc.PushTransactionReq) | [PushTransactionResp](#gc.PushTransactionReq) |  |
| GetLatticePublicKeyTxn | [LatticePublicKeyTxnReq](#gc.LatticePublicKeyTxnReq) | [TransferCoinsResp](#gc.LatticePublicKeyTxnReq) |  |





<a name="gcbase.proto"/>
<p align="right"><a href="#top">Top</a></p>

## gcbase.proto



<a name="gc.GetNodeInfoReq"/>

### GetNodeInfoReq







<a name="gc.GetNodeInfoResp"/>

### GetNodeInfoResp



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| version | [string](#string) |  |  |
| grpcProto | [string](#string) |  |  |












<a name="gc.Base"/>

### Base


| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| GetNodeInfo | [GetNodeInfoReq](#gc.GetNodeInfoReq) | [GetNodeInfoResp](#gc.GetNodeInfoReq) |  |





<a name="gclegacy.proto"/>
<p align="right"><a href="#top">Top</a></p>

## gclegacy.proto



<a name="gc.BKData"/>

### BKData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| mrData | [MRData](#gc.MRData) |  |  |
| block | [Block](#gc.Block) |  |  |






<a name="gc.FBData"/>

### FBData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| index | [uint64](#uint64) |  |  |






<a name="gc.LegacyMessage"/>

### LegacyMessage
Adding old code to refactor while keeping things working


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| func_name | [LegacyMessage.FuncName](#gc.LegacyMessage.FuncName) |  |  |
| noData | [NoData](#gc.NoData) |  |  |
| veData | [VEData](#gc.VEData) |  |  |
| pongData | [PONGData](#gc.PONGData) |  |  |
| mrData | [MRData](#gc.MRData) |  |  |
| sfmData | [MRData](#gc.MRData) |  |  |
| bkData | [BKData](#gc.BKData) |  |  |
| fbData | [FBData](#gc.FBData) |  |  |
| pbData | [PBData](#gc.PBData) |  |  |
| pbbData | [PBData](#gc.PBData) |  |  |
| syncData | [SYNCData](#gc.SYNCData) |  |  |






<a name="gc.MRData"/>

### MRData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| hash | [bytes](#bytes) |  | FIXME: rename this to block_headerhash |
| type | [LegacyMessage.FuncName](#gc.LegacyMessage.FuncName) |  | FIXME: type/string what is this |
| stake_selector | [bytes](#bytes) |  |  |
| block_number | [uint64](#uint64) |  |  |
| prev_headerhash | [bytes](#bytes) |  |  |
| reveal_hash | [bytes](#bytes) |  |  |






<a name="gc.NoData"/>

### NoData







<a name="gc.PBData"/>

### PBData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| index | [uint64](#uint64) |  |  |
| block | [Block](#gc.Block) |  |  |






<a name="gc.PLData"/>

### PLData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| peer_ips | [string](#string) | repeated |  |






<a name="gc.PONGData"/>

### PONGData







<a name="gc.SYNCData"/>

### SYNCData







<a name="gc.VEData"/>

### VEData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| version | [string](#string) |  |  |
| genesis_prev_hash | [bytes](#bytes) |  |  |








<a name="gc.LegacyMessage.FuncName"/>

### LegacyMessage.FuncName


| Name | Number | Description |
| ---- | ------ | ----------- |
| VE | 0 | Version |
| PL | 1 | Peers List |
| PONG | 2 | Pong |
| MR | 3 | Message received |
| SFM | 4 | Send Full Message |
| BK | 5 | Block |
| FB | 6 | Fetch request for block |
| PB | 7 | Push Block |
| PBB | 8 | Push Block Buffer |
| ST | 9 | Stake Transaction |
| DST | 10 | Destake Transaction |
| DT | 11 | Duplicate Transaction |
| TX | 12 | Transfer Transaction |
| VT | 13 | Vote |
| SYNC | 14 | Add into synced list, if the node replies |










## Scalar Value Types

| .proto Type | Notes | C++ Type | Java Type | Python Type |
| ----------- | ----- | -------- | --------- | ----------- |
| <a name="double" /> double |  | double | double | float |
| <a name="float" /> float |  | float | float | float |
| <a name="int32" /> int32 | Uses variable-length encoding. Inefficient for encoding negative numbers – if your field is likely to have negative values, use sint32 instead. | int32 | int | int |
| <a name="int64" /> int64 | Uses variable-length encoding. Inefficient for encoding negative numbers – if your field is likely to have negative values, use sint64 instead. | int64 | long | int/long |
| <a name="uint32" /> uint32 | Uses variable-length encoding. | uint32 | int | int/long |
| <a name="uint64" /> uint64 | Uses variable-length encoding. | uint64 | long | int/long |
| <a name="sint32" /> sint32 | Uses variable-length encoding. Signed int value. These more efficiently encode negative numbers than regular int32s. | int32 | int | int |
| <a name="sint64" /> sint64 | Uses variable-length encoding. Signed int value. These more efficiently encode negative numbers than regular int64s. | int64 | long | int/long |
| <a name="fixed32" /> fixed32 | Always four bytes. More efficient than uint32 if values are often greater than 2^28. | uint32 | int | int |
| <a name="fixed64" /> fixed64 | Always eight bytes. More efficient than uint64 if values are often greater than 2^56. | uint64 | long | int/long |
| <a name="sfixed32" /> sfixed32 | Always four bytes. | int32 | int | int |
| <a name="sfixed64" /> sfixed64 | Always eight bytes. | int64 | long | int/long |
| <a name="bool" /> bool |  | bool | boolean | boolean |
| <a name="string" /> string | A string must always contain UTF-8 encoded or 7-bit ASCII text. | string | String | str/unicode |
| <a name="bytes" /> bytes | May contain any arbitrary sequence of bytes. | string | ByteString | str |

