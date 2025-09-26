# topics classifier

This repository reproduces Google's implementations of the Topics API [for the Web](https://privacysandbox.com/proposals/topics/) and [for Android](https://developer.android.com/design-for-safety/privacy-sandbox/topics).
This is mainly used in [my research](https://yohan.beugin.org/posts/2024_02_topics_api_web_classifier.html) to study the privacy and utility guarantees of these proposals: [PETS'24](https://petsymposium.org/popets/2024/popets-2024-0004.php) and [SecWeb'24](https://arxiv.org/abs/2403.19577).


## Instructions

Start by cloning this repository:
- `git clone git@github.com:yohhaan/topics_classifier.git` (SSH)
- `git clone https://github.com/yohhaan/topics_classifier.git` (HTTPS)

Then, follow either set of instructions (or install dependencies manually).
- The [`.devcontainer/`](.devcontainer/) directory contains the config for  integration with VS Code (see [guide here](https://github.com/PoPETS-AEC/examples-and-other-resources/blob/main/resources/vs-code-docker-integration.md)).

> <details><summary>Using the Docker image from the Container Registry</summary>
>
> This [GitHub workflow](.github/workflows/build-push-docker-image.yaml)
> automatically builds and pushes the Docker image to GitHub's Container Registry
> when the `Dockerfile` or the `requirements.txt` files are modified.
>
> 1. Pull the Docker image:
> ```bash
> docker pull ghcr.io/yohhaan/topics_classifier:main
> ```
> 2. Launch the Docker container, attach the current working directory (i.e.,
> run from the root of the cloned git repository) as a volume, set the context
> to be that volume, and provide an interactive bash terminal:
> ```bash
> docker run --rm -it -v ${PWD}:/workspaces/topics_classifier \
>     -w /workspaces/topics_classifier \
>     --entrypoint bash ghcr.io/yohhaan/topics_classifier:main
> ```
> 3. Execute the example script:
> ```bash
> ./test.sh
> ```
> </details>


> <details><summary>Using a locally built Docker image</summary>
>
> 1. Build the Docker image:
> ```bash
> docker build -t topics_classifier:main .
> ```
> 2. Launch the Docker container, attach the current working directory (i.e.,
> run from the root of the cloned git repository) as a volume, set the context
> to be that volume, and provide an interactive bash terminal:
> ```bash
> docker run --rm -it -v ${PWD}:/workspaces/topics_classifier \
>     -w /workspaces/topics_classifier \
>     --entrypoint bash topics_classifier:main
> ```
> 3. Execute the example script:
> ```bash
> ./test.sh
> ```
> </details>

## Usage
```
usage: python3 classify.py [-h] -mv {chrome1,chrome4,chrome5,android1,android2} -ct {topics-api,model-only,raw-model} -i INPUTS [INPUTS ...] [-id [INPUTS_DESCRIPTION ...]] [-ohr]

Reimplementations of the Topics API

options:
  -h, --help            show this help message and exit
  -id [INPUTS_DESCRIPTION ...], --inputs_description [INPUTS_DESCRIPTION ...]
                        additional input description(s) (for android classification)
  -ohr, --output_human_readable
                        make output human readable, does not work with --classification-type raw-model

required optional arguments:
  -mv {chrome1,chrome4,chrome5,android1,android2}, --model_version {chrome1,chrome4,chrome5,android1,android2}
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
    - Override list: 47 128 domains (about 50k) -> 625 domains are incorrectly formatted in the list shipped by Google, see [here](https://yohan.beugin.org/posts/2024_02_topics_api_web_classifier.html)
    - Web taxonomy version: 2 (469 topics)
    - Introduction of utility buckets: version 1

- [`chrome5`](chrome5/config.json)
    - Web model version: 5
    - Override list: 45 270 domains (about 45k)
    - Web taxonomy version: 2 (469 topics)
    - Utility buckets version: 1
    - Note: only change with `chrome4` is the modification of the override list, see [here](https://issues.chromium.org/issues/325123734)

- [`android1`](android1/config.json)
    - Android model version: 1
    - Override list: 10 012 apps (about 10k)
    - Android taxonomy version: 1 (349 topics)

- [`android2`](android2/config.json)
    - Android model version: 2
    - Override list: 10 014 apps (about 10k)
    - Android taxonomy version: 2 (446 topics)

If a new model for the Topics API has been released and is not available here yet, please let me know by contacting me or opening an issue.
