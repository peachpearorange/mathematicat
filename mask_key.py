#!/usr/bin/env python3
"""Fold an OpenRouter key into the blob that mathematicat.html unmasks at runtime.

This is scraper avoidance, not secrecy: anyone who opens the network tab sees the
key in the Authorization header. Its only job is to keep the provider's key
prefix, and any variable name resembling one, out of the served HTML, since
that is what automated harvesters grep for.

    python3 mask_key.py <key>      # prints the line to paste
"""
import base64, sys

PASS = "mathematicat"
key = sys.argv[1] if len(sys.argv) > 1 else input("key: ").strip()
masked = base64.b64encode(bytes(c ^ ord(PASS[i % len(PASS)]) for i, c in enumerate(key.encode()))).decode()
print('const credential = unmask("' + masked + '");')
