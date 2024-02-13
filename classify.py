import argparse
import json
import math
import pandas as pd
import re

from tflite_support.task import core
from tflite_support.task import text
from tensorflow_lite_support.python.task.processor.proto import classifications_pb2
from typing import List


class TopicsAPIClassifier:
    """
    Abstract Class to create a Topics API classifier for the Web or Android
    """

    def __init__(
        self, model_version: str, classification_type: str, output_human_readable: str
    ) -> None:
        self.model_version: str = model_version
        self.classification_type: str = classification_type
        self.output_human_readable: str = output_human_readable

        # load config.json
        with open(self.relative_path("/config.json"), "r") as f:
            self.config = json.load(f)

        # load taxonomy
        self.taxonomy = (
            pd.read_csv(
                self.relative_path(self.config["taxonomy_filename"]),
                sep="\t",
            )
            .set_index("ID")["Topic"]
            .to_dict()
        )
        # add to taxonomy dict the unknown topic
        self.taxonomy[self.config["unknown_topic_id"]] = self.config[
            "unknown_topic_name"
        ]

        # load model
        options = text.BertNLClassifierOptions(
            base_options=core.BaseOptions(
                file_name=self.relative_path(self.config["model_filename"])
            )
        )
        self.model = text.BertNLClassifier.create_from_options(options)

    def relative_path(self, filename: str) -> str:
        return self.model_version + "/" + filename

    def load_override_list(self, override_list_path: str) -> None:
        # Load manually curated list Android
        precomputed_list_df = pd.read_csv(override_list_path, sep="\t")
        self.override_list = dict()
        for _, row in precomputed_list_df.iterrows():
            topics = row[self.config["override_list_topics_column"]]
            # check if topics column is empty
            if type(topics) is not str and math.isnan(topics):
                self.override_list[row[self.config["override_list_input_column"]]] = []
            else:
                self.override_list[row[self.config["override_list_input_column"]]] = [
                    int(topic) for topic in topics.split(",")
                ]

    def print_output(self, input: str, topic_id: int) -> None:
        if self.output_human_readable:
            print(
                "{}\t{}".format(input, self.taxonomy[topic_id]) + "\n",
                end="",
            )
        else:
            print(
                "{}\t{}".format(input, topic_id) + "\n",
                end="",
            )


class ChromeTopicsAPIClassifier(TopicsAPIClassifier):
    """
    Topics API for the Web implemented in Google Chrome
    """

    def __init__(
        self, model_version: str, classification_type: str, output_human_readable: str
    ) -> None:
        super().__init__(model_version, classification_type, output_human_readable)

        # load override list
        override_list_path = self.relative_path(self.config["override_list_filename"])
        self.load_override_list(override_list_path)

    def clean_input(self, input: str) -> str:
        """
        Clean the domain input: prune meaningless prefixes and replace some
        characters with a space
        """
        # Grab regex from config files to remove meaningless prefixes  and also convert to lower case
        cleaned_input = re.sub(
            self.config["meaningless_prefix_regex"], "", input.lower()
        )
        # Replace following characters
        replace_chars = ["-", "_", ".", "+"]
        for rc in replace_chars:
            cleaned_input = cleaned_input.replace(rc, " ")
        return cleaned_input

    def topics_api_filtering(
        self, input: str, model_results: classifications_pb2.ClassificationResult
    ) -> None:
        """
        Perform the filtering applied by the Topics API to the classification
        results of the model.
        """
        # Order according to classification score, keep max ones only
        topics = sorted(
            model_results.classifications[0].categories,
            key=lambda x: x.score,
            reverse=True,
        )[0 : self.config["max_categories"]]
        top_sum = 0
        unknown_score = None
        # Sum scores, check if unknown topic in there
        for t in topics:
            top_sum += t.score
            if t.category_name == self.config["unknown_topic_id"]:
                unknown_score = t.score
        # if unknown topic there and too important, output unknown
        if unknown_score and unknown_score / top_sum > self.config["min_none_weight"]:
            self.print_output(input, int(t.category_name))
        else:
            # to keep track if a topic other than unknown passes the filtering
            other = False
            # go again through inferred topics, normalize scores, and check
            for t in topics:
                if (
                    t.category_name != -2
                    and t.score >= self.config["min_category_weight"]
                    and t.score / top_sum
                    >= self.config["min_normalized_weight_within_top_n"]
                ):
                    other = True
                    self.print_output(input, int(t.category_name))
            # we need to output unknown as no topic passes the filtering
            if not (other):
                self.print_output(input, self.config["unknown_topic_id"])

    def model_inference(self, input: str) -> classifications_pb2.ClassificationResult:
        """
        Perform model inference and return classification results
        """
        cleaned_input = self.clean_input(input)
        model_results = self.model.classify(cleaned_input)
        return model_results

    def one_inference(self, input: str) -> None:
        match self.classification_type:
            case "topics-api":
                cleaned_input = self.clean_input(input)
                if cleaned_input in self.override_list:
                    # input is in override list
                    topics = self.override_list[cleaned_input]
                    if topics == []:
                        # unknown topic
                        self.print_output(input, self.config["unknown_topic_id"])
                    else:
                        for t in topics:
                            self.print_output(input, t)
                else:
                    # input is not in override list
                    model_results = self.model_inference(input)
                    # apply filter and print
                    self.topics_api_filtering(input, model_results)

            case "model-only":
                model_results = self.model_inference(input)
                # apply filter and print
                self.topics_api_filtering(input, model_results)

            case "raw-model":
                model_results = self.model_inference(input)
                # print raw results
                line = "{}".format(input)
                topics = sorted(
                    model_results.classifications[0].categories,
                    key=lambda x: int(x.category_name),
                )
                for t in topics:
                    line += "\t{}".format(t.score)
                print(line + "\n", end="")

    def multiple_inferences(self, inputs: List[str]) -> None:
        for i in range(len(inputs)):
            self.one_inference(inputs[i])


