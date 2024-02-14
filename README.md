# topics classifier

This repository reproduces Google's implementations of the Topics API [for the
Web](https://privacysandbox.com/proposals/topics/) and [for
Android](https://developer.android.com/design-for-safety/privacy-sandbox/topics).
This is mainly used in [my
research](https://yohan.beugin.org/posts/2024_02_topics_api_web_classifier.html) to study
the [privacy and utility guarantees](https://petsymposium.org/popets/2024/popets-2024-0004.php) of these proposals.

## Getting started

Clone this repository, then install the required dependencies. A Dockerfile is
provided under `.devcontainer/`, see
[here](https://gist.github.com/yohhaan/b492e165b77a84d9f8299038d21ae2c9) for
direct integration with VS code or for manual deployment instructions.

## Usage
```
usage: python3 classify.py [-h] -mv {chrome1,chrome4,android1,android2} -ct {topics-api,model-only,raw-model} -i INPUTS [INPUTS ...] [-id [INPUTS_DESCRIPTION ...]] [-ohr]

Reimplementations of the Topics API

options:
  -h, --help            show this help message and exit
  -id [INPUTS_DESCRIPTION ...], --inputs_description [INPUTS_DESCRIPTION ...]
                        additional input description(s) (for android classification)
  -ohr, --output_human_readable
                        make output human readable, does not work with --classification-type raw-model

required optional arguments:
  -mv {chrome1,chrome4,android1,android2}, --model_version {chrome1,chrome4,android1,android2}
                        model version to use
  -ct {topics-api,model-only,raw-model}, -classification_type {topics-api,model-only,raw-model}
                        type of classification: either run the full Topics classification (override+model+filtering), the model only (model+filtering), or get the raw classification by the model
  -i INPUTS [INPUTS ...], --inputs INPUTS [INPUTS ...]
                        input(s) to classify
```

## Supported versions

- [`chrome1`](chrome1/config.json)
    - Web model version: 1
    - Override list: 9 254 domains (about 10k)
    - Web taxonomy version: 1 (349 topics)

- [`chrome4`](chrome4/config.json)
    - Web model version: 4
    - Override list: 47 128 domains (about 50k) -> 625 domains are incorrectly
      formatted in the list shipped by Google, see [here](https://yohan.beugin.org/posts/2024_02_topics_api_web_classifier.html)
    - Web taxonomy version: 2 (469 topics)
    - Introduction of utility buckets: version 1

- [`android1`](android1/config.json)
    - Android model version: 1
    - Override list: 10 012 apps (about 10k)
    - Android taxonomy version: 1 (349 topics)

- [`android2`](android2/config.json)
    - Android model version: 2
    - Override list: 10 014 apps (about 10k)
    - Android taxonomy version: 2 (446 topics)

If a new model for the Topics API has been released and is not available here
yet, please let me know by contacting me or opening an issue.
