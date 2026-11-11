# Hard-case check

A small, deterministic record-matching experiment on DBLP-ACM. Overall positive-class F1 can mask much lower recall on low-title-similarity pairs. The [results](docs/results.md) report the observed numbers and their limitations; the [protocol](docs/protocol.md) was committed before either matcher was run.

## Reproduce

Requires Python 3.10 or newer and [uv](https://docs.astral.sh/uv/). No third-party Python packages are required.

```sh
uv venv --python python3
.venv/bin/python download.py
.venv/bin/python evaluate.py
```

The downloader checks the archive's SHA-256; the evaluator checks it again. Both train-selected thresholds and the test tables are printed. The provided validation split is not used for selection or fitting.

## Data and licensing

The dataset is the [DeepMatcher structured DBLP-ACM experimental benchmark](https://github.com/anhaidgroup/deepmatcher/blob/master/Datasets.md#dblp-acm), derived from the [Leipzig entity-resolution benchmarks](https://dbs.uni-leipzig.de/en/research/projects/object_matching/fever/benchmark_datasets_for_entity_resolution). The downloaded archive is https://pages.cs.wisc.edu/~anhai/data1/deepmatcher_data/Structured/DBLP-ACM/dblp_acm_exp_data.zip (SHA-256 `a15b752ffc318a714690cf13286d31c2012f686525803ca803c392ceff4aa4f3`). A clear redistribution license for these data has not been established; the data are not included in this repository. The code's MIT license does not apply to the dataset; consult its providers for applicable terms.

Code: [MIT License](LICENSE).
