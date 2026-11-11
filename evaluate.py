#!/usr/bin/env python3
"""Run the matching, bootstrap and mix analyses in docs/protocol.md."""
import os

# Bound native-library threads before importing NumPy or scikit-learn.
for variable in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "BLIS_NUM_THREADS"):
    os.environ[variable] = "1"

import csv
from dataclasses import dataclass
from difflib import SequenceMatcher
import hashlib
from importlib.metadata import version
import io
import math
import re
import sys
from zipfile import ZipFile

import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from threadpoolctl import threadpool_limits

from download import DATASETS, archive_path

FIELDS = {
    "dblp-acm": ("title", "authors", "exp_data/"),
    "abt-buy": ("name", None, "exp_data/"),
    "amazon-google": ("title", "manufacturer", ""),
    "walmart-amazon": ("title", "brand", "exp_data/"),
}
EXTRA_FIELDS = {
    "dblp-acm": ("authors", "year"),
    "abt-buy": ("description", "price"),
    "amazon-google": ("manufacturer", "price"),
    "walmart-amazon": ("brand", "price"),
}
MODEL_SETTINGS = dict(
    loss="log_loss", learning_rate=0.1, max_iter=200, max_leaf_nodes=31,
    max_depth=None, min_samples_leaf=20, l2_regularization=1.0, max_bins=255,
    categorical_features=None, early_stopping=False, class_weight=None, random_state=42,
)
SLICES = ("Hard", "Middle", "Easy")
MATCHERS = ("Title ratio", "Trigram Dice", "Learned")
BOOTSTRAPS = 1000
MIN_SUPPORT = 20
SEED = 42


@dataclass(frozen=True)
class PairData:
    labels: np.ndarray
    title: np.ndarray
    trigram: np.ndarray
    learned: np.ndarray


@dataclass(frozen=True)
class Evaluation:
    threshold: float
    selection: str
    counts: np.ndarray
    values: np.ndarray
    intervals: np.ndarray


def normalize(value):
    return " ".join(value.casefold().split())


def ratio(a, b):
    return SequenceMatcher(None, normalize(a), normalize(b), autojunk=False).ratio()


def dice(a, b):
    a, b = normalize(a), normalize(b)
    if not a and not b:
        return 0.0
    def grams(s):
        s = "  " + s + "  "
        return {s[i:i + 3] for i in range(len(s) - 2)}
    x, y = grams(a), grams(b)
    return 2 * len(x & y) / (len(x) + len(y))


def jaccard(a, b):
    union = a | b
    return len(a & b) / len(union) if union else 0.0


def number(value):
    try:
        parsed = float(value.replace("$", "").replace(",", ""))
    except ValueError:
        return None
    return parsed if math.isfinite(parsed) else None


def numeric_agreement(a, b, field):
    a, b = number(a), number(b)
    if a is None or b is None:
        return 0.0
    if field == "year":
        return float(a == b)
    if min(a, b) < 0:
        return 0.0
    return min(a, b) / max(a, b) if max(a, b) else 1.0


def feature_names(name):
    text, numeric = EXTRA_FIELDS[name]
    names = [
        "title trigram Dice", "title token Jaccard", "title TF-IDF cosine",
        "title length ratio", "title numeric-token Jaccard",
        f"{text} trigram Dice", f"{text} token Jaccard",
        "year equality" if numeric == "year" else "price agreement",
    ]
    if name == "walmart-amazon":
        names.append("modelno equality")
    return names


def fit_vectorizer(train, left, right, key):
    # Only train-referenced records enter either the vocabulary or IDF fit.
    corpus = [
        normalize(table[record_id][key])
        for table, column in ((left, "ltable_id"), (right, "rtable_id"))
        for record_id in sorted({pair[column] for pair in train})
    ]
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2), token_pattern=r"(?u)\b\w+\b", lowercase=False,
        sublinear_tf=True, min_df=1, max_df=1.0, max_features=50000,
        norm="l2", dtype=np.float64,
    )
    vectorizer.fit(corpus)
    return vectorizer


