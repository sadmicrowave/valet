python3 -m grpc_tools.protoc -I ./.grpc/.protos \
        --python_out=./.grpc/.grpc_generated \
        --grpc_python_out=./.grpc/.grpc_generated \
        ./.grpc/.protos/*.proto
        