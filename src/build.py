"""Z JSON záznamů vyrobí ploché tabulky se zdrojem u každého údaje.

  data/investors_cz_vc.csv  zařazení investoři (decision = include)
  data/excluded.csv         vyřazení a neaktivní, s pravidlem a důvodem

Použití: python src/build.py
"""
import csv

from records import ROOT, load_records

DATA = ROOT / "data"


def fact_cols(prefix, fact):
    fact = fact or {}
    return {
        f"{prefix}_source": fact.get("source_url") or "",
        f"{prefix}_source_date": fact.get("source_date") or "",
        f"{prefix}_tier": fact.get("source_tier") or "",
    }


def latest_deal(rec):
    deals = [d for d in (rec.get("investment_evidence") or []) if d.get("date")]
    return max(deals, key=lambda d: d["date"]) if deals else {}


def join(v):
    return "; ".join(v) if isinstance(v, list) else (v or "")


def included_row(rec):
    ticket = (rec.get("ticket") or {}).get("value") or {}
    capital = (rec.get("capital") or {}).get("value") or {}
    deal = latest_deal(rec)
    row = {
        "id": rec["id"], "name": rec["name"], "legal_name": rec.get("legal_name") or "",
        "investor_type": rec.get("investor_type"), "country": rec.get("country"),
        "hq_city": rec.get("hq_city") or "", "website": rec.get("website") or "",
        "registry_id": (rec.get("registry") or {}).get("value") or "",
    }
    row.update(fact_cols("registry", rec.get("registry")))
    row["sectors"] = join((rec.get("sectors") or {}).get("value"))
    row.update(fact_cols("sectors", rec.get("sectors")))
    row["stages"] = join((rec.get("stages") or {}).get("value"))
    row.update(fact_cols("stages", rec.get("stages")))
    row["ticket_min_eur"] = ticket.get("min_eur") if ticket.get("min_eur") is not None else ""
    row["ticket_max_eur"] = ticket.get("max_eur") if ticket.get("max_eur") is not None else ""
    row["ticket_text"] = (rec.get("ticket") or {}).get("value_text") or ""
    row.update(fact_cols("ticket", rec.get("ticket")))
    row["capital_eur"] = capital.get("eur") if capital.get("eur") is not None else ""
    row["capital_basis"] = capital.get("basis") or ""
    row["capital_text"] = (rec.get("capital") or {}).get("value_text") or ""
    row.update(fact_cols("capital", rec.get("capital")))
    row["evidence_count"] = len(rec.get("investment_evidence") or [])
    row["last_deal_company"] = deal.get("company", "")
    row["last_deal_date"] = deal.get("date", "")
    row["last_deal_round"] = deal.get("round", "")
    row["last_deal_source"] = deal.get("source_url", "")
    row["last_deal_tier"] = deal.get("source_tier", "")
    row["accessed"] = "2026-10-22"
    return row


def write(path, rows):
    if not rows:
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def main():
    recs = load_records()
    inc = [included_row(r) for r in recs if r.get("decision") == "include"]
    exc = [{
        "id": r["id"], "name": r["name"], "decision": r.get("decision"),
        "exclusion_rule": r.get("exclusion_rule") or "", "reason": r.get("decision_reason") or "",
        "last_deal_date": latest_deal(r).get("date", ""), "last_deal_source": latest_deal(r).get("source_url", ""),
    } for r in recs if r.get("decision") != "include"]
    write(DATA / "investors_cz_vc.csv", sorted(inc, key=lambda r: r["name"].lower()))
    write(DATA / "excluded.csv", sorted(exc, key=lambda r: r["name"].lower()))

    n = len(inc)
    def cov(col):
        return sum(1 for r in inc if r[col] not in ("", None)) / n if n else 0
    print(f"zařazeno {n}, vyřazeno/neaktivní {len(exc)}")
    for col in ["registry_id", "sectors", "stages", "capital_eur", "last_deal_date"]:
        print(f"  pokrytí {col:<16} {cov(col):.0%}")
    ticket = sum(1 for r in inc if r["ticket_min_eur"] != "" or r["ticket_max_eur"] != "") / n if n else 0
    print(f"  pokrytí {'ticket (min/max)':<16} {ticket:.0%}")

    # aktuálnost: věcné údaje se mění (nový fond, jiný tiket) → stáří zdroje je součást spolehlivosti
    print("  aktuálnost zdroje (≤ 24 m / 24–36 m / > 36 m = zastaralé / nedatováno):")
    for col in ["sectors", "stages", "ticket", "capital"]:
        c = {"fresh": 0, "aging": 0, "stale": 0, "undated": 0}
        for r in inc:
            if not r[f"{col}_source"]:
                continue
            c[freshness(r[f"{col}_source_date"])] += 1
        print(f"    {col:<8} {c['fresh']:>3} / {c['aging']:>3} / {c['stale']:>3} / {c['undated']:>3}")


def freshness(date, today="2026-10-22"):
    if not date or date == "undated":
        return "undated"
    y, m = int(today[:4]) - int(date[:4]), int(today[5:7]) - int(date[5:7] or 1)
    months = y * 12 + m
    return "fresh" if months <= 24 else "aging" if months <= 36 else "stale"


if __name__ == "__main__":
    main()