def features(pairs, left, right, name, vectorizer):
    key, second, _ = FIELDS[name]
    text, numeric = EXTRA_FIELDS[name]
    records = [(left[p["ltable_id"]], right[p["rtable_id"]]) for p in pairs]
    titles_a = [normalize(a[key]) for a, _ in records]
    titles_b = [normalize(b[key]) for _, b in records]
    # Row-aligned sparse products, never an all-pairs or dense vocabulary matrix.
    cosine = np.asarray(
        vectorizer.transform(titles_a).multiply(vectorizer.transform(titles_b)).sum(axis=1)
    ).ravel()
    title_scores, trigram_scores, learned = [], [], []
    for i, (a, b) in enumerate(records):
        ta, tb = titles_a[i], titles_b[i]
        title_dice = dice(ta, tb)
        title_scores.append(ratio(ta, tb))
        trigram_scores.append(
            title_dice if second is None
            else 0.75 * title_dice + 0.25 * dice(a[second], b[second])
        )
        longer = max(len(ta), len(tb))
        values = [
            title_dice, jaccard(set(ta.split()), set(tb.split())), cosine[i],
            min(len(ta), len(tb)) / longer if longer else 0.0,
            jaccard(set(re.findall(r"\d+(?:\.\d+)?", ta)), set(re.findall(r"\d+(?:\.\d+)?", tb))),
            dice(a[text], b[text]),
            jaccard(set(normalize(a[text]).split()), set(normalize(b[text]).split())),
            numeric_agreement(a[numeric], b[numeric], numeric),
        ]
        if name == "walmart-amazon":
            ma, mb = normalize(a["modelno"]), normalize(b["modelno"])
            values.append(float(bool(ma) and ma == mb))
        learned.append(values)
    return PairData(
        np.array([int(p["label"]) for p in pairs], dtype=bool),
        np.array(title_scores), np.array(trigram_scores), np.array(learned),
    )


def divide(numerator, denominator):
    return np.divide(
        numerator, denominator, out=np.zeros_like(numerator, dtype=float),
        where=denominator != 0,
    )


def metrics(counts):
    tp, fp, fn, tn = np.moveaxis(np.asarray(counts), -1, 0)
    return np.stack((
        divide(tp, tp + fp), divide(tp, tp + fn), divide(2 * tp, 2 * tp + fp + fn),
    ), axis=-1)


def choose(labels, scores, candidates):
    def objective(threshold):
        predictions = scores >= threshold
        tp = np.count_nonzero(labels & predictions)
        fp = np.count_nonzero(~labels & predictions)
        fn = np.count_nonzero(labels & ~predictions)
        # Preserve the existing matchers' floating-point threshold objective.
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        return (f1, threshold)
    return float(max(candidates, key=objective))


def evaluate(data, scores, threshold, selection):
    predictions = scores >= threshold
    slices = np.where(data.title < 0.60, 0, np.where(data.title < 0.85, 1, 2))
    cells = np.where(predictions, np.where(data.labels, 0, 1), np.where(data.labels, 2, 3))
    counts = np.bincount(4 * slices + cells, minlength=12).reshape(3, 4)
    total = int(counts.sum())
    samples = np.random.default_rng(SEED).multinomial(
        total, counts.ravel() / total, size=BOOTSTRAPS,
    ).reshape(BOOTSTRAPS, 3, 4)
    all_samples = np.concatenate((samples.sum(axis=1, keepdims=True), samples), axis=1)
    intervals = np.quantile(
        metrics(all_samples)[:, :, 1:], [0.025, 0.975], axis=0, method="linear",
    )
    all_counts = np.vstack((counts.sum(axis=0), counts))
    return Evaluation(threshold, selection, all_counts, metrics(all_counts), intervals)


def rows(archive, name, prefix):
    with archive.open(prefix + name + ".csv") as raw:
        return list(csv.DictReader(io.TextIOWrapper(raw, encoding="utf-8", newline="")))


