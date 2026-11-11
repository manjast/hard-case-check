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
