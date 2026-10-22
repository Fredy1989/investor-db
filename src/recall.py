"""Úplnost (recall) vzorku proti oficiálnímu katalogu investorů CzechStartups (CzechInvest).

Referenční množina = položky katalogu, které po rešerši a ověření prošly pravidly (decision = include).
Položky katalogu, které jsou podle jeho vlastního popisu asociace, crowdfundingové platformy nebo zahraniční fondy,
se nerešeršovaly (data/reference_czechstartups.csv, sloupec catalog_class).

Měří:
  1. úplnost fáze 1 (původní výběr kandidátů) vůči katalogu,
  2. jak úplný je sám katalog vůči všem nalezeným investorům (katalog taky není úplný),
  3. odhad populace Lincoln–Petersen (fáze 1 × katalog jako dva „úlovky").

Použití: python src/recall.py
"""
import csv

from records import ROOT, load_records

DATA = ROOT / "data"


def main() -> None:
    recs = {r["id"]: r for r in load_records()}
    included = {rid for rid, r in recs.items() if r.get("decision") == "include"}
    phase1 = {rid for rid in included if recs[rid].get("phase") != 2}

    with open(DATA / "reference_czechstartups.csv", encoding="utf-8") as f:
        ref = list(csv.DictReader(f))
    catalog_ids = {row["record_id"] for row in ref if row["record_id"]}
    missing_records = sorted(i for i in catalog_ids if i not in recs)
    catalog_incl = catalog_ids & included

    print(f"katalog: {len(ref)} položek, z toho rešeršováno {len(catalog_ids)} subjektů "
          f"(zbytek: asociace / platformy / zahraniční podle popisu v katalogu)")
    if missing_records:
        print(f"  POZOR: chybí záznamy pro {missing_records}")
    print(f"  z katalogu prošlo pravidly (referenční množina): {len(catalog_incl)}")

    found = catalog_incl & phase1
    print(f"\n1) Úplnost fáze 1 vůči katalogu: {len(found)}/{len(catalog_incl)} = {len(found) / len(catalog_incl):.0%}")
    print(f"   chyběly: {', '.join(sorted(catalog_incl - phase1))}")

    print(f"\n2) Úplnost katalogu vůči všem zařazeným: {len(catalog_incl)}/{len(included)} "
          f"= {len(catalog_incl) / len(included):.0%}")
    print(f"   mimo katalog: {', '.join(sorted(included - catalog_ids))}")

    m = len(found)
    if m:
        n_est = len(phase1) * len(catalog_incl) / m
        print(f"\n3) Lincoln–Petersen: {len(phase1)} · {len(catalog_incl)} / {m} ≈ {n_est:.0f} aktivních investorů "
              f"(nalezeno celkem {len(included)})")

    with open(DATA / "recall.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["record_id", "decision", "phase", "in_catalog"])
        for rid in sorted(recs):
            w.writerow([rid, recs[rid].get("decision"), recs[rid].get("phase", 1), rid in catalog_ids])


if __name__ == "__main__":
    main()
