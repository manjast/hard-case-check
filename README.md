# Hard-case check

A small, deterministic record-matching experiment on DBLP-ACM and three product benchmarks. Overall positive-class F1 can mask much lower recall on low-title-similarity pairs, although overall F1 also varies substantially across datasets. The [results](docs/results.md) report the observed numbers and their limitations; the [protocol](docs/protocol.md) and its extension were committed before the corresponding matcher runs.

## Reproduce

Requires Python 3.10 or newer and [uv](https://docs.astral.sh/uv/). No third-party Python packages are required.

```sh
uv venv --python python3
.venv/bin/python download.py
.venv/bin/python evaluate.py
```

The downloader checks each archive's SHA-256; the evaluator checks it again. Both train-selected thresholds and the test tables are printed. The provided validation splits are not used for selection or fitting. To run a subset, pass one or more names to each command: `dblp-acm`, `abt-buy`, `amazon-google`, or `walmart-amazon`.

## Data and licensing

The datasets are [DeepMatcher's](https://github.com/anhaidgroup/deepmatcher/blob/master/Datasets.md) structured DBLP-ACM, textual Abt-Buy, structured Amazon-Google, and structured Walmart-Amazon experimental benchmarks. The first three are derived from the [Leipzig entity-resolution benchmarks](https://dbs.uni-leipzig.de/en/research/projects/object_matching/fever/benchmark_datasets_for_entity_resolution). Source archive URLs and SHA-256 checksums are recorded in `download.py`. A clear redistribution license for these data has not been established; the data are not included in this repository. The code's MIT license does not apply to the datasets; consult their providers for applicable terms.

Code: [MIT License](LICENSE).
