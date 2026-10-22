"""Měření přesnosti vzorku — tři oddělená čísla, aby se nemíchala:

  A) Surový výstup rešeršního agenta (records_raw), měřeno ověřovacím agentem B na VŠECH záznamech.
     → kolik chyb dělá samotná AI rešerše.
  B) Finální data (records po opravách), měřeno ČLOVĚKEM na náhodném vzorku z data/manual_check.csv.
     → přesnost toho, co se odevzdává. Agent B to měřit nemůže, protože opravy sám navrhl.
  C) Shoda agenta B s člověkem na polích, která se po ověření neměnila.
     → nakolik se dá ověřovacímu agentovi věřit při škálování (kde člověk zkontroluje jen vzorek).

Verdikty: ok, wrong, unverifiable, null_ok, null_missed.
  přesnost = ok / (ok + wrong) — jen vyplněná pole, která šlo ověřit
Výstup: data/accuracy.csv + souhrn na stdout.
Použití: python src/measure.py
"""
import csv
import json
from collections import Counter
from pathlib import Path

from records import ROOT

DATA = ROOT / "data"
FIELDS = ["decision", "investor_type", "registry", "sectors", "stages", "ticket", "capital", "investment_evidence"]


def read_csv(path):
    if not Path(path).exists():
        return []
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def norm_field(f):
    f = (f or "").strip()
    return "investment_evidence" if f.startswith("investment_evidence") else f


def precision(c):
    checked = c["ok"] + c["wrong"]
    return (c["ok"] / checked) if checked else None


def pct(x):
    return "" if x is None else f"{x:.0%}"


def raw_decisions():
    out = {}
    for p in (DATA / "records_raw").glob("*.json"):
        with open(p, encoding="utf-8") as f:
            r = json.load(f)
        out[r["id"]] = r.get("decision")
    return out


def main():
    rows = []

    # A) surový výstup agenta A podle agenta B
    decisions = raw_decisions()
    b = {}
    for p in sorted((DATA / "verification").glob("*.csv")):
        for row in read_csv(p):
            b[(row["id"].strip(), norm_field(row["field"]))] = row["verdict"].strip().lower()
    print("A) Surový výstup rešeršního agenta, ověřeno agentem B (všech 29 záznamů)")
    print(f"   {'pole':<20} {'ok':>3} {'chyba':>5} {'neov.':>5} {'null_ok':>7} {'null_miss':>9} {'přesnost':>9}")
    for field in FIELDS:
        c = Counter(v for (rid, f), v in b.items() if f == field and decisions.get(rid) == "include")
        rows.append({"measure": "A_raw_by_agent_b", "field": field, **{k: c[k] for k in
                     ("ok", "wrong", "unverifiable", "null_ok", "null_missed")}, "precision": pct(precision(c))})
        print(f"   {field:<20} {c['ok']:>3} {c['wrong']:>5} {c['unverifiable']:>5} {c['null_ok']:>7} "
              f"{c['null_missed']:>9} {pct(precision(c)):>9}")
    inc = [rid for rid, d in decisions.items() if d == "include"]
    good = [rid for rid in inc if b.get((rid, "decision")) == "ok" and b.get((rid, "investor_type")) == "ok"]
    fields = Counter(v for (rid, f), v in b.items() if decisions.get(rid) == "include"
                     and f not in ("decision", "investor_type"))
    excl = [rid for rid, d in decisions.items() if d != "include"]
    excl_ok = [rid for rid in excl if b.get((rid, "decision")) == "ok"]
    print(f"   přesnost záznamu (zařazen správně a typ sedí): {len(good)}/{len(inc)} = {len(good) / len(inc):.0%}")
    print(f"   správně vyřazené / neaktivní:                 {len(excl_ok)}/{len(excl)}")
    print(f"   přesnost vyplněných polí:                     {fields['ok']}/{fields['ok'] + fields['wrong']}"
          f" = {pct(precision(fields))}")
    print(f"   zmeškané údaje (null, ale veřejně existují):  {fields['null_missed']}"
          f"/{fields['null_ok'] + fields['null_missed']}")

    # B) + C) ruční kontrola
    manual = [r for r in read_csv(DATA / "manual_check.csv") if (r.get("human_verdict") or "").strip()]
    if not manual:
        print("\nB) Ruční kontrola: data/manual_check.csv zatím nemá vyplněný sloupec human_verdict.")
    else:
        sample = [r for r in manual if r["group"] == "1_random_sample"]
        c = Counter(r["human_verdict"].strip().lower() for r in sample)
        recs = {}
        for r in sample:
            if r["field"] in ("decision", "investor_type"):
                recs.setdefault(r["id"], []).append(r["human_verdict"].strip().lower() == "ok")
        rec_ok = sum(all(v) for v in recs.values())
        print(f"\nB) Finální data, ruční kontrola člověkem (náhodný vzorek {len(recs)} záznamů, {len(sample)} polí)")
        print(f"   přesnost záznamu: {rec_ok}/{len(recs)}")
        print(f"   přesnost polí:    {c['ok']}/{c['ok'] + c['wrong']} = {pct(precision(c))}   "
              f"(neověřitelné {c['unverifiable']}, zmeškané {c['null_missed']})")
        rows.append({"measure": "B_final_by_human", "field": "all", **{k: c[k] for k in
                     ("ok", "wrong", "unverifiable", "null_ok", "null_missed")}, "precision": pct(precision(c))})

        same = [r for r in manual if not r.get("corrected_after_b") and r.get("agent_b_verdict")]
        agree = sum(1 for r in same if r["agent_b_verdict"].strip().lower() == r["human_verdict"].strip().lower())
        if same:
            print(f"\nC) Shoda agent B × člověk na neopravených polích: {agree}/{len(same)} = {agree / len(same):.0%}")
            for r in same:
                if r["agent_b_verdict"].strip().lower() != r["human_verdict"].strip().lower():
                    print(f"   neshoda: {r['id']}.{r['field']}: B={r['agent_b_verdict']} člověk={r['human_verdict']}"
                          f" – {r.get('human_comment', '')}")

        disputed = [r for r in manual if r["group"] != "1_random_sample"]
        if disputed:
            print("\n   Sporné body a nepotvrzené citace (rozhodnutí člověka):")
            for r in disputed:
                print(f"   {r['id']}.{r['field']} = {r['value'][:50]} → {r['human_verdict']} {r.get('human_comment', '')}")

    with open(DATA / "accuracy.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()
