#!/bin/bash

override_pb_gz=$1
override_tsv=$2

override_pb=override.pb
proto_path=page_topics_override_list.proto
python_proto_path=page_topics_override_list_pb2.py
if [ ! -f $override_tsv ]
then
    # Fetch page_topics_override_list.proto
    wget -q -O $proto_path https://raw.githubusercontent.com/chromium/chromium/main/components/optimization_guide/proto/page_topics_override_list.proto
    protoc $proto_path --python_out=.
    # Decompress override.pb.gz
    gzip -cdk $override_pb_gz > $override_pb
    python3 convert_pb_override.py $override_pb > $override_tsv
    rm $proto_path $override_pb $python_proto_path
fi

