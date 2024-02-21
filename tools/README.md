# tools

## Convert taxonomy to `.tsv`
- Markdown table: `python3 convert_md_taxonomy.py md_input tsv_output`
- HTML table: `./convert_html_taxonomy.sh html_input tsv_output`

## Convert override list to `.tsv`
- `./convert_pb_override.sh pb_gz_input tsv_output`

## Decoding `model-info.pb`
- `protoc --decode_raw < model-info.pb`
- Correlate fields with [this
  `.proto`](https://source.chromium.org/chromium/chromium/src/+/main:components/optimization_guide/proto/page_topics_model_metadata.proto)

## Chrome validation
To verify that we obtain the same result as the Google Chrome's implementation
of the Topics API:
- `./chrome_validation.sh` extract 1000 domains from crux in
  `chrome_validation.domains` and classify them with
  our implementation in `chrome_validation_chrome4.tsv`
- Classify the same 1000 domains with Google Chrome by visiting
  `chrome://topics-internals`, select the output: copy-paste the tab separated
  table in `chrome_validation_chrome_internals.tsv`
- Run `python3 chrome_validation.py chrome_validation_chrome4.tsv
  chrome_validation_chrome_internals.tsv` to validate the local classification
  with the one implemented in Chrome (incorrect and correct sets are returned,
  incorrect should be empty, but in practice it may not due to floating point encoding)


## Other
- Check for invalid characters in override list: `grep
  ".*[^[:alpha:][:space:][:digit:]^,].*"`
- Meaningless prefixes v2:
  ```json
  {
      "meaningless_prefix_regex": "^(www[0-9]*|web|ftp|wap|home|m|mobile|amp|w)\\.",
      "meaningless_prefix_version": 2
  }
  ```