def run_dataset(name):
    key, _, prefix = FIELDS[name]
    path = archive_path(name)
    if hashlib.sha256(path.read_bytes()).hexdigest() != DATASETS[name][1]:
        raise SystemExit(f"{name}: archive SHA-256 mismatch; rerun download.py")
    with ZipFile(path) as archive:
        left = {r["id"]: r for r in rows(archive, "tableA", prefix)}
        right = {r["id"]: r for r in rows(archive, "tableB", prefix)}
        train_pairs = rows(archive, "train", prefix)
        vectorizer = fit_vectorizer(train_pairs, left, right, key)
        train = features(train_pairs, left, right, name, vectorizer)
        grid = [t / 100 for t in range(101)]
        thresholds = [
            choose(train.labels, train.title, grid),
            choose(train.labels, train.trigram, grid),
        ]
        model = HistGradientBoostingClassifier(**MODEL_SETTINGS)
        model.fit(train.learned, train.labels)
        valid_pairs = rows(archive, "valid", prefix)
        valid = features(valid_pairs, left, right, name, vectorizer)
        valid_scores = model.predict_proba(valid.learned)[:, 1]
        thresholds.append(choose(valid.labels, valid_scores, np.unique(np.append(valid_scores, 1.0))))
        # No test features or predictions are computed until all thresholds are fixed.
        test = features(rows(archive, "test", prefix), left, right, name, vectorizer)
        scores = (test.title, test.trigram, model.predict_proba(test.learned)[:, 1])
        results = {
            matcher: evaluate(test, score, threshold, "validation" if matcher == "Learned" else "train")
            for matcher, score, threshold in zip(MATCHERS, scores, thresholds)
        }
    print(f"\n### {name}")
    print(f"\nTrain pairs: {len(train_pairs)}; validation pairs: {len(valid_pairs)}; "
          f"train-only TF-IDF vocabulary: {len(vectorizer.vocabulary_)} terms.")
    print("\nLearned features: " + "; ".join(feature_names(name)) + ".")
    for matcher, result in results.items():
        report(matcher, result)
    return results


def interval(result, row, metric):
    lower, upper = result.intervals[:, row, metric - 1]
    return f"{result.values[row, metric]:.3f} [{lower:.3f}, {upper:.3f}]"


def report(matcher, result):
    print(f"\n#### {matcher}")
    print(f"\n{result.selection.capitalize()}-selected threshold: {result.threshold:.17g}.")
    print("\n| Slice | Pairs | Positives | Positive rate | Precision | Recall [95% interval] | F1 [95% interval] | Support |")
    print("|---|---:|---:|---:|---:|---:|---:|---|")
    for i, label in enumerate(("Overall",) + SLICES):
        tp, fp, fn, tn = result.counts[i]
        pairs, positives = int(tp + fp + fn + tn), int(tp + fn)
        support = "insufficient (<20 positives)" if positives < MIN_SUPPORT else "at least 20 positives"
        print(f"| {label} | {pairs} | {positives} | {positives / pairs if pairs else 0:.3f} | "
              f"{result.values[i, 0]:.3f} | {interval(result, i, 1)} | {interval(result, i, 2)} | {support} |")


def remix(source, target):
    weighted = np.zeros(4)
    unsupported = []
    for label, source_counts, target_counts in zip(SLICES, source.counts[1:], target.counts[1:]):
        for indices, class_name in (((0, 2), "positives"), ((1, 3), "negatives")):
            source_mass = source_counts[list(indices)].sum()
            target_mass = target_counts[list(indices)].sum()
            if target_mass == 0:
                continue
            if source_mass < MIN_SUPPORT:
                unsupported.append(f"{label.lower()} {class_name}={source_mass}")
            else:
                weighted[list(indices)] += source_counts[list(indices)] * target_mass / source_mass
    return (None, "; ".join(unsupported)) if unsupported else (metrics(weighted), "estimable")


