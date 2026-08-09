import json, re, subprocess, difflib, glob

GROUP = {"jmo":("jmo","Junior Mathematical Olympiad"), "cayley":("cayley","Cayley"),
         "hamilton":("hamilton","Hamilton"), "maclaurin":("maclaurin","Maclaurin"),
         "mog":("mog","Mathematical Olympiad for Girls"),
         "bmo":("bmo","BMO Round 1"), "bmo2":("bmo2","BMO Round 2"), "bmo1":("bmo","BMO Round 1")}

# The UKMT free archive mixes both BMO rounds under one slug, so the round is
# read off the paper's own header rather than trusted from the file name.
def round_of(src):
    t = subprocess.run(["pdftotext","-layout","pdf/"+src,"-"],capture_output=True,text=True).stdout[:1200]
    return "bmo2" if re.search(r'Round\s*2', t) else "bmo"

conv = json.load(open("raw-conv.json")) + json.load(open("raw_bmo1-conv.json")) + json.load(open("retry-conv.json"))
html = open("/home/user/Code/mathpuzzles/mathematicat.html").read()
existing = re.findall(r'\{ p: "((?:[^"\\]|\\.)*)"', html)
norm = lambda s: re.sub(r'[^a-z0-9]', '', s.lower())[:200]
seen = [norm(e) for e in existing]

kept, drops = [], []
for q in conv:
    if not q.get("usable"): drops.append((q, q.get("why","")[:60])); continue
    if q.get("topic") == "Geometry": drops.append((q, "geometry")); continue
    p, k = (q.get("p") or "").strip(), (q.get("k") or "").strip()
    if len(p) < 40 or len(k) < 40: drops.append((q, "too short")); continue
    fam = round_of(q["src"]) if q["fam"] == "bmo" else q["fam"]
    gid, label = GROUP[fam]
    y = int(q["year"])
    # BMO rounds are named by season, and the paper is sat in the autumn or the
    # January before the file's year; the other olympiads are sat within it.
    when = f"{y-1}/{str(y)[2:]}" if gid.startswith("bmo") else str(y)
    n = norm(p)
    dup = next((s for s in seen if difflib.SequenceMatcher(None, n, s).ratio() > 0.7), None)
    if dup: drops.append((q, "duplicate of existing bank entry")); continue
    seen.append(n)
    kept.append({"p": p + f" (UKMT {label}, {when}.)", "k": k, "g": gid, "src": q["src"], "label": q["label"], "topic": q.get("topic")})

import collections
print("kept", len(kept), collections.Counter(x["g"] for x in kept))
print("dropped", len(drops), collections.Counter(r for _, r in drops).most_common(8))
json.dump(kept, open("kept.json","w"), indent=1)

j = lambda s: json.dumps(s, ensure_ascii=False)
out = []
for x in kept:
    out.append("  { p: " + j(x["p"]) + ", g: " + j(x["g"]) + ",\n    k: " + j(x["k"]) + " },\n")
open("new_entries.js","w").write("\n".join(out))
print("wrote new_entries.js", len(open('new_entries.js').read()), "bytes")
