import json, random, sys
BASE = r"C:\Users\Khumza\Documents\Coding projects\CISSP"
sys.path.insert(0, BASE)
from dataio import load_bank, section_list

DATA, Q, SEC, DNAME = load_bank()
SECLIST = section_list(DATA)
F = {int(k): v["section"] for k, v in json.load(
    open(BASE + r"\_classify\final_assignments.json", encoding="utf-8")).items()}

TITLE = {sid: t for did, rows in SECLIST.items() for sid, t in rows}
TITLE["general"] = "Other topics in the domain"

def show(sids, per=10, seed=None):
    random.seed(seed)
    for sid in sids:
        members = sorted(n for n, s in F.items() if s == sid)
        print("\n" + "=" * 104)
        print(f"{sid}  {TITLE.get(sid, sid)}   [{len(members)} questions]")
        print("=" * 104)
        if not members:
            print("  (none)")
            continue
        for n in random.sample(members, min(per, len(members))):
            print(f"  Q{n}: {Q[n]['q'][:145]}")

if __name__ == "__main__":
    show(sys.argv[1:] or ["3.4", "3.6", "5.4", "7.4"])
