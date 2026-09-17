"""
Build batches of UNCERTAIN questions for LLM adjudication:
  * the whole 'general' bucket
  * assignments with a small margin or a low score
Each batch is a JSON file a subagent can read; it must write back a mapping.
"""
import json, os
BASE = r"C:\Users\Khumza\Documents\Coding projects\CISSP"
OUT = os.path.join(BASE, "_classify")
BATCH = os.path.join(OUT, "batches")
os.makedirs(BATCH, exist_ok=True)
os.makedirs(os.path.join(OUT, "out"), exist_ok=True)

src = open(BASE + r"\cissp-data.js", encoding="utf-8-sig").read()
src = src[len("window.CISSP_DATA = "):].rstrip().rstrip(";")
DATA = json.loads(src)
A = {int(k): v for k, v in json.load(open(OUT + r"\assignments.json", encoding="utf-8")).items()}

Q = {}
for d in DATA["domains"]:
    for q in d["questions"]:
        Q[q["n"]] = (d["id"], q)

sections = []
for d in DATA["domains"]:
    for s in d["sections"]:
        sections.append({"id": s["id"], "title": s["title"], "domain": d["id"]})

# ---- choose uncertain questions ----
uncertain = []
for n, a in A.items():
    if a["section"] == "general":
        uncertain.append(n)
    elif a["score"] < 15 or a["margin"] < 3:
        uncertain.append(n)
uncertain.sort()

items = []
for n in uncertain:
    did, q = Q[n]
    a = A[n]
    items.append({
        "n": n,
        "domain_hint": a["domain"],
        "current": a["section"],
        "question": q["q"][:600],
        "options": [f"{o[0]}. {o[1][:160]}" for o in q["o"]],
        "answer": q["a"],
        "explanation": (q["e"] or "")[:200],
    })

SIZE = 120
batches = [items[i:i + SIZE] for i in range(0, len(items), SIZE)]
for i, b in enumerate(batches, 1):
    json.dump(b, open(os.path.join(BATCH, f"batch_{i}.json"), "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)

json.dump(sections, open(os.path.join(OUT, "sections.json"), "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)

print(f"uncertain questions: {len(items)}")
print(f"batches: {len(batches)}  (sizes: {[len(b) for b in batches]})")
print("wrote _classify/batches/batch_N.json and _classify/sections.json")
print("range of question numbers:", min(uncertain), "-", max(uncertain))
