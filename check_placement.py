import json, sys
sys.path.insert(0, r"C:\Users\Khumza\Documents\Coding projects\CISSP")
from dataio import load_bank
DATA, Q, SEC, DNAME = load_bank()
F = {int(k): v["section"] for k, v in json.load(
    open(r"C:\Users\Khumza\Documents\Coding projects\CISSP\_classify\final_assignments.json",
         encoding="utf-8")).items()}
for qn in [777, 827, 1396, 1407, 1476, 1509, 1668, 513, 624, 683, 817, 842, 852, 2088, 2103]:
    if qn in Q:
        print("Q%-5s %-9s %s" % (qn, F.get(qn), Q[qn]["q"][:105]))
