#!/usr/bin/env bash
pushd . > /dev/null
cd $( dirname "${BASH_SOURCE[0]}" )
cd ..

python -m grpc_tools.protoc -I=gc/protos --python_out=gc/generated --grpc_python_out=gc/generated gc/protos/gc.proto
python -m grpc_tools.protoc -I=gc/protos/gc.proto -I=gc/protos --python_out=gc/generated --grpc_python_out=gc/generated gc/protos/gclegacy.proto
python -m grpc_tools.protoc -I=gc/protos --python_out=gc/generated --grpc_python_out=gc/generated gc/protos/gcbase.proto
python -m grpc_tools.protoc -I=gc/protos --python_out=gc/generated --grpc_python_out=gc/generated gc/protos/gcmining.proto

# Patch import problem in generated code
sed -i 's|import gc_pb2 as gc__pb2|import gc.generated.gc_pb2 as gc__pb2|g' gc/generated/gc_pb2_grpc.py
sed -i 's|import gc_pb2 as gc__pb2|import gc.generated.gc_pb2 as gc__pb2|g' gc/generated/gclegacy_pb2.py
sed -i 's|import gc_pb2 as gc__pb2|import gc.generated.gc_pb2 as gc__pb2|g' gc/generated/gcmining_pb2.py

sed -i 's|import gclegacy_pb2 as gclegacy__pb2|import gc.generated.gclegacy_pb2 as gclegacy__pb2|g' gc/generated/gclegacy_pb2_grpc.py
sed -i 's|import gcbase_pb2 as gcbase__pb2|import gc.generated.gcbase_pb2 as gcbase__pb2|g' gc/generated/gcbase_pb2_grpc.py
sed -i 's|import gcmining_pb2 as gcmining__pb2|import gc.generated.gcmining_pb2 as gcmining__pb2|g' gc/generated/gcmining_pb2_grpc.py

find gc/generated -name '*.py'|grep -v migrations|xargs autoflake --in-place

#docker run --rm \
#  -v $(pwd)/docs/proto:/out \
#  -v $(pwd)/gc/protos:/protos \
#  pseudomuto/protoc-gen-doc --doc_opt=markdown,proto.md
#
#docker run --rm \
#  -v $(pwd)/docs/proto:/out \
#  -v $(pwd)/gc/protos:/protos \
#  pseudomuto/protoc-gen-doc --doc_opt=html,index.html

popd > /dev/null
