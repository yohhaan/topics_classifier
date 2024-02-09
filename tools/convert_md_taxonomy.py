import argparse
import pandas as pd

# Create Argument Parser
parser = argparse.ArgumentParser(
    prog="python3 convert_md_taxonomy.py", description="Convert Markdown Table to .tsv"
)
parser.add_argument("input_file", help="input file")
parser.add_argument("output_file", help="output file")
args = parser.parse_args()

ids = []
topics = []
with open(args.input_file, "r") as taxo:
    # skip header and 2nd line ----
    next(taxo)
    next(taxo)
    for line in taxo:
        # split id and topic
        _, id, topic, _ = line.split("|")
        # sanitizing and append
        ids.append(int(id.strip()))
        topics.append(topic.strip())
# save to disk dict as .csv
pd.DataFrame({"ID": ids, "Topic": topics}).to_csv(
    str(args.output_file), index=False, sep="\t"
)
