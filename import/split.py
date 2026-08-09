import re, json, glob, subprocess, os

NOISE = re.compile(r'(©\s*\d*\s*UK Mathematics Trust|www\.ukmt\.org\.uk|^\s*Solutions\s*$|Mathematical Olympiad.*(paper|Solutions)|British Mathematical Olympiad|Junior Mathematical Olympiad|Olympiad for Girls|United Kingdom|Mathematics Trust|^\s*U?K?\s*MT\s*$|^\s*\d+\s*$)', re.I)
# Labels are 1., 2., ... on the modern papers and A1./B1. on the older JMO ones,
# where the A section is short-answer and only the B section wants a proof.
LABEL = re.compile(r'\s{0,10}([AB]?)(\d{1,2})\.\s+(\S.*)')
SOLUTION = re.compile(r'\n\s*Solution[.:]?\s')

def split(pdf):
    raw = subprocess.run(["pdftotext","-layout",pdf,"-"],capture_output=True,text=True).stdout
    lines = [l for l in raw.split("\n") if not NOISE.search(l)]
    out, want, cur = [], {"": 1, "A": 1, "B": 1}, None
    for l in lines:
        m = LABEL.match(l)
        if m and int(m.group(2)) == want[m.group(1)]:
            cur and out.append(cur)
            cur = {"label": m.group(1) + m.group(2), "sec": m.group(1), "lines": [m.group(3)]}
            want[m.group(1)] += 1
        elif cur is not None:
            cur["lines"].append(l)
    cur and out.append(cur)
    keep = []
    for q in out:
        blob = "\n".join(q.pop("lines"))
        parts = SOLUTION.split(blob, maxsplit=1)
        q["statement"] = re.sub(r'[ \t]+\n', '\n', parts[0]).strip()
        q["solution"] = (parts[1] if len(parts) > 1 else "").strip()
        # A-section questions are answer-only, so they cannot be graded as proofs.
        q["sec"] != "A" and q["solution"] and len(q["statement"]) > 40 and keep.append(q)
    return keep

bank = []
for f in sorted(glob.glob("pdf/*.pdf")):
    fam, year = os.path.basename(f).split("-")[:2]
    qs = split(f)
    for q in qs: q.update(fam=fam, year=year, src=os.path.basename(f))
    bank += qs
    print(f"{os.path.basename(f):26s} {len(qs)}")
json.dump(bank, open("raw.json","w"), indent=1)
import collections
print("TOTAL", len(bank), collections.Counter(q["fam"] for q in bank))
