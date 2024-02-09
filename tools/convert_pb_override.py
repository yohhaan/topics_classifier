import argparse
import pandas as pd
import page_topics_override_list_pb2

# Create Argument Parser
parser = argparse.ArgumentParser(
    prog="python3 convert_pb_override.py",
    description="Convert .pb override list to .tsv",
)
parser.add_argument("input_file", help="input file")
args = parser.parse_args()

# Load override list
override_list = page_topics_override_list_pb2.PageTopicsOverrideList()
with open(args.input_file, "rb") as f:
    override_list.ParseFromString(f.read())
print("domain\ttopics")
for entry in override_list.entries:
    line = "{}".format(entry.domain)
    first_topic = True
    for id in entry.topics.topic_ids:
        if first_topic:
            line += "\t{}".format(id)
            first_topic = False
        else:
            line += ",{}".format(id)
    print(line)
