#!/usr/bin/env python3
"""Evaluate two fixed similarity matchers on the benchmark's supplied split."""
import csv
from difflib import SequenceMatcher
import hashlib
import io
import random
from zipfile import ZipFile

random.seed(42)
ARCHIVE = "data/dblp_acm_exp_data.zip"
SHA256 = "a15b752ffc318a714690cf13286d31c2012f686525803ca803c392ceff4aa4f3"


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


def rows(archive, name):
    with archive.open("exp_data/" + name + ".csv") as raw:
        return list(csv.DictReader(io.TextIOWrapper(raw, encoding="utf-8", newline="")))


def features(pairs, left, right):
    result = []
    for pair in pairs:
        a, b = left[pair["ltable_id"]], right[pair["rtable_id"]]
        title = ratio(a["title"], b["title"])
        score = 0.75 * dice(a["title"], b["title"]) + 0.25 * dice(a["authors"], b["authors"])
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
    with open(ARCHIVE, "rb") as f:
        if hashlib.sha256(f.read()).hexdigest() != SHA256:
            raise SystemExit("Archive SHA-256 mismatch; rerun download.py")
    with ZipFile(ARCHIVE) as archive:
        left = {r["id"]: r for r in rows(archive, "tableA")}
        right = {r["id"]: r for r in rows(archive, "tableB")}
        train = features(rows(archive, "train"), left, right)
        baseline_threshold = choose(train, 1)
        trigram_threshold = choose(train, 2)
        test = features(rows(archive, "test"), left, right)
    report("Title ratio baseline", test, 1, baseline_threshold)
    report("Title/author trigram Dice", test, 2, trigram_threshold)


if __name__ == "__main__":
    main()
