# Results

Each supplied test split was evaluated once under the [preregistered protocol](protocol.md), including its dated extension. Thresholds were selected on train, not test. Metrics are positive-class metrics; zero denominators are reported as zero. Values are rounded to three decimals.

## Cross-dataset summary: trigram matcher

Each slice cell reports positives / recall / F1.

| Dataset | Overall F1 | Hard | Middle | Easy |
|---|---:|---:|---:|---:|
| DBLP-ACM | 0.944 | 2 / 0.000 / 0.000 | 10 / 0.200 / 0.308 | 432 / 0.981 / 0.955 |
| Abt-Buy | 0.454 | 86 / 0.081 / 0.146 | 104 / 0.702 / 0.505 | 16 / 1.000 / 0.842 |
| Amazon-Google | 0.468 | 85 / 0.153 / 0.174 | 111 / 0.613 / 0.544 | 38 / 1.000 / 0.691 |
| Walmart-Amazon | 0.370 | 39 / 0.000 / 0.000 | 109 / 0.257 / 0.296 | 45 / 0.844 / 0.594 |

The product datasets show low hard-slice recall, but also much lower overall F1 than DBLP-ACM. Thus, the specific combination of high overall F1 and poor hard performance is most evident on DBLP-ACM, where only two hard positives make that slice especially uncertain. The product hard slices contain 86, 85, and 39 positives respectively; those estimates are also subject to sampling uncertainty.

## DBLP-ACM

### Title ratio baseline

Train-selected threshold: 0.87.

| Slice | Pairs | Positives | Positive rate | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|
| Overall | 2473 | 444 | 0.180 | 0.855 | 0.968 | 0.908 |
| Hard | 1430 | 2 | 0.001 | 0.000 | 0.000 | 0.000 |
| Middle | 534 | 10 | 0.019 | 0.000 | 0.000 | 0.000 |
| Easy | 509 | 432 | 0.849 | 0.855 | 0.995 | 0.920 |

### Title/author trigram Dice

Train-selected threshold: 0.84.

| Slice | Pairs | Positives | Positive rate | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|
| Overall | 2473 | 444 | 0.180 | 0.928 | 0.959 | 0.944 |
| Hard | 1430 | 2 | 0.001 | 0.000 | 0.000 | 0.000 |
| Middle | 534 | 10 | 0.019 | 0.667 | 0.200 | 0.308 |
| Easy | 509 | 432 | 0.849 | 0.930 | 0.981 | 0.955 |

The trigram matcher has overall F1 0.944, but misses both hard-slice positives and eight of ten middle-slice positives. The easy slice contains 432 of 444 positives (97.3%); most of the positive-class score therefore reflects this slice. The baseline shows the same qualitative pattern. The hard-slice estimate rests on only two positives, so it is highly uncertain and should not be generalized as a robust estimate of performance on hard matches elsewhere.

These bins are based on title surface similarity, not an independent measure of difficulty. The baseline also uses that same ratio for prediction, making its poor low-similarity recall partly a consequence of the definition; the trigram matcher uses a different score that still overlaps with the slicing signal. Slice positive rates differ sharply, affecting precision and F1. These four candidate-pair test splits and two simple matchers do not describe all possible cross-table pairs or establish general production performance.

## Abt-Buy (textual)

### Title ratio baseline

Train-selected threshold: 0.68.

| Slice | Pairs | Positives | Positive rate | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|
| Overall | 1916 | 206 | 0.108 | 0.377 | 0.447 | 0.409 |
| Hard | 1316 | 86 | 0.065 | 0.000 | 0.000 | 0.000 |
| Middle | 578 | 104 | 0.180 | 0.342 | 0.731 | 0.466 |
| Easy | 22 | 16 | 0.727 | 0.727 | 1.000 | 0.842 |

### Title trigram Dice

Train-selected threshold: 0.63.

| Slice | Pairs | Positives | Positive rate | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|
| Overall | 1916 | 206 | 0.108 | 0.442 | 0.466 | 0.454 |
| Hard | 1316 | 86 | 0.065 | 0.700 | 0.081 | 0.146 |
| Middle | 578 | 104 | 0.180 | 0.395 | 0.702 | 0.505 |
| Easy | 22 | 16 | 0.727 | 0.727 | 1.000 | 0.842 |

## Amazon-Google (structured)

### Title ratio baseline

Train-selected threshold: 0.68.

| Slice | Pairs | Positives | Positive rate | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|
| Overall | 2293 | 234 | 0.102 | 0.352 | 0.487 | 0.409 |
| Hard | 1663 | 85 | 0.051 | 0.000 | 0.000 | 0.000 |
| Middle | 557 | 111 | 0.199 | 0.303 | 0.685 | 0.420 |
| Easy | 73 | 38 | 0.521 | 0.521 | 1.000 | 0.685 |

### Title/manufacturer trigram Dice

Train-selected threshold: 0.52.

| Slice | Pairs | Positives | Positive rate | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|
| Overall | 2293 | 234 | 0.102 | 0.433 | 0.509 | 0.468 |
| Hard | 1663 | 85 | 0.051 | 0.203 | 0.153 | 0.174 |
| Middle | 557 | 111 | 0.199 | 0.489 | 0.613 | 0.544 |
| Easy | 73 | 38 | 0.521 | 0.528 | 1.000 | 0.691 |

## Walmart-Amazon (structured)

### Title ratio baseline

Train-selected threshold: 0.82.

| Slice | Pairs | Positives | Positive rate | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|
| Overall | 2049 | 193 | 0.094 | 0.306 | 0.269 | 0.287 |
| Hard | 401 | 39 | 0.097 | 0.000 | 0.000 | 0.000 |
| Middle | 1543 | 109 | 0.071 | 0.108 | 0.064 | 0.080 |
| Easy | 105 | 45 | 0.429 | 0.429 | 1.000 | 0.600 |

### Title/brand trigram Dice

Train-selected threshold: 0.81.

| Slice | Pairs | Positives | Positive rate | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|
| Overall | 2049 | 193 | 0.094 | 0.402 | 0.342 | 0.370 |
| Hard | 401 | 39 | 0.097 | 0.000 | 0.000 | 0.000 |
| Middle | 1543 | 109 | 0.071 | 0.350 | 0.257 | 0.296 |
| Easy | 105 | 45 | 0.429 | 0.458 | 0.844 | 0.594 |
