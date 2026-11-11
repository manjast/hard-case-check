# Evaluation protocol

Registered before running either matcher.

## Data and split

Use the structured DBLP-ACM experimental data from [DeepMatcher](https://github.com/anhaidgroup/deepmatcher/blob/master/Datasets.md#dblp-acm), including its supplied train, valid and test pair lists and two record tables. Do not resplit. Train selects thresholds; validation is not used for selection or fitting. Test is evaluated once after the method and thresholds are fixed.

## Difficulty

Compare each pair's title fields without looking at labels or predictions: lowercase with Unicode casefold, collapse whitespace, and use Python `difflib.SequenceMatcher` ratio with `autojunk=False`. Missing text becomes empty. This symmetric-looking ratio is evaluated in left-to-right order as supplied. Define hard as ratio < 0.60, middle as 0.60 <= ratio < 0.85, and easy as ratio >= 0.85. These fixed bins are a proxy for surface similarity, not an independent measure of intrinsic difficulty; low similarity can occur for true nonmatches as well as matches.

## Matchers and selection

Baseline: predict match when the title ratio is at least a threshold. The second matcher uses the mean of title and author character-trigram Dice similarities, weighted 0.75 for title and 0.25 for authors. For each field, casefold and collapse whitespace, pad both ends with two spaces, and make a set of character trigrams; Dice is twice the intersection size divided by the sum of set sizes. Two empty field values have similarity zero. No vocabulary is fitted. Predict match when the weighted similarity is at least a threshold.

Choose each threshold independently to maximize positive-class F1 on train over 0.00, 0.01, ..., 1.00 inclusive; break ties in favor of the largest threshold. No test-driven changes or model tuning. The method is deterministic and uses no random sampling (seed 42 is fixed for reproducibility if randomness is introduced).

## Reporting

For each matcher report overall and hard, middle, and easy test pair counts, positive counts and positive rates, plus positive-class precision, recall and F1. Treat a zero denominator as zero. Include chosen train thresholds and discuss slice sizes, class composition, and limits of the similarity proxy. The scores describe these preselected candidate pairs, not all possible cross-table pairs.

## Amendment 1, 2026-11-11

The DBLP-ACM test hard slice has only two positive pairs, too few to estimate hard-slice performance reliably. Extend the evaluation to all three additional DeepMatcher product benchmarks, without selecting among them based on their outcomes: textual Abt-Buy, structured Amazon-Google, and structured Walmart-Amazon. Use each benchmark's supplied train, validation, and test splits; train alone selects thresholds, and each new test split is evaluated once. Report all three alongside DBLP-ACM, whatever the results show.

Use exactly the same normalization, label-independent similarity ratio and fixed difficulty bins, baseline, character-trigram Dice construction, threshold grid and tie rule, and metrics. For Abt-Buy, use `name` as the key title field and title-only trigram Dice (no suitable short second field). For Amazon-Google, use `title` as the key field and `manufacturer` as the second field. For Walmart-Amazon, use `title` and `brand`, respectively. Where a second field is used, retain the 0.75 title / 0.25 second-field weighting. As before, two empty values in a field score zero. Report a cross-dataset summary with overall trigram F1 and each slice's positive count, recall, and F1, in addition to the complete per-dataset tables.

## Amendment 2, 2026-11-11

Register this amendment and commit it before running the new analyses. The earlier two matchers' outcomes are already known; this is an extension, not a claim that these benchmarks have never been inspected. Retain all four datasets, supplied splits, normalization, left-to-right title-ratio bins, existing matchers and their train-selected threshold rules. Recompute their deterministic predictions in the same run to add uncertainty estimates. No test-driven model changes, feature selection, threshold tuning or reruns.

### Learned matcher

Fit one independent `HistGradientBoostingClassifier` per dataset on train pairs only, using scikit-learn 1.7.2 and NumPy 2.3.5. Fix `loss="log_loss"`, `learning_rate=0.1`, `max_iter=200`, `max_leaf_nodes=31`, `max_depth=None`, `min_samples_leaf=20`, `l2_regularization=1.0`, `max_bins=255`, `categorical_features=None`, `early_stopping=False`, `class_weight=None` and `random_state=42`; leave other parameters at that version's defaults. Use one computational thread. This nonlinear learner can combine complementary cheap comparisons without fitting a large text model; no algorithm or hyperparameter comparison will be run.

Every dataset has five title features: character-trigram Dice (as defined above), whitespace-token Jaccard, word TF-IDF cosine, character-length ratio and numeric-token Jaccard. Jaccard is intersection size divided by union size, with an empty union scoring zero. Length ratio is shorter normalized length divided by longer, or zero for two empty titles. Numeric tokens are the set of matches of `\d+(?:\.\d+)?` in the normalized title; two titles without numbers score zero. All text comparisons use the existing casefold/whitespace normalization.

Fit a separate `TfidfVectorizer` on normalized titles of distinct left and right records referenced by TRAIN pairs only (deduplicated by ID within each table, left IDs sorted then right IDs sorted). This is the vocabulary and inverse-document-frequency leakage boundary: do not fit on whole record tables, validation-only records or test-only records. Use word unigrams and bigrams, `token_pattern=r"(?u)\b\w+\b"`, `lowercase=False`, `sublinear_tf=True`, `min_df=1`, `max_df=1.0`, `max_features=50000`, `norm="l2"` and float64 values; other vectorizer parameters retain their defaults. Transform validation and test titles with this frozen vectorizer. Cosine is the sparse dot product of the L2-normalized title vectors; a zero vector scores zero. Shared record IDs across supplied splits are not removed or refitted.

Per-dataset feature lists (no IDs or labels are features):

| Dataset | Title field | Features in addition to the five title features |
|---|---|---|
| DBLP-ACM | title | authors trigram Dice; authors token Jaccard; year equality |
| Abt-Buy | name | description trigram Dice; description token Jaccard; price agreement |
| Amazon-Google | title | manufacturer trigram Dice; manufacturer token Jaccard; price agreement |
| Walmart-Amazon | title | brand trigram Dice; brand token Jaccard; price agreement; modelno equality |

Year equality is one only for equal, present numeric years. Price agreement is the smaller nonnegative price divided by the larger, with two present zero prices scoring one; strip currency dollar signs and commas before numeric conversion. Missing, invalid or nonfinite numeric values score zero. Model-number equality is one only for equal, nonempty normalized values. The text features already define empty-value behavior; no imputation is fitted.

After fitting the classifier on train, select the probability threshold maximizing positive-class F1 on validation, over its distinct predicted probabilities plus 1.0; break ties toward the largest threshold and predict match for probability greater than or equal to it. Do not refit on train plus validation. Only then transform and evaluate test. Existing matchers still select thresholds on train, not validation.

### Bootstrap uncertainty

For every dataset and all three matchers, report overall and hard, middle and easy pair counts, positive counts, positive rates, precision, recall and F1, and 95% percentile bootstrap intervals for recall and F1. Draw 1,000 samples of N test pairs with replacement, where N is the dataset's test-pair count, with a fresh NumPy `default_rng(42)` for each dataset/matcher. Recompute each slice within each full-pair resample; do not stratify by slice or label. Sampling the 12 slice-by-confusion-cell counts from the equivalent multinomial distribution is permitted to avoid allocating resampled pair matrices. Use NumPy's linear 2.5th and 97.5th percentiles. Zero-denominator metrics remain zero, including in resamples.

These are conditional pair-bootstrap intervals, not uncertainty from retraining or resplitting; pairs can share records. A zero-success slice can have a degenerate zero interval, which is not evidence of known population performance. Always put the slice positive count alongside its metrics and flag slices with fewer than 20 positives as insufficient support.

### Difficulty-mix analysis

For each matcher, report all 12 ordered source/target dataset combinations (excluding self-remixes). Keep the source model and threshold fixed; use target labels only to describe its test-set slice mix, never to fit or select a matcher. This is a descriptive standardization, not a prediction of transfer to the target dataset.

For slice s, let source counts be TP_s, FP_s, FN_s and TN_s, with P_s = TP_s + FN_s and Q_s = FP_s + TN_s. Let target test counts be P'_s positives and Q'_s negatives. Set positive weight a_s = P'_s / P_s and negative weight b_s = Q'_s / Q_s. The reweighted counts are TP* = sum_s a_s TP_s, FN* = sum_s a_s FN_s, FP* = sum_s b_s FP_s and TN* = sum_s b_s TN_s. Thus each slice has exactly the target pair count and positive count; multiplying all target counts by a common constant leaves scores unchanged. Compute precision = TP* / (TP* + FP*), recall = TP* / (TP* + FN*) and F1 = 2 TP* / (2 TP* + FP* + FN*), with zero denominators scoring zero.

Require at least 20 SOURCE positives in every slice with nonzero target positive mass, and at least 20 SOURCE negatives in every slice with nonzero target negative mass. Otherwise mark the entire re-mix "not estimable", listing the unsupported source slices and counts; do not omit, pool, smooth or extrapolate those slices. A zero target class mass contributes zero without division. The minimum applies to source performance estimates, not target counts, which specify a fixed descriptive mixture. Report original overall precision/recall/F1 alongside the standardized scores and report the source slice confusion counts and target pair/positive counts. No bootstrap intervals are planned for re-mixes.

### Reporting and acceptance

Run `.venv/bin/python evaluate.py` once for all four datasets after implementation review; no other experiment, test suite, linter or formatter is planned. Print the registered model settings, per-dataset feature names, thresholds, package versions, bootstrap settings, all metric tables, source confusion counts and all re-mixes. Update the existing results and README from that output, including unfavorable findings and non-estimable comparisons.

For the concluding question, call overall F1 at least 0.90 "high". Require at least 20 hard positives and a hard-recall bootstrap upper endpoint below the overall-recall lower endpoint to describe clearly lower hard recall with adequate support. This is a descriptive criterion, not a formal hypothesis test. Do not tune these criteria after seeing results. Explain that title similarity is only a difficulty proxy, the matchers overlap with that signal, candidate pairs are not production traffic, and standardization assumes source within-slice error rates remain fixed.
