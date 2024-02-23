import argparse
import os
import pandas as pd
import numpy as np
import sys
import re


def validation_parameters(local_tsv, chrome_tsv):
    """
    Compare local classification to the one performed by Google Chrome on
    chrome://topics-internals
    """
    correct = []
    incorrect = []
    df_local = pd.read_csv(local_tsv, sep="\t")

    with open(chrome_tsv, "r") as f:
        beta = f.readlines()

    for line in beta:
        domain, labels = line.split("\t")
        ids_beta = [
            int(id[:-1]) for id in re.findall(r"\b\d+\.", labels)
        ]  # remove the dot from find all with -1
        if ids_beta == []:
            ids_beta = [-2]
        ids_model = np.array(df_local[df_local["domain"] == domain]["topic"])
        intersection = list(set(ids_model).intersection(ids_beta))
        if len(ids_beta) == len(intersection):
            correct.append(domain)
        else:
            incorrect.append(domain)
            print("Domain:", domain)
            print("Chrome internals:", ids_beta)
            print("Local:", ids_model)
    return correct, incorrect


if __name__ == "__main__":
    # Create Argument Parser
    parser = argparse.ArgumentParser(
        prog="python3 chrome_validation.py",
        description="Verify that local classification matches with Google Chrome's.",
    )
    parser.add_argument("local_tsv")
    parser.add_argument("chrome_tsv")
    args = parser.parse_args()

    local_tsv = args.local_tsv
    chrome_tsv = args.chrome_tsv

    if not (os.path.isfile(local_tsv)) or not (os.path.isfile(chrome_tsv)):
        raise Exception("Error: file(s) missing, check README.md")
    else:
        correct, incorrect = validation_parameters(local_tsv, chrome_tsv)

        print("Size of incorrect set: {}".format(len(incorrect)))
        print("Incorrect set: {}".format(incorrect))
