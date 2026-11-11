# Hard-case check

A reproducible record-matching experiment on DBLP-ACM and three product benchmarks. It compares two fixed similarity matchers with a learned matcher, reports uncertainty by title-similarity slice, and standardizes scores to different slice mixes. The [results](docs/results.md) report all outcomes and limitations; each analysis was registered in the [protocol](docs/protocol.md) before its run.

The learned matcher reaches F1 0.981 on DBLP-ACM and 0.667–0.771 on the product benchmarks. No original test split combines F1 at least 0.90 with a supported hard-recall gap; the highest-scoring dataset has only two hard positives. Reweighting Walmart-Amazon's fixed trigram matcher to DBLP-ACM's pair/positive mix raises F1 from 0.370 to 0.824 without changing predictions.

## Reproduce

Requires Python 3.12 or newer and [uv](https://docs.astral.sh/uv/). The pinned NumPy/scikit-learn environment uses CPU only; native-library computation is limited to one thread.

```sh
uv venv --python python3
uv pip install --link-mode copy --python .venv/bin/python -r requirements.txt
.venv/bin/python download.py
.venv/bin/python evaluate.py
```

The downloader checks each archive's SHA-256; the evaluator checks it again. The two fixed matchers select thresholds on train. The learned gradient-boosted matcher fits on train and selects its threshold on validation, without refitting. Its title TF-IDF vocabulary and inverse document frequencies are fitted only on records referenced by train pairs, never the full record tables.

The evaluator prints all thresholds, features, package versions, 1,000-resample pair-bootstrap intervals for recall/F1, and confusion-count reweightings to each other dataset's pair/positive slice mix. Reweighting requires at least 20 source positives and 20 source negatives in every target-relevant slice; unsupported comparisons are reported as not estimable. These are candidate-pair benchmarks, not production traffic, and title similarity is only a difficulty proxy.

To run a subset, pass one or more names to each command: `dblp-acm`, `abt-buy`, `amazon-google`, or `walmart-amazon`. Reweighting then covers only the datasets included in that run.

## Data and licensing

The datasets are [DeepMatcher's](https://github.com/anhaidgroup/deepmatcher/blob/master/Datasets.md) structured DBLP-ACM, textual Abt-Buy, structured Amazon-Google, and structured Walmart-Amazon experimental benchmarks. The first three are derived from the [Leipzig entity-resolution benchmarks](https://dbs.uni-leipzig.de/en/research/projects/object_matching/fever/benchmark_datasets_for_entity_resolution). Source archive URLs and SHA-256 checksums are recorded in `download.py`. A clear redistribution license for these data has not been established; the data are not included in this repository. The code's MIT license does not apply to the datasets; consult their providers for applicable terms.

Code: [MIT License](LICENSE).
