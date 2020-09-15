# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
from google.protobuf.json_format import MessageToJson, Parse

from pygclib.pygclib import bin2hstr
from gc.core import config
from gc.core.misc import logger
from gc.core.State import State
from gc.generated import gc_pb2


class BlockMetadata(object):

    def __init__(self, pbdata=None):
        self._data = pbdata
        if not pbdata:
            self._data = gc_pb2.BlockMetaData()
            self._data.block_difficulty = bytes([0] * 32)
            self._data.cumulative_difficulty = bytes([0] * 32)
        else:
            # TODO: Improve validation
            if len(self.cumulative_difficulty) != 32:
                raise ValueError("Invalid cumulative_difficulty")

            if len(self.block_difficulty) != 32:
                raise ValueError("Invalid block_difficulty")

    @property
    def pbdata(self):
        return self._data

    @property
    def block_difficulty(self):
        return tuple(self._data.block_difficulty)

    @property
    def cumulative_difficulty(self):
        return tuple(self._data.cumulative_difficulty)

    @property
    def child_headerhashes(self):
        return self._data.child_headerhashes

    @property
    def last_N_headerhashes(self):
        return self._data.last_N_headerhashes

    def set_block_difficulty(self, value):

        if len(value) != 32:
            raise ValueError("Invalid block_difficulty")

        self._data.block_difficulty = bytes(value)

    def set_cumulative_difficulty(self, value):
        if len(value) != 32:
            raise ValueError("Invalid cumulative_difficulty")
        self._data.cumulative_difficulty = bytes(value)

    def add_child_headerhash(self, child_headerhash: bytes):
        if child_headerhash not in self._data.child_headerhashes:
            self._data.child_headerhashes.append(child_headerhash)

    def update_last_headerhashes(self, parent_last_N_headerhashes, last_headerhash: bytes):
        del self._data.last_N_headerhashes[:]
        self._data.last_N_headerhashes.extend(parent_last_N_headerhashes)
        self._data.last_N_headerhashes.append(last_headerhash)
        if len(self._data.last_N_headerhashes) > config.dev.N_measurement:
            del self._data.last_N_headerhashes[0]

        if len(self._data.last_N_headerhashes) > config.dev.N_measurement:
            raise Exception('Size of last_N_headerhashes is more than expected %s %s',
                            len(self._data.last_N_headerhashes),
                            config.dev.N_measurement)

    @staticmethod
    def create(block_difficulty=bytes([0] * 32),
               cumulative_difficulty=bytes([0] * 32),
               child_headerhashes=None):
        block_meta_data = BlockMetadata()
        block_meta_data._data.block_difficulty = block_difficulty
        block_meta_data._data.cumulative_difficulty = cumulative_difficulty

        if child_headerhashes:
            for headerhash in child_headerhashes:
                block_meta_data._data.child_headerhashes.append(headerhash)

        return block_meta_data

    @staticmethod
    def from_json(json_data):
        pbdata = gc_pb2.BlockMetaData()
        Parse(json_data, pbdata)
        return BlockMetadata(pbdata)

    def to_json(self) -> str:
        return MessageToJson(self._data, sort_keys=True).encode()

    def serialize(self) -> str:
        return self._data.SerializeToString()

    @staticmethod
    def deserialize(data):
        pbdata = gc_pb2.BlockMetaData()
        pbdata.ParseFromString(bytes(data))
        return BlockMetadata(pbdata)

    @staticmethod
    def put_block_metadata(state: State, headerhash: bytes, block_metadata, batch):
        state._db.put_raw(b'metadata_' + headerhash, block_metadata.serialize(), batch)

    @staticmethod
    def get_block_metadata(state: State, header_hash: bytes):
        try:
            data = state._db.get_raw(b'metadata_' + header_hash)
            return BlockMetadata.deserialize(data)
        except KeyError:
            logger.debug('[get_block_metadata] Block header_hash %s not found',
                         b'metadata_' + bin2hstr(header_hash).encode())
        except Exception as e:
            logger.error('[get_block_metadata] %s', e)

        return None
