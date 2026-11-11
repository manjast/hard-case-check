# Results

## What this shows

Scores change substantially when the mix of pairs changes, even though the matcher does not: Walmart-Amazon's trigram matcher rises from F1 0.370 to 0.824 under DBLP-ACM's mix. The learned matcher scores 0.981 overall on DBLP-ACM and 0.667–0.771 on the product datasets, but none of the original test splits meets the registered combination of high overall F1 and clearly lower hard-case recall with enough matching pairs. DBLP-ACM has only two matching hard pairs, while the learned Walmart-Amazon matcher recalls hard matches about as often as it recalls matches overall. Title similarity is only a proxy for difficulty, and these benchmark candidate pairs are not production traffic.

## Learned matcher

The [registered Amendment 2](protocol.md#amendment-2-2026-11-11) fixes one gradient-boosted model and feature list per dataset, without model selection or test-driven tuning. Models fit on train pairs; their probability thresholds maximize validation F1, without refitting. Title TF-IDF vocabulary and inverse document frequencies fit only on distinct records referenced by train pairs, not whole record tables or validation/test-only records. The original matchers retain train-selected thresholds.

Intervals below are the registered 95% pair-bootstrap intervals. Hard-slice positive counts are the numbers of true matches available to estimate recall.

| Dataset | Overall F1 [95% interval] | Overall recall [95% interval] | Hard positives | Hard recall [95% interval] | Hard F1 [95% interval] |
|---|---:|---:|---:|---:|---:|
| DBLP-ACM | 0.981 [0.971, 0.989] | 0.982 [0.968, 0.993] | 2 | 0.500 [0.000, 1.000] | 0.667 [0.000, 1.000] |
| Abt-Buy | 0.741 [0.692, 0.783] | 0.791 [0.735, 0.851] | 86 | 0.674 [0.571, 0.776] | 0.663 [0.575, 0.745] |
| Amazon-Google | 0.667 [0.615, 0.717] | 0.688 [0.627, 0.747] | 85 | 0.518 [0.411, 0.615] | 0.557 [0.457, 0.646] |
| Walmart-Amazon | 0.771 [0.721, 0.817] | 0.689 [0.624, 0.755] | 39 | 0.692 [0.541, 0.841] | 0.794 [0.677, 0.889] |

No dataset/matcher meets the registered combined criterion: overall F1 at least 0.90, at least 20 hard positives, and a hard-recall interval upper endpoint below the overall-recall lower endpoint. Only DBLP-ACM reaches 0.90 overall, but 432 of its 444 positives (97.3%) are easy and only two are hard. Its learned matcher finds one hard match and nine of ten middle matches, compared with zero and two for the trigram matcher. The product datasets have 39–86 hard positives but learned overall F1 remains below 0.90; Amazon-Google has a supported recall gap, Abt-Buy's intervals overlap, and Walmart-Amazon has no lower hard-recall point estimate. A low title-similarity bin is therefore not uniformly a worse slice for the learned matcher.

The title-ratio baseline uses the slicing score itself; the other matchers also use related title-similarity features. These bins therefore do not provide an independent measure of difficulty, and the baseline's zero hard recall follows directly from its threshold being above the hard-bin boundary.

## Bootstrap uncertainty

Every matcher and dataset has overall and all-slice recall/F1 intervals: 48 metric rows and 96 intervals in the detailed tables below. Each matcher/dataset uses 1,000 unstratified resamples of its full test-pair count, with seed 42, computed through equivalent slice/confusion-cell multinomial draws. Metrics with zero denominators are zero. All reported metrics are positive-class metrics and are rounded to three decimals; support flags use unrounded counts.

These intervals condition on the fitted model, threshold and supplied split; they do not include retraining uncertainty. Pairs can share records, so independent-pair resampling may understate uncertainty. Degenerate intervals at zero or one cannot reveal outcomes absent from the empirical sample and do not imply certainty about population performance. In particular, the old DBLP-ACM matchers' [0.000, 0.000] hard-recall intervals do not repair the two-positive support problem.


### DBLP-ACM

Train pairs: 7417; validation pairs: 2473; train-only TF-IDF vocabulary: 12098 terms.

Learned features: title trigram Dice; title token Jaccard; title TF-IDF cosine; title length ratio; title numeric-token Jaccard; authors trigram Dice; authors token Jaccard; year equality.

#### Title ratio

Train-selected threshold: 0.87.

| Slice | Pairs | Positives | Positive rate | Precision | Recall [95% interval] | F1 [95% interval] | Support |
|---|---:|---:|---:|---:|---:|---:|---|
| Overall | 2473 | 444 | 0.180 | 0.855 | 0.968 [0.952, 0.984] | 0.908 [0.888, 0.927] | at least 20 positives |
| Hard | 1430 | 2 | 0.001 | 0.000 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | insufficient (<20 positives) |
| Middle | 534 | 10 | 0.019 | 0.000 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | insufficient (<20 positives) |
| Easy | 509 | 432 | 0.849 | 0.855 | 0.995 [0.988, 1.000] | 0.920 [0.901, 0.937] | at least 20 positives |

#### Trigram Dice

Train-selected threshold: 0.84.

| Slice | Pairs | Positives | Positive rate | Precision | Recall [95% interval] | F1 [95% interval] | Support |
|---|---:|---:|---:|---:|---:|---:|---|
| Overall | 2473 | 444 | 0.180 | 0.928 | 0.959 [0.941, 0.975] | 0.944 [0.928, 0.957] | at least 20 positives |
| Hard | 1430 | 2 | 0.001 | 0.000 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | insufficient (<20 positives) |
| Middle | 534 | 10 | 0.019 | 0.667 | 0.200 [0.000, 0.500] | 0.308 [0.000, 0.625] | insufficient (<20 positives) |
| Easy | 509 | 432 | 0.849 | 0.930 | 0.981 [0.968, 0.993] | 0.955 [0.940, 0.968] | at least 20 positives |

#### Learned

Validation-selected threshold: 0.66729172115606328.

| Slice | Pairs | Positives | Positive rate | Precision | Recall [95% interval] | F1 [95% interval] | Support |
|---|---:|---:|---:|---:|---:|---:|---|
| Overall | 2473 | 444 | 0.180 | 0.980 | 0.982 [0.968, 0.993] | 0.981 [0.971, 0.989] | at least 20 positives |
| Hard | 1430 | 2 | 0.001 | 1.000 | 0.500 [0.000, 1.000] | 0.667 [0.000, 1.000] | insufficient (<20 positives) |
| Middle | 534 | 10 | 0.019 | 0.818 | 0.900 [0.667, 1.000] | 0.857 [0.666, 1.000] | insufficient (<20 positives) |
| Easy | 509 | 432 | 0.849 | 0.984 | 0.986 [0.973, 0.996] | 0.985 [0.976, 0.992] | at least 20 positives |

### Abt-Buy

Train pairs: 5743; validation pairs: 1916; train-only TF-IDF vocabulary: 10810 terms.

Learned features: title trigram Dice; title token Jaccard; title TF-IDF cosine; title length ratio; title numeric-token Jaccard; description trigram Dice; description token Jaccard; price agreement.

#### Title ratio

Train-selected threshold: 0.68.

| Slice | Pairs | Positives | Positive rate | Precision | Recall [95% interval] | F1 [95% interval] | Support |
|---|---:|---:|---:|---:|---:|---:|---|
| Overall | 1916 | 206 | 0.108 | 0.377 | 0.447 [0.377, 0.518] | 0.409 [0.348, 0.467] | at least 20 positives |
| Hard | 1316 | 86 | 0.065 | 0.000 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | at least 20 positives |
| Middle | 578 | 104 | 0.180 | 0.342 | 0.731 [0.642, 0.815] | 0.466 [0.398, 0.532] | at least 20 positives |
| Easy | 22 | 16 | 0.727 | 0.727 | 1.000 [1.000, 1.000] | 0.842 [0.692, 0.950] | insufficient (<20 positives) |

#### Trigram Dice

Train-selected threshold: 0.63.

| Slice | Pairs | Positives | Positive rate | Precision | Recall [95% interval] | F1 [95% interval] | Support |
|---|---:|---:|---:|---:|---:|---:|---|
| Overall | 1916 | 206 | 0.108 | 0.442 | 0.466 [0.397, 0.531] | 0.454 [0.392, 0.512] | at least 20 positives |
| Hard | 1316 | 86 | 0.065 | 0.700 | 0.081 [0.025, 0.139] | 0.146 [0.048, 0.238] | at least 20 positives |
| Middle | 578 | 104 | 0.180 | 0.395 | 0.702 [0.611, 0.794] | 0.505 [0.433, 0.578] | at least 20 positives |
| Easy | 22 | 16 | 0.727 | 0.727 | 1.000 [1.000, 1.000] | 0.842 [0.690, 0.944] | insufficient (<20 positives) |

#### Learned

Validation-selected threshold: 0.26357348605344588.

| Slice | Pairs | Positives | Positive rate | Precision | Recall [95% interval] | F1 [95% interval] | Support |
|---|---:|---:|---:|---:|---:|---:|---|
| Overall | 1916 | 206 | 0.108 | 0.697 | 0.791 [0.735, 0.851] | 0.741 [0.692, 0.783] | at least 20 positives |
| Hard | 1316 | 86 | 0.065 | 0.652 | 0.674 [0.571, 0.776] | 0.663 [0.575, 0.745] | at least 20 positives |
| Middle | 578 | 104 | 0.180 | 0.700 | 0.875 [0.808, 0.935] | 0.778 [0.714, 0.832] | at least 20 positives |
| Easy | 22 | 16 | 0.727 | 0.933 | 0.875 [0.692, 1.000] | 0.903 [0.774, 1.000] | insufficient (<20 positives) |

### Amazon-Google

Train pairs: 6874; validation pairs: 2293; train-only TF-IDF vocabulary: 10922 terms.

Learned features: title trigram Dice; title token Jaccard; title TF-IDF cosine; title length ratio; title numeric-token Jaccard; manufacturer trigram Dice; manufacturer token Jaccard; price agreement.

#### Title ratio

Train-selected threshold: 0.68.

| Slice | Pairs | Positives | Positive rate | Precision | Recall [95% interval] | F1 [95% interval] | Support |
|---|---:|---:|---:|---:|---:|---:|---|
| Overall | 2293 | 234 | 0.102 | 0.352 | 0.487 [0.423, 0.551] | 0.409 [0.356, 0.458] | at least 20 positives |
| Hard | 1663 | 85 | 0.051 | 0.000 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | at least 20 positives |
| Middle | 557 | 111 | 0.199 | 0.303 | 0.685 [0.602, 0.768] | 0.420 [0.353, 0.483] | at least 20 positives |
| Easy | 73 | 38 | 0.521 | 0.521 | 1.000 [1.000, 1.000] | 0.685 [0.580, 0.781] | at least 20 positives |

#### Trigram Dice

Train-selected threshold: 0.52.

| Slice | Pairs | Positives | Positive rate | Precision | Recall [95% interval] | F1 [95% interval] | Support |
|---|---:|---:|---:|---:|---:|---:|---|
| Overall | 2293 | 234 | 0.102 | 0.433 | 0.509 [0.446, 0.570] | 0.468 [0.414, 0.520] | at least 20 positives |
| Hard | 1663 | 85 | 0.051 | 0.203 | 0.153 [0.080, 0.241] | 0.174 [0.091, 0.262] | at least 20 positives |
| Middle | 557 | 111 | 0.199 | 0.489 | 0.613 [0.520, 0.701] | 0.544 [0.465, 0.618] | at least 20 positives |
| Easy | 73 | 38 | 0.521 | 0.528 | 1.000 [1.000, 1.000] | 0.691 [0.587, 0.793] | at least 20 positives |

#### Learned

Validation-selected threshold: 0.33946340869258979.

| Slice | Pairs | Positives | Positive rate | Precision | Recall [95% interval] | F1 [95% interval] | Support |
|---|---:|---:|---:|---:|---:|---:|---|
| Overall | 2293 | 234 | 0.102 | 0.647 | 0.688 [0.627, 0.747] | 0.667 [0.615, 0.717] | at least 20 positives |
| Hard | 1663 | 85 | 0.051 | 0.603 | 0.518 [0.411, 0.615] | 0.557 [0.457, 0.646] | at least 20 positives |
| Middle | 557 | 111 | 0.199 | 0.648 | 0.748 [0.661, 0.830] | 0.695 [0.617, 0.761] | at least 20 positives |
| Easy | 73 | 38 | 0.521 | 0.708 | 0.895 [0.791, 0.976] | 0.791 [0.690, 0.879] | at least 20 positives |

### Walmart-Amazon

Train pairs: 6144; validation pairs: 2049; train-only TF-IDF vocabulary: 28183 terms.

Learned features: title trigram Dice; title token Jaccard; title TF-IDF cosine; title length ratio; title numeric-token Jaccard; brand trigram Dice; brand token Jaccard; price agreement; modelno equality.

#### Title ratio

Train-selected threshold: 0.82.

| Slice | Pairs | Positives | Positive rate | Precision | Recall [95% interval] | F1 [95% interval] | Support |
|---|---:|---:|---:|---:|---:|---:|---|
| Overall | 2049 | 193 | 0.094 | 0.306 | 0.269 [0.208, 0.332] | 0.287 [0.223, 0.347] | at least 20 positives |
| Hard | 401 | 39 | 0.097 | 0.000 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | at least 20 positives |
| Middle | 1543 | 109 | 0.071 | 0.108 | 0.064 [0.019, 0.112] | 0.080 [0.024, 0.136] | at least 20 positives |
| Easy | 105 | 45 | 0.429 | 0.429 | 1.000 [1.000, 1.000] | 0.600 [0.503, 0.689] | at least 20 positives |

#### Trigram Dice

Train-selected threshold: 0.81.

| Slice | Pairs | Positives | Positive rate | Precision | Recall [95% interval] | F1 [95% interval] | Support |
|---|---:|---:|---:|---:|---:|---:|---|
| Overall | 2049 | 193 | 0.094 | 0.402 | 0.342 [0.276, 0.409] | 0.370 [0.306, 0.435] | at least 20 positives |
| Hard | 401 | 39 | 0.097 | 0.000 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | at least 20 positives |
| Middle | 1543 | 109 | 0.071 | 0.350 | 0.257 [0.177, 0.342] | 0.296 [0.208, 0.380] | at least 20 positives |
| Easy | 105 | 45 | 0.429 | 0.458 | 0.844 [0.723, 0.939] | 0.594 [0.481, 0.686] | at least 20 positives |

#### Learned

Validation-selected threshold: 0.77026400948540341.

| Slice | Pairs | Positives | Positive rate | Precision | Recall [95% interval] | F1 [95% interval] | Support |
|---|---:|---:|---:|---:|---:|---:|---|
| Overall | 2049 | 193 | 0.094 | 0.875 | 0.689 [0.624, 0.755] | 0.771 [0.721, 0.817] | at least 20 positives |
| Hard | 401 | 39 | 0.097 | 0.931 | 0.692 [0.541, 0.841] | 0.794 [0.677, 0.889] | at least 20 positives |
| Middle | 1543 | 109 | 0.071 | 0.850 | 0.624 [0.538, 0.709] | 0.720 [0.641, 0.788] | at least 20 positives |
| Easy | 105 | 45 | 0.429 | 0.884 | 0.844 [0.738, 0.947] | 0.864 [0.783, 0.933] | at least 20 positives |


### Cross-dataset summaries


| Dataset | Matcher | Overall F1 [95% interval] | Overall recall [95% interval] | Hard positives | Hard recall [95% interval] | Hard F1 [95% interval] | High F1 and supported recall gap |
|---|---|---:|---:|---:|---:|---:|---|
| DBLP-ACM | Title ratio | 0.908 [0.888, 0.927] | 0.968 [0.952, 0.984] | 2 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | no |
| DBLP-ACM | Trigram Dice | 0.944 [0.928, 0.957] | 0.959 [0.941, 0.975] | 2 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | no |
| DBLP-ACM | Learned | 0.981 [0.971, 0.989] | 0.982 [0.968, 0.993] | 2 | 0.500 [0.000, 1.000] | 0.667 [0.000, 1.000] | no |
| Abt-Buy | Title ratio | 0.409 [0.348, 0.467] | 0.447 [0.377, 0.518] | 86 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | no |
| Abt-Buy | Trigram Dice | 0.454 [0.392, 0.512] | 0.466 [0.397, 0.531] | 86 | 0.081 [0.025, 0.139] | 0.146 [0.048, 0.238] | no |
| Abt-Buy | Learned | 0.741 [0.692, 0.783] | 0.791 [0.735, 0.851] | 86 | 0.674 [0.571, 0.776] | 0.663 [0.575, 0.745] | no |
| Amazon-Google | Title ratio | 0.409 [0.356, 0.458] | 0.487 [0.423, 0.551] | 85 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | no |
| Amazon-Google | Trigram Dice | 0.468 [0.414, 0.520] | 0.509 [0.446, 0.570] | 85 | 0.153 [0.080, 0.241] | 0.174 [0.091, 0.262] | no |
| Amazon-Google | Learned | 0.667 [0.615, 0.717] | 0.688 [0.627, 0.747] | 85 | 0.518 [0.411, 0.615] | 0.557 [0.457, 0.646] | no |
| Walmart-Amazon | Title ratio | 0.287 [0.223, 0.347] | 0.269 [0.208, 0.332] | 39 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | no |
| Walmart-Amazon | Trigram Dice | 0.370 [0.306, 0.435] | 0.342 [0.276, 0.409] | 39 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | no |
| Walmart-Amazon | Learned | 0.771 [0.721, 0.817] | 0.689 [0.624, 0.755] | 39 | 0.692 [0.541, 0.841] | 0.794 [0.677, 0.889] | no |

### All-slice cross-dataset summary

Each slice cell reports positives / recall [95% interval] / F1 [95% interval].

| Dataset | Matcher | Hard | Middle | Easy |
|---|---|---:|---:|---:|
| DBLP-ACM | Title ratio | 2 / 0.000 [0.000, 0.000] / 0.000 [0.000, 0.000] | 10 / 0.000 [0.000, 0.000] / 0.000 [0.000, 0.000] | 432 / 0.995 [0.988, 1.000] / 0.920 [0.901, 0.937] |
| DBLP-ACM | Trigram Dice | 2 / 0.000 [0.000, 0.000] / 0.000 [0.000, 0.000] | 10 / 0.200 [0.000, 0.500] / 0.308 [0.000, 0.625] | 432 / 0.981 [0.968, 0.993] / 0.955 [0.940, 0.968] |
| DBLP-ACM | Learned | 2 / 0.500 [0.000, 1.000] / 0.667 [0.000, 1.000] | 10 / 0.900 [0.667, 1.000] / 0.857 [0.666, 1.000] | 432 / 0.986 [0.973, 0.996] / 0.985 [0.976, 0.992] |
| Abt-Buy | Title ratio | 86 / 0.000 [0.000, 0.000] / 0.000 [0.000, 0.000] | 104 / 0.731 [0.642, 0.815] / 0.466 [0.398, 0.532] | 16 / 1.000 [1.000, 1.000] / 0.842 [0.692, 0.950] |
| Abt-Buy | Trigram Dice | 86 / 0.081 [0.025, 0.139] / 0.146 [0.048, 0.238] | 104 / 0.702 [0.611, 0.794] / 0.505 [0.433, 0.578] | 16 / 1.000 [1.000, 1.000] / 0.842 [0.690, 0.944] |
| Abt-Buy | Learned | 86 / 0.674 [0.571, 0.776] / 0.663 [0.575, 0.745] | 104 / 0.875 [0.808, 0.935] / 0.778 [0.714, 0.832] | 16 / 0.875 [0.692, 1.000] / 0.903 [0.774, 1.000] |
| Amazon-Google | Title ratio | 85 / 0.000 [0.000, 0.000] / 0.000 [0.000, 0.000] | 111 / 0.685 [0.602, 0.768] / 0.420 [0.353, 0.483] | 38 / 1.000 [1.000, 1.000] / 0.685 [0.580, 0.781] |
| Amazon-Google | Trigram Dice | 85 / 0.153 [0.080, 0.241] / 0.174 [0.091, 0.262] | 111 / 0.613 [0.520, 0.701] / 0.544 [0.465, 0.618] | 38 / 1.000 [1.000, 1.000] / 0.691 [0.587, 0.793] |
| Amazon-Google | Learned | 85 / 0.518 [0.411, 0.615] / 0.557 [0.457, 0.646] | 111 / 0.748 [0.661, 0.830] / 0.695 [0.617, 0.761] | 38 / 0.895 [0.791, 0.976] / 0.791 [0.690, 0.879] |
| Walmart-Amazon | Title ratio | 39 / 0.000 [0.000, 0.000] / 0.000 [0.000, 0.000] | 109 / 0.064 [0.019, 0.112] / 0.080 [0.024, 0.136] | 45 / 1.000 [1.000, 1.000] / 0.600 [0.503, 0.689] |
| Walmart-Amazon | Trigram Dice | 39 / 0.000 [0.000, 0.000] / 0.000 [0.000, 0.000] | 109 / 0.257 [0.177, 0.342] / 0.296 [0.208, 0.380] | 45 / 0.844 [0.723, 0.939] / 0.594 [0.481, 0.686] |
| Walmart-Amazon | Learned | 39 / 0.692 [0.541, 0.841] / 0.794 [0.677, 0.889] | 109 / 0.624 [0.538, 0.709] / 0.720 [0.641, 0.788] | 45 / 0.844 [0.738, 0.947] / 0.864 [0.783, 0.933] |


## Difficulty-mix analysis

Within each source slice, keep the true-positive and false-positive rates fixed. Scale positive confusion cells by the target/source positive-count ratio and negative cells by the target/source negative-count ratio, then sum and recompute overall precision, recall and F1. This matches both the target pair counts and positive counts per slice, not just the share of easy pairs. The target uses labels only to specify its mix; neither a model nor a threshold changes.

### Key comparisons with the DBLP-ACM mix

| Source | Matcher | Original precision / recall / F1 | DBLP-ACM-mix precision / recall / F1 |
|---|---|---:|---:|
| Amazon-Google | Title ratio | 0.352 / 0.487 / 0.409 | 0.608 / 0.988 / 0.753 |
| Amazon-Google | Trigram Dice | 0.433 / 0.509 / 0.468 | 0.682 / 0.987 / 0.807 |
| Amazon-Google | Learned | 0.647 / 0.688 / 0.667 | 0.782 / 0.890 / 0.833 |
| Walmart-Amazon | Title ratio | 0.306 / 0.269 / 0.287 | 0.815 / 0.974 / 0.888 |
| Walmart-Amazon | Trigram Dice | 0.402 / 0.342 / 0.370 | 0.820 / 0.827 / 0.824 |
| Walmart-Amazon | Learned | 0.875 / 0.689 / 0.771 | 0.952 / 0.839 / 0.892 |

All DBLP-ACM-to-product comparisons are **not estimable**: source hard/middle positive counts are 2/10, below the registered minimum of 20. All Abt-Buy-source comparisons, including Abt-Buy to DBLP-ACM, are **not estimable** because its easy slice has only 16 positives and six negatives. Amazon-Google and Walmart-Amazon meet the source support rules in all slices, giving 18 estimable and 18 non-estimable comparisons across three matchers. Every ordered comparison, including refusals, appears below.

The mix effect can be large, but this is descriptive standardization, not measured cross-dataset transfer. It changes both the distribution of true matches across slices and slice class composition, so gains cannot be attributed to the easy-pair fraction alone. It assumes the source's within-slice class-conditional rates stay fixed; broad title bins do not make domains interchangeable. No reweighted score reaches the registered high-F1 cutoff of 0.90, and no intervals were planned for reweighted scores.


### Observed mix (target counts)

| Dataset | Slice | Pairs | Positives | Negatives |
|---|---|---:|---:|---:|
| DBLP-ACM | Hard | 1430 | 2 | 1428 |
| DBLP-ACM | Middle | 534 | 10 | 524 |
| DBLP-ACM | Easy | 509 | 432 | 77 |
| Abt-Buy | Hard | 1316 | 86 | 1230 |
| Abt-Buy | Middle | 578 | 104 | 474 |
| Abt-Buy | Easy | 22 | 16 | 6 |
| Amazon-Google | Hard | 1663 | 85 | 1578 |
| Amazon-Google | Middle | 557 | 111 | 446 |
| Amazon-Google | Easy | 73 | 38 | 35 |
| Walmart-Amazon | Hard | 401 | 39 | 362 |
| Walmart-Amazon | Middle | 1543 | 109 | 1434 |
| Walmart-Amazon | Easy | 105 | 45 | 60 |

### Source slice confusion counts

| Dataset | Matcher | Slice | TP | FP | FN | TN |
|---|---|---|---:|---:|---:|---:|
| DBLP-ACM | Title ratio | Hard | 0 | 0 | 2 | 1428 |
| DBLP-ACM | Title ratio | Middle | 0 | 0 | 10 | 524 |
| DBLP-ACM | Title ratio | Easy | 430 | 73 | 2 | 4 |
| DBLP-ACM | Trigram Dice | Hard | 0 | 0 | 2 | 1428 |
| DBLP-ACM | Trigram Dice | Middle | 2 | 1 | 8 | 523 |
| DBLP-ACM | Trigram Dice | Easy | 424 | 32 | 8 | 45 |
| DBLP-ACM | Learned | Hard | 1 | 0 | 1 | 1428 |
| DBLP-ACM | Learned | Middle | 9 | 2 | 1 | 522 |
| DBLP-ACM | Learned | Easy | 426 | 7 | 6 | 70 |
| Abt-Buy | Title ratio | Hard | 0 | 0 | 86 | 1230 |
| Abt-Buy | Title ratio | Middle | 76 | 146 | 28 | 328 |
| Abt-Buy | Title ratio | Easy | 16 | 6 | 0 | 0 |
| Abt-Buy | Trigram Dice | Hard | 7 | 3 | 79 | 1227 |
| Abt-Buy | Trigram Dice | Middle | 73 | 112 | 31 | 362 |
| Abt-Buy | Trigram Dice | Easy | 16 | 6 | 0 | 0 |
| Abt-Buy | Learned | Hard | 58 | 31 | 28 | 1199 |
| Abt-Buy | Learned | Middle | 91 | 39 | 13 | 435 |
| Abt-Buy | Learned | Easy | 14 | 1 | 2 | 5 |
| Amazon-Google | Title ratio | Hard | 0 | 0 | 85 | 1578 |
| Amazon-Google | Title ratio | Middle | 76 | 175 | 35 | 271 |
| Amazon-Google | Title ratio | Easy | 38 | 35 | 0 | 0 |
| Amazon-Google | Trigram Dice | Hard | 13 | 51 | 72 | 1527 |
| Amazon-Google | Trigram Dice | Middle | 68 | 71 | 43 | 375 |
| Amazon-Google | Trigram Dice | Easy | 38 | 34 | 0 | 1 |
| Amazon-Google | Learned | Hard | 44 | 29 | 41 | 1549 |
| Amazon-Google | Learned | Middle | 83 | 45 | 28 | 401 |
| Amazon-Google | Learned | Easy | 34 | 14 | 4 | 21 |
| Walmart-Amazon | Title ratio | Hard | 0 | 0 | 39 | 362 |
| Walmart-Amazon | Title ratio | Middle | 7 | 58 | 102 | 1376 |
| Walmart-Amazon | Title ratio | Easy | 45 | 60 | 0 | 0 |
| Walmart-Amazon | Trigram Dice | Hard | 0 | 1 | 39 | 361 |
| Walmart-Amazon | Trigram Dice | Middle | 28 | 52 | 81 | 1382 |
| Walmart-Amazon | Trigram Dice | Easy | 38 | 45 | 7 | 15 |
| Walmart-Amazon | Learned | Hard | 27 | 2 | 12 | 360 |
| Walmart-Amazon | Learned | Middle | 68 | 12 | 41 | 1422 |
| Walmart-Amazon | Learned | Easy | 38 | 5 | 7 | 55 |

### Reweighted overall scores

Each original and reweighted score cell is precision / recall / F1. Not estimable means a source slice/class fails the registered minimum of 20. Target counts specify a fixed mix, not target performance. No model is retrained.

| Source | Target mix | Matcher | Original precision / recall / F1 | Reweighted precision / recall / F1 | Status |
|---|---|---|---:|---:|---|
| DBLP-ACM | Abt-Buy | Title ratio | 0.855 / 0.968 / 0.908 | not estimable | hard positives=2; middle positives=10 |
| DBLP-ACM | Abt-Buy | Trigram Dice | 0.928 / 0.959 / 0.944 | not estimable | hard positives=2; middle positives=10 |
| DBLP-ACM | Abt-Buy | Learned | 0.980 / 0.982 / 0.981 | not estimable | hard positives=2; middle positives=10 |
| DBLP-ACM | Amazon-Google | Title ratio | 0.855 / 0.968 / 0.908 | not estimable | hard positives=2; middle positives=10 |
| DBLP-ACM | Amazon-Google | Trigram Dice | 0.928 / 0.959 / 0.944 | not estimable | hard positives=2; middle positives=10 |
| DBLP-ACM | Amazon-Google | Learned | 0.980 / 0.982 / 0.981 | not estimable | hard positives=2; middle positives=10 |
| DBLP-ACM | Walmart-Amazon | Title ratio | 0.855 / 0.968 / 0.908 | not estimable | hard positives=2; middle positives=10 |
| DBLP-ACM | Walmart-Amazon | Trigram Dice | 0.928 / 0.959 / 0.944 | not estimable | hard positives=2; middle positives=10 |
| DBLP-ACM | Walmart-Amazon | Learned | 0.980 / 0.982 / 0.981 | not estimable | hard positives=2; middle positives=10 |
| Abt-Buy | DBLP-ACM | Title ratio | 0.377 / 0.447 / 0.409 | not estimable | easy positives=16; easy negatives=6 |
| Abt-Buy | DBLP-ACM | Trigram Dice | 0.442 / 0.466 / 0.454 | not estimable | easy positives=16; easy negatives=6 |
| Abt-Buy | DBLP-ACM | Learned | 0.697 / 0.791 / 0.741 | not estimable | easy positives=16; easy negatives=6 |
| Abt-Buy | Amazon-Google | Title ratio | 0.377 / 0.447 / 0.409 | not estimable | easy positives=16; easy negatives=6 |
| Abt-Buy | Amazon-Google | Trigram Dice | 0.442 / 0.466 / 0.454 | not estimable | easy positives=16; easy negatives=6 |
| Abt-Buy | Amazon-Google | Learned | 0.697 / 0.791 / 0.741 | not estimable | easy positives=16; easy negatives=6 |
| Abt-Buy | Walmart-Amazon | Title ratio | 0.377 / 0.447 / 0.409 | not estimable | easy positives=16; easy negatives=6 |
| Abt-Buy | Walmart-Amazon | Trigram Dice | 0.442 / 0.466 / 0.454 | not estimable | easy positives=16; easy negatives=6 |
| Abt-Buy | Walmart-Amazon | Learned | 0.697 / 0.791 / 0.741 | not estimable | easy positives=16; easy negatives=6 |
| Amazon-Google | DBLP-ACM | Title ratio | 0.352 / 0.487 / 0.409 | 0.608 / 0.988 / 0.753 | estimable |
| Amazon-Google | DBLP-ACM | Trigram Dice | 0.433 / 0.509 / 0.468 | 0.682 / 0.987 / 0.807 | estimable |
| Amazon-Google | DBLP-ACM | Learned | 0.647 / 0.688 / 0.667 | 0.782 / 0.890 / 0.833 | estimable |
| Amazon-Google | Abt-Buy | Title ratio | 0.352 / 0.487 / 0.409 | 0.312 / 0.423 / 0.359 | estimable |
| Amazon-Google | Abt-Buy | Trigram Dice | 0.433 / 0.509 / 0.468 | 0.434 / 0.451 / 0.442 | estimable |
| Amazon-Google | Abt-Buy | Learned | 0.647 / 0.688 / 0.667 | 0.652 / 0.663 / 0.658 | estimable |
| Amazon-Google | Walmart-Amazon | Title ratio | 0.352 / 0.487 / 0.409 | 0.161 / 0.620 / 0.256 | estimable |
| Amazon-Google | Walmart-Amazon | Trigram Dice | 0.433 / 0.509 / 0.468 | 0.283 / 0.610 / 0.387 | estimable |
| Amazon-Google | Walmart-Amazon | Learned | 0.647 / 0.688 / 0.667 | 0.447 / 0.736 / 0.556 | estimable |
| Walmart-Amazon | DBLP-ACM | Title ratio | 0.306 / 0.269 / 0.287 | 0.815 / 0.974 / 0.888 | estimable |
| Walmart-Amazon | DBLP-ACM | Trigram Dice | 0.402 / 0.342 / 0.370 | 0.820 / 0.827 / 0.824 | estimable |
| Walmart-Amazon | DBLP-ACM | Learned | 0.875 / 0.689 / 0.771 | 0.952 / 0.839 / 0.892 | estimable |
| Walmart-Amazon | Abt-Buy | Title ratio | 0.306 / 0.269 / 0.287 | 0.474 / 0.110 / 0.179 | estimable |
| Walmart-Amazon | Abt-Buy | Trigram Dice | 0.402 / 0.342 / 0.370 | 0.616 / 0.195 / 0.297 | estimable |
| Walmart-Amazon | Abt-Buy | Learned | 0.875 / 0.689 / 0.771 | 0.925 / 0.670 / 0.777 | estimable |
| Walmart-Amazon | Amazon-Google | Title ratio | 0.306 / 0.269 / 0.287 | 0.460 / 0.193 / 0.272 | estimable |
| Walmart-Amazon | Amazon-Google | Trigram Dice | 0.402 / 0.342 / 0.370 | 0.564 / 0.259 / 0.355 | estimable |
| Walmart-Amazon | Amazon-Google | Learned | 0.875 / 0.689 / 0.771 | 0.912 / 0.685 / 0.782 | estimable |

## Reproduction and run record

Amendment 2 was committed as `c3f5727` before implementing or running these analyses. The single completed all-dataset run exited successfully without stderr; elapsed time was 98.18 seconds and peak child resident memory was 135,960 KiB (about 133 MiB). An initial invocation stopped at a missing canonical DBLP-ACM archive filename before loading train pairs or evaluating any test split; the registered downloader then fetched and verified the expected archive. No methods were changed after seeing test outcomes, and no test suite, linter or formatter was run.

The two fixed matchers reproduce the earlier reported thresholds and scores; their deterministic predictions were recomputed for the new bootstrap and standardization analyses. The learned matcher evaluates each supplied test split only after train fitting and validation threshold selection. See the [README](../README.md#reproduce) for the commands and pinned dependencies.


numpy 2.3.5; scikit-learn 1.7.2; scipy 1.18.1; joblib 1.6.0; threadpoolctl 3.8.0; cloudpickle 3.1.2; Python 3.12.13.

HistGradientBoostingClassifier settings: `{'loss': 'log_loss', 'learning_rate': 0.1, 'max_iter': 200, 'max_leaf_nodes': 31, 'max_depth': None, 'min_samples_leaf': 20, 'l2_regularization': 1.0, 'max_bins': 255, 'categorical_features': None, 'early_stopping': False, 'class_weight': None, 'random_state': 42}`.

One native-library thread; seed 42; 1000 full-test-pair bootstrap resamples via slice/confusion-cell multinomial counts; linear 95% percentile intervals.

TF-IDF vocabulary and IDF fitted only on train-referenced records; classifier fitted only on train; learned threshold selected on validation, existing thresholds on train.

High F1 means at least 0.90; a supported recall gap requires at least 20 hard positives and hard-recall upper interval below overall-recall lower interval.

