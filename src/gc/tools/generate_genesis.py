# coding=utf-8
from __future__ import print_function
import simplejson as json
import yaml
import sys

from pygclib.pygclib import hstr2bin

from gc.generated import gc_pb2
from gc.core import config
from gc.core.txs.TransferTransaction import TransferTransaction
from gc.core.Block import Block
from gc.crypto.xmss import XMSS


def create_tx(addrs_to, amounts, signing_xmss, nonce):
    tx = TransferTransaction.create(addrs_to=addrs_to,
                                    amounts=amounts,
                                    message_data=None,
                                    fee=0,
                                    xmss_pk=signing_xmss.pk)
    tx.sign(signing_xmss)
    tx._data.nonce = nonce
    return tx


def get_migration_transactions(signing_xmss, filename):
    transactions = []

    with open(filename, 'r') as f:
        json_data = json.load(f)

    count = 1
    addrs_to = []
    amounts = []
    output_limit = config.dev.transaction_multi_output_limit

    for addr in json_data:
        try:
            addrs_to.append(bytes(hstr2bin(addr[1:])))
        except:  # noqa
            print("Invalid Address ", addr)
            raise Exception
        amounts.append(json_data[addr])

        count += 1
        if count % output_limit == 0:
            transactions.append(create_tx(addrs_to, amounts, signing_xmss, count // output_limit))

            addrs_to = []
            amounts = []

    if addrs_to:
        transactions.append(create_tx(addrs_to, amounts, signing_xmss, (count // output_limit) + 1))

    return transactions


def main():
    if len(sys.argv) > 2:
        print("Unexpected arguments")
        sys.exit(0)
    elif len(sys.argv) == 1:
        print("Missing Filename")
        sys.exit(0)

    filename = sys.argv[1]

    if sys.version_info.major > 2:
        seed = bytes(hstr2bin(input('Enter extended hexseed: ')))
    else:
        seed = bytes(hstr2bin(raw_input('Enter extended hexseed: ')))  # noqa

    dist_xmss = XMSS.from_extended_seed(seed)

    transactions = get_migration_transactions(signing_xmss=dist_xmss, filename=filename)

    block = Block.create(dev_config=config.dev,
                         block_number=0,
                         prev_headerhash=config.user.genesis_prev_headerhash,
                         prev_timestamp=config.user.genesis_timestamp,
                         transactions=transactions,
                         miner_address=dist_xmss.address,
                         seed_height=None,
                         seed_hash=None)

    block.set_nonces(config.dev, 0, 0)

    block._data.genesis_balance.extend([gc_pb2.GenesisBalance(address=config.dev.coinbase_address,
                                                               balance=105000000000000000)])

    with open('genesis.yml', 'w') as f:
        yaml.dump(json.loads(block.to_json()), f)


if __name__ == '__main__':
    main()
