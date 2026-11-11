#!/usr/bin/env python3
"""Download fixed benchmark archives and verify their bytes."""
import hashlib
from pathlib import Path
import sys
from urllib.request import urlopen

BASE = "https://pages.cs.wisc.edu/~anhai/data1/deepmatcher_data/"
DATASETS = {
    "dblp-acm": ("Structured/DBLP-ACM/dblp_acm_exp_data.zip", "a15b752ffc318a714690cf13286d31c2012f686525803ca803c392ceff4aa4f3"),
    "abt-buy": ("Textual/Abt-Buy/abt_buy_exp_data.zip", "cd806d925aca21e6ab942b239353a10ee88904c59d3d3e3da6a74e364e9200a1"),
    "amazon-google": ("Structured/Amazon-Google/amazon_google_exp_data.zip", "9b19c85c98c6289f38969e4961cb944bdf986123fc42f6bf17283ac6eb502e61"),
    "walmart-amazon": ("Structured/Walmart-Amazon/walmart_amazon_exp_data.zip", "d6604b0562c2ef3afec8186d7b43e8bdd82d68325bb98b75bbd01f468d4aa57e"),
}


def archive_path(name):
    return Path("data") / (name + ".zip")


def main():
    names = sys.argv[1:] or list(DATASETS)
    if any(name not in DATASETS for name in names):
        raise SystemExit("Dataset must be one of: " + ", ".join(DATASETS))
    Path("data").mkdir(exist_ok=True)
    for name in names:
        url, checksum = DATASETS[name]
        with urlopen(BASE + url, timeout=60) as response:
            data = response.read(100_000_001)
        if len(data) > 100_000_000 or hashlib.sha256(data).hexdigest() != checksum:
            raise SystemExit(f"{name}: archive too large or SHA-256 mismatch; nothing written")
        archive_path(name).write_bytes(data)
        print(f"Downloaded and verified {archive_path(name)}")


if __name__ == "__main__":
    main()
