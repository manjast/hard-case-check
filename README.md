# Hard-case check

A reproducible record-matching experiment on DBLP-ACM and three product benchmarks. It compares two fixed similarity matchers with a learned matcher, reports uncertainty by title-similarity slice, and standardizes scores to different slice mixes. The [results](docs/results.md) report all outcomes and limitations; the [protocol](docs/protocol.md) records the original method and two amendments.

The learned matcher reaches F1 0.981 on DBLP-ACM and 0.667–0.771 on the product benchmarks. No original test split combines F1 at least 0.90 with a supported hard-recall gap; the highest-scoring dataset has only two hard positives. Reweighting Walmart-Amazon's fixed trigram matcher to DBLP-ACM's pair/positive mix raises F1 from 0.370 to 0.824 without changing predictions.

## Method registration and provenance

Methods were committed locally before their corresponding runs. Each registration commit was first pushed to GitHub together with its results. The history preserves the method versions and recorded sequence, but does not independently establish execution timing or provide external, pre-execution timestamped registration.

| Stage | Method commit | Corresponding results |
|---|---|---|
| Original DBLP-ACM protocol | [Original protocol](https://github.com/manjast/hard-case-check/commit/20a15ff160c11b2c31f80d7cb2e7a80ab53ac4ba) | [Initial results](https://github.com/manjast/hard-case-check/blob/31a6e60027911040210f06e1a90f7f90fe5aa56e/docs/results.md) |
| Amendment 1: product benchmarks | [Product extension](https://github.com/manjast/hard-case-check/commit/89897eac2567f8f9d636c72653d6974cc5891fb2) | [Product results](https://github.com/manjast/hard-case-check/blob/eb23d96c2094da3ce47aa1f442682e7cccf462f3/docs/results.md) |
| Amendment 2: learned matcher, intervals and case-mix analysis | [Second amendment](https://github.com/manjast/hard-case-check/commit/c3f57277ce79819abe9b3ef2216c13354a9168fe) | [Complete results](https://github.com/manjast/hard-case-check/blob/1b1f118de324d2ac4297168f7a78ea1759e9e92c/docs/results.md) |

Amendment 1 followed the finding of only two low-similarity matches in DBLP-ACM. Amendment 2 was written after the fixed rules' results were known; it introduced the explicit combined criterion alongside the new analyses. Earlier result files retain their original interpretations. The complete results report the unsupported combined criterion, every case-mix comparison and the comparisons marked not estimable. The code and results at `1b1f118de324d2ac4297168f7a78ea1759e9e92c` are unchanged by this provenance note.

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
