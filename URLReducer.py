#!/usr/bin/env python3
import sys
cur, total = None, 0

def flush():
    if cur is not None and total > 5:
        sys.stdout.write(f"{cur}\t{total}\n")

for raw in sys.stdin:
    line = raw.strip()
    if not line:
        continue
    try:
        url, cnt = line.split("\t", 1); cnt = int(cnt)
    except ValueError:
        continue
    if url == cur:
        total += cnt
    else:
        flush(); cur, total = url, cnt
flush()