#!/usr/bin/env python3
"""Download the fixed benchmark archive and verify its bytes."""
import hashlib
from pathlib import Path
from urllib.request import urlopen

URL = "https://pages.cs.wisc.edu/~anhai/data1/deepmatcher_data/Structured/DBLP-ACM/dblp_acm_exp_data.zip"
SHA256 = "a15b752ffc318a714690cf13286d31c2012f686525803ca803c392ceff4aa4f3"

with urlopen(URL, timeout=60) as response:
    data = response.read(100_000_001)
if len(data) > 100_000_000 or hashlib.sha256(data).hexdigest() != SHA256:
    raise SystemExit("Archive too large or SHA-256 mismatch; nothing written")
Path("data").mkdir(exist_ok=True)
Path("data/dblp_acm_exp_data.zip").write_bytes(data)
print("Downloaded and verified data/dblp_acm_exp_data.zip")