def summaries(results):
    print("\n## Cross-dataset summary")
    print("\n| Dataset | Matcher | Overall F1 [95% interval] | Overall recall [95% interval] | Hard positives | Hard recall [95% interval] | Hard F1 [95% interval] | High F1 and supported recall gap |")
    print("|---|---|---:|---:|---:|---:|---:|---|")
    for name, matchers in results.items():
        for matcher, result in matchers.items():
            positives = int(result.counts[1, 0] + result.counts[1, 2])
            qualifies = (
                result.values[0, 2] >= 0.90 and positives >= MIN_SUPPORT
                and result.intervals[1, 1, 0] < result.intervals[0, 0, 0]
            )
            print(f"| {name} | {matcher} | {interval(result, 0, 2)} | {interval(result, 0, 1)} | "
                  f"{positives} | {interval(result, 1, 1)} | {interval(result, 1, 2)} | {'yes' if qualifies else 'no'} |")
    print("\n### All-slice cross-dataset summary")
    print("\nEach slice cell reports positives / recall [95% interval] / F1 [95% interval].")
    print("\n| Dataset | Matcher | Hard | Middle | Easy |")
    print("|---|---|---:|---:|---:|")
    for name, matchers in results.items():
        for matcher, result in matchers.items():
            cells = [
                f"{result.counts[i, 0] + result.counts[i, 2]} / "
                f"{interval(result, i, 1)} / {interval(result, i, 2)}"
                for i in range(1, 4)
            ]
            print(f"| {name} | {matcher} | " + " | ".join(cells) + " |")
    print("\n## Difficulty-mix analysis")
    print("\n### Observed mix (target counts)")
    print("\n| Dataset | Slice | Pairs | Positives | Negatives |")
    print("|---|---|---:|---:|---:|")
    for name, matchers in results.items():
        for label, counts in zip(SLICES, matchers[MATCHERS[0]].counts[1:]):
            print(f"| {name} | {label} | {counts.sum()} | {counts[0] + counts[2]} | {counts[1] + counts[3]} |")
    print("\n### Source slice confusion counts")
    print("\n| Dataset | Matcher | Slice | TP | FP | FN | TN |")
    print("|---|---|---|---:|---:|---:|---:|")
    for name, matchers in results.items():
        for matcher, result in matchers.items():
            for label, counts in zip(SLICES, result.counts[1:]):
                print(f"| {name} | {matcher} | {label} | " + " | ".join(map(str, counts)) + " |")
    print("\n### Reweighted overall scores")
    print("\nEach original and reweighted score cell is precision / recall / F1. "
          "Not estimable means a source slice/class fails the registered minimum of 20. "
          "Target counts specify a fixed mix, not target performance. No model is retrained.")
    print("\n| Source | Target mix | Matcher | Original precision / recall / F1 | Reweighted precision / recall / F1 | Status |")
    print("|---|---|---|---:|---:|---|")
    for source_name, matchers in results.items():
        for target_name, target_matchers in results.items():
            if source_name == target_name:
                continue
            for matcher, source in matchers.items():
                values, status = remix(source, target_matchers[matcher])
                original = " / ".join(f"{v:.3f}" for v in source.values[0])
                reweighted = "not estimable" if values is None else " / ".join(f"{v:.3f}" for v in values)
                print(f"| {source_name} | {target_name} | {matcher} | {original} | {reweighted} | {status} |")


def main():
    names = sys.argv[1:] or list(DATASETS)
    if any(name not in DATASETS for name in names) or len(set(names)) != len(names):
        raise SystemExit("Provide unique dataset names from: " + ", ".join(DATASETS))
    print("## Run settings")
    print("\n" + "; ".join(f"{package} {version(package)}" for package in (
        "numpy", "scikit-learn", "scipy", "joblib", "threadpoolctl", "cloudpickle",
    )) + f"; Python {sys.version.split()[0]}.")
    print(f"\nHistGradientBoostingClassifier settings: `{MODEL_SETTINGS}`.")
    print(f"\nOne native-library thread; seed {SEED}; {BOOTSTRAPS} full-test-pair bootstrap "
          "resamples via slice/confusion-cell multinomial counts; linear 95% percentile intervals.")
    print("\nTF-IDF vocabulary and IDF fitted only on train-referenced records; classifier fitted "
          "only on train; learned threshold selected on validation, existing thresholds on train.")
    print("\nHigh F1 means at least 0.90; a supported recall gap requires at least 20 hard positives "
          "and hard-recall upper interval below overall-recall lower interval.")
    print("\n## Matcher performance and bootstrap uncertainty")
    with threadpool_limits(limits=1):
        results = {name: run_dataset(name) for name in names}
    summaries(results)


if __name__ == "__main__":
    main()
