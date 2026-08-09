# Problem import

How the UKMT problems in `BANK` got there, kept so the provenance of any one of
them can be traced back to the paper it came from.

None of this material is in the page any more: the papers are free to download
from UKMT but carry no reuse licence, so the imported problems were removed
again before publishing. The pipeline is kept in case permission ever arrives.

## Stages

1. **Discovery.** `ukmt.org.uk/competition-papers` links only Team Challenge
   PDFs. The olympiad papers live in a WordPress custom post type, enumerable
   at `wp-json/wp/v2/free-past-papers`; the BMO1 markers' reports, which are the
   only free source of BMO1 solutions, are at `bmos.ukmt.org.uk/home/bmo.shtml`.
2. **Download** into `pdf/`, then `pdftotext -layout`. The layout flag keeps the
   column structure that separates a problem from the diagram beside it.
3. **Split** with `split.py` (papers) and `split_report.py` (BMO1 reports).
   Deterministic: strip page furniture, accept a question label only when it is
   the next number in sequence, cut at the `Solution` heading, drop the
   answer-only A sections.
4. **Convert** with `convert.py`. One model call per problem, given the raw
   statement and UKMT's own solution, returning `{usable, topic, p, k}`.
   `pdftotext` renders formulas as Unicode italics with subscripts flattened,
   so `2𝑎𝑖−1` has to be read back as `2a_{i-1}`: that needs comprehension, not
   a regex. The model is told never to invent mathematics and to refuse a
   problem whose solution came out unclear, so it condenses rather than solves.
5. **Emit** with `emit.py`. Drops the unusable and everything topic-tagged
   Geometry, dedupes against the bank already in the page, appends attribution,
   and formats the JS entries.

## Re-running

    python3 split.py && python3 split_report.py
    python3 convert.py raw.json && python3 convert.py raw_bmo1.json
    python3 emit.py                      # writes new_entries.js

`convert.py` reads the OpenRouter key out of `mathematicat.html`, unmasking it
the same way the page does, and bills whatever model is named in `MODEL`.

## Known gaps

- JMO 2015-2019 are scanned pupils' solution booklets, not solution papers, so
  they yield nothing without OCR.
- Geometry is excluded throughout: the page cannot show a diagram.
- The `k` sketches are condensed from official solutions by a model. Two were
  checked line by line against their source PDFs and were faithful; the rest
  are unverified.
