#!/usr/bin/env python3
"""Evaluate two fixed similarity matchers on the benchmark's supplied split."""
import csv
from difflib import SequenceMatcher
import hashlib
import io
import random
import sys
from zipfile import ZipFile

from download import DATASETS, archive_path

random.seed(42)
# Key field, optional second field, archive member prefix.
FIELDS = {
    "dblp-acm": ("title", "authors", "exp_data/"),
    "abt-buy": ("name", None, "exp_data/"),
    "amazon-google": ("title", "manufacturer", ""),
    "walmart-amazon": ("title", "brand", "exp_data/"),
}


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


def metrics(labels, predictions):
    tp = sum(y and p for y, p in zip(labels, predictions))
    fp = sum(not y and p for y, p in zip(labels, predictions))
    fn = sum(y and not p for y, p in zip(labels, predictions))
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return precision, recall, f1


def rows(archive, name, prefix):
    with archive.open(prefix + name + ".csv") as raw:
        return list(csv.DictReader(io.TextIOWrapper(raw, encoding="utf-8", newline="")))


def features(pairs, left, right, key, second):
    result = []
    for pair in pairs:
        a, b = left[pair["ltable_id"]], right[pair["rtable_id"]]
        title = ratio(a[key], b[key])
        score = dice(a[key], b[key])
        if second is not None:
            score = 0.75 * score + 0.25 * dice(a[second], b[second])
        result.append((int(pair["label"]), title, score))
    return result


def choose(data, index):
    labels = [row[0] for row in data]
    return max(range(101), key=lambda t: (metrics(labels, [row[index] >= t / 100 for row in data])[2], t)) / 100


def report(name, data, index, threshold):
    print(f"\n{name} (train threshold {threshold:.2f})")
    print("| Slice | Pairs | Positives | Positive rate | Precision | Recall | F1 |")
    print("|---|---:|---:|---:|---:|---:|---:|")
    groups = [("Overall", lambda r: True), ("Hard", lambda r: r[1] < .60),
              ("Middle", lambda r: .60 <= r[1] < .85), ("Easy", lambda r: r[1] >= .85)]
    for label, belongs in groups:
        subset = [r for r in data if belongs(r)]
        labels = [r[0] for r in subset]
        p, r, f = metrics(labels, [row[index] >= threshold for row in subset])
        rate = sum(labels) / len(labels) if labels else 0.0
        print(f"| {label} | {len(labels)} | {sum(labels)} | {rate:.3f} | {p:.3f} | {r:.3f} | {f:.3f} |")


def main():
    names = sys.argv[1:] or list(DATASETS)
    if any(name not in DATASETS for name in names) or len(set(names)) != len(names):
        raise SystemExit("Provide unique dataset names from: " + ", ".join(DATASETS))
    for name in names:
        key, second, prefix = FIELDS[name]
        path = archive_path(name)
        with path.open("rb") as f:
            if hashlib.sha256(f.read()).hexdigest() != DATASETS[name][1]:
                raise SystemExit(f"{name}: archive SHA-256 mismatch; rerun download.py")
        with ZipFile(path) as archive:
            left = {r["id"]: r for r in rows(archive, "tableA", prefix)}
            right = {r["id"]: r for r in rows(archive, "tableB", prefix)}
            train = features(rows(archive, "train", prefix), left, right, key, second)
            baseline_threshold = choose(train, 1)
            trigram_threshold = choose(train, 2)
            test = features(rows(archive, "test", prefix), left, right, key, second)
        print(f"\n## {name}")
        report("Title ratio baseline", test, 1, baseline_threshold)
        report("Trigram Dice", test, 2, trigram_threshold)


if __name__ == "__main__":
    main()
