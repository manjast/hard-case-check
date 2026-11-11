# Results

One evaluation of the supplied DBLP-ACM test split under the [preregistered protocol](protocol.md). Thresholds were selected on train, not test. Metrics are positive-class metrics; zero denominators are reported as zero. Values are rounded to three decimals.

## Title ratio baseline

Train-selected threshold: 0.87.

| Slice | Pairs | Positives | Positive rate | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|
| Overall | 2473 | 444 | 0.180 | 0.855 | 0.968 | 0.908 |
| Hard | 1430 | 2 | 0.001 | 0.000 | 0.000 | 0.000 |
| Middle | 534 | 10 | 0.019 | 0.000 | 0.000 | 0.000 |
| Easy | 509 | 432 | 0.849 | 0.855 | 0.995 | 0.920 |

## Title/author trigram Dice

Train-selected threshold: 0.84.

| Slice | Pairs | Positives | Positive rate | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|
| Overall | 2473 | 444 | 0.180 | 0.928 | 0.959 | 0.944 |
| Hard | 1430 | 2 | 0.001 | 0.000 | 0.000 | 0.000 |
| Middle | 534 | 10 | 0.019 | 0.667 | 0.200 | 0.308 |
| Easy | 509 | 432 | 0.849 | 0.930 | 0.981 | 0.955 |

The trigram matcher has overall F1 0.944, but misses both hard-slice positives and eight of ten middle-slice positives. The easy slice contains 432 of 444 positives (97.3%); most of the positive-class score therefore reflects this slice. The baseline shows the same qualitative pattern. The hard-slice estimate rests on only two positives, so it is highly uncertain and should not be generalized as a robust estimate of performance on hard matches elsewhere.

These bins are based on title surface similarity, not an independent measure of difficulty. The baseline also uses that same ratio for prediction, making its poor low-similarity recall partly a consequence of the definition; the trigram matcher uses a different score that still overlaps with the slicing signal. Slice positive rates differ sharply, affecting precision and F1. This is one benchmark, one candidate-pair split, and two simple matchers; scores do not describe all possible cross-table pairs or establish general production performance.