class AndroidTopicsAPIClassifier(TopicsAPIClassifier):
    """
    Topics API for Android
    """

    def __init__(
        self, model_version: str, classification_type: str, output_human_readable: str
    ) -> None:
        super().__init__(model_version, classification_type, output_human_readable)

        # load override list
        override_list_path = self.relative_path(self.config["override_list_filename"])
        self.load_override_list(override_list_path)

    def clean_input_description(self, description: str) -> str:
        """
        From https://colab.research.google.com/github/privacysandbox/android-topics-classifier/blob/main/Android_TopicsAPI_Classifier_Execution_Demo.ipynb
        """
        # Avoid some special characters, such as emoji, crash the model.
        cleaned_description = description.encode("unicode_escape").decode("utf-8")
        # Converts to lower case.
        cleaned_description = cleaned_description.lower()
        # Removes urls.
        cleaned_description = re.sub(
            r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
            "",
            cleaned_description,
            flags=re.MULTILINE,
        )
        cleaned_description = re.sub(
            r"www.(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
            "",
            cleaned_description,
            flags=re.MULTILINE,
        )
        # Removes @mentions.
        cleaned_description = re.sub(r"@[A-Za-z0-9]+", "", cleaned_description)
        # Removes html tags.
        cleaned_description = re.sub("\\<.*?\\>", "", cleaned_description)
        # Removes new line and tab.
        cleaned_description = cleaned_description.replace("\n", " ").replace("\t", " ")
        # Removes multiple space.
        cleaned_description = re.sub(" +", " ", cleaned_description)

        return cleaned_description

    def topics_api_filtering(
        self, input: str, model_results: classifications_pb2.ClassificationResult
    ) -> None:
        """
        Perform the filtering applied by the Topics API to the classification
        results of the model.
        """
        topics = sorted(
            model_results.classifications[0].categories,
            key=lambda x: x.score,
            reverse=True,
        )[0 : self.config["max_categories"]]
        for t in topics:
            if t.score >= self.config["min_category_weight"]:
                self.print_output(input, int(t.category_name))

    def model_inference(
        self, description: str
    ) -> classifications_pb2.ClassificationResult:
        """
        Perform model inference and return classification results
        """
        cleaned_description = self.clean_input_description(description)
        # inference with description trimmed at model_max_characters_input
        model_results = self.model.classify(
            cleaned_description[: self.config["model_max_characters_input"]]
        )
        return model_results

    def one_inference(self, input: str, description: str) -> None:
        match self.classification_type:
            case "topics-api":
                if input in self.override_list:
                    # input is in override list
                    topics = self.override_list[input]
                    if topics == []:
                        # unknown topic
                        self.print_output(input, self.config["unknown_topic_id"])
                    else:
                        for t in topics:
                            self.print_output(input, t)
                else:
                    # input is not in override list
                    model_results = self.model_inference(description)
                    # apply filter and print
                    self.topics_api_filtering(input, model_results)

            case "model-only":
                model_results = self.model_inference(description)
                # apply filter and print
                self.topics_api_filtering(input, model_results)

            case "raw-model":
                model_results = self.model_inference(description)
                # print raw results
                line = "{}".format(input)
                topics = sorted(
                    model_results.classifications[0].categories,
                    key=lambda x: int(x.category_name),
                )
                for t in topics:
                    line += "\t{}".format(t.score)
                print(line + "\n", end="")

    def multiple_inferences(self, inputs: List[str], descriptions: List[str]) -> None:
        assert len(inputs) == len(descriptions)
        for i in range(len(inputs)):
            self.one_inference(inputs[i], descriptions[i])


if __name__ == "__main__":
    # Create Argument Parser
    parser = argparse.ArgumentParser(
        prog="python3 classify.py", description="Reimplementations of the Topics API"
    )
    req_grp = parser.add_argument_group(title="required optional arguments")
    req_grp.add_argument(
        "-mv",
        "--model_version",
        choices=["chrome1", "chrome4", "android1", "android2"],
        help="model version to use",
        required=True,
    )
    req_grp.add_argument(
        "-ct",
        "-classification_type",
        choices=["topics-api", "model-only", "raw-model"],
        help="type of classification: either run the full Topics classification (override+model+filtering), the model only (model+filtering), or get the raw classification by the model ",
        required=True,
    )
    req_grp.add_argument(
        "-i",
        "--inputs",
        nargs="+",
        help="input(s) to classify",
        required=True,
    )
    parser.add_argument(
        "-id",
        "--inputs_description",
        nargs="*",
        help="additional input description(s) (for android classification)",
    )
    parser.add_argument(
        "-ohr",
        "--output_human_readable",
        action="store_true",
        help="make output human readable, does not work with --classification-type raw-model",
    )
    args = parser.parse_args()

    chromeVersions = ["chrome1", "chrome4"]

    if args.output_human_readable and args.ct == "raw-model":
        raise Exception(
            "Output human readable is not available with raw-model classification"
        )

    if args.model_version in chromeVersions:
        topics_classifier = ChromeTopicsAPIClassifier(
            args.model_version, args.ct, args.output_human_readable
        )
        topics_classifier.multiple_inferences(args.inputs)
    else:
        topics_classifier = AndroidTopicsAPIClassifier(
            args.model_version, args.ct, args.output_human_readable
        )
        topics_classifier.multiple_inferences(args.inputs, args.inputs_description)
