import json, re, sys, urllib.request, concurrent.futures as cf

import base64
_html = open('/home/user/Code/mathpuzzles/mathematicat.html').read()
_b64 = re.search(r'unmask\("([^"]+)"\)', _html).group(1)
_P = "mathematicat"
KEY = "".join(chr(c ^ ord(_P[i % len(_P)])) for i, c in enumerate(base64.b64decode(_b64)))
MODEL = sys.argv[2] if len(sys.argv) > 2 else "deepseek/deepseek-v4-flash-0731"

SYSTEM = """You convert UK Mathematics Trust olympiad problems, extracted from PDF, into entries for a proof-practice web app.

The extracted text has mathematics as Unicode italics with subscripts flattened, for example "2𝑎𝑖−1" means 2a_{i-1}. Restore it to LaTeX.

Reply with ONLY a JSON object:
{"usable": true|false, "why": "<short reason when false>", "topic": "Algebra"|"Number Theory"|"Combinatorics"|"Geometry", "p": "<statement>", "k": "<key idea>"}

Set usable to false, and leave p and k empty, when the problem:
- depends on a diagram, figure, grid picture or anything the extracted text cannot convey;
- is geometry that a reader could not attempt without the picture;
- asks only for an answer with no proof required, or splits into lettered parts with mark allocations;
- refers to an answer sheet, or lost essential content in extraction.
Be strict: a problem that is not fully self-contained in your "p" is not usable.

"p" is the problem statement, rewritten to stand alone: British spelling, LaTeX inside $...$ or $$...$$, no question numbering, no mark allocations, no reference to the original paper. Define any term a strong beginner might not know. It must ask for a proof or a justified determination, and it must be answerable from the text alone.

"k" is the key idea: the shortest honest route to a proof, 2 to 5 sentences, condensed from the official solution given to you and faithful to it. It is a sketch a solver could expand, not a full write-up. LaTeX inside $...$.

Never invent mathematics. If the official solution is unclear or truncated, set usable to false."""

def call(q):
    body = json.dumps({"model": MODEL, "temperature": 0, "max_tokens": 40000, "messages": [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": "Competition: " + q["fam"].upper() + " " + q["year"] + ", question " + q["label"]
         + "\n\nExtracted statement:\n" + q["statement"] + "\n\nExtracted official solution:\n" + q["solution"][:6000]}]}).encode()
    r = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=body,
        headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json", "X-Title": "MathematiCat import"})
    try:
        resp = json.loads(urllib.request.urlopen(r, timeout=300).read())["choices"][0]
        txt = resp["message"].get("content") or ""
        if not txt: raise RuntimeError("empty content, finish=" + str(resp.get("finish_reason")))
        m = re.search(r'\{[\s\S]*\}', txt)
        out = json.loads(m.group(0))
    except Exception as e:
        return {**q, "usable": False, "why": "call failed: " + str(e)[:120]}
    return {**q, **out}

raw = json.load(open(sys.argv[1]))
with cf.ThreadPoolExecutor(8) as ex:
    done = list(ex.map(call, raw))
json.dump(done, open(sys.argv[1].replace(".json", "-conv.json"), "w"), indent=1)
ok = [d for d in done if d.get("usable")]
print("in", len(raw), "usable", len(ok), "dropped", len(raw) - len(ok))
for d in done:
    print(("OK  " if d.get("usable") else "DROP"), d["fam"], d["year"], d["label"], "|", (d.get("why") or d.get("topic","") + ": " + d.get("p","")[:90]))
