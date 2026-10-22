"""Vyrobí podklady pro slepého ověřovatele (fáze 2): data/blind/<id>.json.

Ověřovatel dostane jen tvrzení (hodnotu) a URL zdroje. Nedostane citace, poznámky ani zdůvodnění rešeršního agenta,
aby si citaci musel ve zdroji najít sám a nemohl jen potvrdit podstrčený text (PLAN §7.10).

Použití: python src/make_blind_claims.py
"""
import json

from records import ROOT

RAW = ROOT / "data" / "records_raw"
OUT = ROOT / "data" / "blind"


def claim(fact: dict | None) -> dict:
    fact = fact or {}
    out = {"value": fact.get("value"), "source_url": fact.get("source_url")}
    if fact.get("original"):
        out["original"] = fact["original"]
    if fact.get("derived_from"):
        out["derived_from"] = fact["derived_from"]
    return out


def blind(rec: dict) -> dict:
    deals = sorted(rec.get("investment_evidence") or [], key=lambda d: d.get("date") or "", reverse=True)
    latest = deals[0] if deals else {}
    return {
        "id": rec["id"],
        "name": rec["name"],
        "claims": {
            "decision": {"value": rec.get("decision"), "exclusion_rule": rec.get("exclusion_rule"),
                         "source_url": latest.get("source_url")},
            "investor_type": {"value": rec.get("investor_type"), "country": rec.get("country"),
                              "website": rec.get("website")},
            "registry": claim(rec.get("registry")),
            "sectors": claim(rec.get("sectors")),
            "stages": claim(rec.get("stages")),
            "ticket": claim(rec.get("ticket")),
            "capital": claim(rec.get("capital")),
            "investment_evidence": {"company": latest.get("company"), "date": latest.get("date"),
                                    "round": latest.get("round"), "source_url": latest.get("source_url")},
        },
    }


def main() -> None:
    OUT.mkdir(exist_ok=True)
    n = 0
    for p in sorted(RAW.glob("*.json")):
        with open(p, encoding="utf-8") as f:
            rec = json.load(f)
        if rec.get("phase") != 2:
            continue
        with open(OUT / p.name, "w", encoding="utf-8") as f:
            json.dump(blind(rec), f, ensure_ascii=False, indent=2)
        n += 1
    print(f"{n} slepých podkladů v {OUT}")


if __name__ == "__main__":
    main()
