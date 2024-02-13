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
