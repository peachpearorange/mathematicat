import re, json, glob, subprocess, os
NOISE = re.compile(r'(©\s*\d*\s*UK Mathematics Trust|www\.ukmt\.org\.uk|Markers.{0,3} report|British Mathematical Olympiad Round \d+ \d{4}|^\s*\d+\s*$)', re.I)
SOLUTION = re.compile(r'\n\s*Solution[.:]?\s')

def split(pdf):
    raw = subprocess.run(["pdftotext","-layout",pdf,"-"],capture_output=True,text=True).stdout
    lines = [l for l in raw.split("\n") if not NOISE.search(l)]
    out, want, cur = [], 1, None
    for l in lines:
        m = re.match(r'\s*Question\s+(\d+)\s*$', l)
        if m and int(m.group(1)) == want:
            cur and out.append(cur); cur = {"label": str(want), "lines": []}; want += 1
        elif cur is not None: cur["lines"].append(l)
    cur and out.append(cur)
    keep = []
    for q in out:
        parts = SOLUTION.split("\n".join(q.pop("lines")), maxsplit=1)
        q["statement"] = re.sub(r'[ \t]+\n','\n',parts[0]).strip()
        q["solution"] = (parts[1] if len(parts) > 1 else "").strip()
        # The markers' commentary trails each solution; the grader never sees it.
        q["solution"] = re.split(r'\n\s*(This question|Most candidates|Candidates|The vast majority)', q["solution"])[0].strip()
        q["solution"] and len(q["statement"]) > 40 and keep.append(q)
    return keep

bank = []
for f in sorted(glob.glob("pdf/bmo1r-*.pdf")):
    year = os.path.basename(f).split("-")[1]
    qs = split(f)
    for q in qs: q.update(fam="bmo1", year=year, src=os.path.basename(f))
    bank += qs
    print(os.path.basename(f), len(qs))
json.dump(bank, open("raw_bmo1.json","w"), indent=1)
print("TOTAL", len(bank))
