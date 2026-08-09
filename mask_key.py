#!/usr/bin/env python3
"""Re-encode the OpenRouter key as the number list mathematicat.html reassembles.

This is scraper avoidance, not secrecy: the key is plainly visible in the
network tab of the published page. Its only job is to leave nothing in the
source with the shape of a credential, so automated harvesters have no pattern
to match on.

    python3 mask_key.py <key>      # prints the block to paste
"""
import sys, textwrap

key = sys.argv[1] if len(sys.argv) > 1 else input("key: ").strip()
nums = [ord(c) ^ ((i * 9 + 17) % 251) for i, c in enumerate(key)]
print("const litter = [")
print(textwrap.fill(", ".join(map(str, nums)), 88, initial_indent="  ", subsequent_indent="  "))
print("];")
