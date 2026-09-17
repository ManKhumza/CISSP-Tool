"""Validation: agreement, disagreements sample, and per-section sanity."""
import json, os, glob, random, sys
from collections import Counter

BASE = r"C:\Users\Khumza\Documents\Coding projects\CISSP"
OUT = os.path.join(BASE, "_classify")
sys.path.insert(0, BASE)
from dataio import load_bank, section_list

DATA, Q, SEC, DNAME = load_bank()
SECLIST = section_list(DATA)

base = {int(k): v["section"] for k, v in json.load(open(OUT + r"\assignments.json", encoding="utf-8")).items()}
final = {int(k): v["section"] for k, v in json.load(open(OUT + r"\final_assignments.json", encoding="utf-8")).items()}

merged = {}
for fp in sorted(glob.glob(OUT + r"\out\out_*.json")):
    for k, v in json.load(open(fp, encoding="utf-8")).items():
        try: merged[int(k)] = str(v).strip()
        except ValueError: pass

agree = sum(1 for qn, lab in merged.items() if base.get(qn) == lab)
print(f"LLM adjudicated labels      : {len(merged)}")
print(f"agreement with rule labels  : {agree}/{len(merged)} ({agree/max(len(merged),1)*100:.1f}%)")
print(f"general bucket (final)      : {sum(1 for v in final.values() if v=='general')}/{len(final)}")

dis = [(qn, base.get(qn), lab) for qn, lab in merged.items() if base.get(qn) != lab]
random.seed(5)
print("\n" + "=" * 104)
print("RANDOM DISAGREEMENTS — rule label first, LLM label second (which is right?)")
print("=" * 104)
for qn, r, l in random.sample(dis, min(22, len(dis))):
    rt = SEC.get(r, ("Other",))[0][:34]
    lt = SEC.get(l, ("Other",))[0][:34]
    print(f"Q{qn}: rules {r} ({rt})  |  llm {l} ({lt})")
    print(f"      {Q[qn]['q'][:140]}")

print("\n" + "=" * 104)
print("PER-SECTION COUNTS (final)")
print("=" * 104)
cnt = Counter(final.values())
for did, rows in SECLIST.items():
    parts = [f"{sid}:{cnt.get(sid,0)}" for sid, _ in rows]
    print(f"D{did}: " + "  ".join(parts))
tot = sum(cnt.values())
print(f"total labelled: {tot}")
