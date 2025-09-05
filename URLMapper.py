#!/usr/bin/env python3
import sys, re
HREF = re.compile(r'href="([^"]*)"')
for line in sys.stdin:
    for url in HREF.findall(line):
        sys.stdout.write(f"{url}\t1\n")
