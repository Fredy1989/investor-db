"""records_raw/ (výstup rešeršních agentů, beze změn) + corrections.json → records/.

Každá oprava má důvod a autora návrhu (agent_b = ověřovací agent, orchestrator = hlavní session),
takže z gitu i z tohoto souboru je dohledatelné, co a proč se změnilo oproti výstupu agenta A.
Po opravách se spustí přepočet měn (fx.py).

Operace: set (path = tečková cesta, čísla = index v seznamu), append (do seznamu), remove (prvek seznamu).
Použití: python src/apply_corrections.py
"""
import json
import shutil

import fx
from records import ROOT, RECORDS

RAW = ROOT / "data" / "records_raw"
CORR = ROOT / "data" / "corrections.json"


def walk(obj, parts):
    for p in parts:
        obj = obj[int(p)] if isinstance(obj, list) else obj.setdefault(p, {})
    return obj


def apply(rec, c):
    parts = c["path"].split(".")
    parent, last = walk(rec, parts[:-1]), parts[-1]
    if c["op"] == "set":
        if isinstance(parent, list):
            parent[int(last)] = c["value"]
        else:
            parent[last] = c["value"]
    elif c["op"] == "append":
        parent.setdefault(last, []).append(c["value"])
    elif c["op"] == "remove":
        removed = parent.pop(int(last))
        rec.setdefault("removed_evidence", []).append({**removed, "removed_reason": c["reason"]})
    else:
        raise ValueError(c["op"])


def main():
    shutil.rmtree(RECORDS, ignore_errors=True)
    shutil.copytree(RAW, RECORDS)
    with open(CORR, encoding="utf-8") as f:
        corrections = json.load(f)
    by_id = {}
    for c in corrections:
        by_id.setdefault(c["id"], []).append(c)
    for rid, cs in by_id.items():
        path = RECORDS / f"{rid}.json"
        with open(path, encoding="utf-8") as f:
            rec = json.load(f)
        # odebírání od nejvyššího indexu, aby se indexy neposouvaly
        for c in sorted(cs, key=lambda c: (c["op"] == "remove", -int(c["path"].split(".")[-1]) if c["op"] == "remove" else 0)):
            apply(rec, c)
        rec["corrections_applied"] = len(cs)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(rec, f, ensure_ascii=False, indent=2)
    print(f"{len(corrections)} oprav v {len(by_id)} záznamech")
    fx.main()


if __name__ == "__main__":
    main()
