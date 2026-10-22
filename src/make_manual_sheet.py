"""Vyrobí list pro ruční kontrolu člověkem: data/manual_check.csv.

Obsah (aby kontrola stála ~45 min a přitom měřila to podstatné):
  1. náhodný vzorek 6 zařazených záznamů (pevný seed) × všechna pole  → nestranný odhad přesnosti
  2. sporné body: změny typu / rozhodnutí z corrections.json            → člověk rozhodne hraniční případy
  3. citace, které strojová kontrola nepotvrdila (partial / blocked …)  → ruční náhrada strojové kontroly

Sloupce human_verdict / human_comment vyplní člověk (ok / wrong / unverifiable / null_ok / null_missed).
Použití: python src/make_manual_sheet.py
"""
import csv
import json


from records import ROOT, load_records

DATA = ROOT / "data"
FIELDS = ["decision", "investor_type", "registry", "sectors", "stages", "ticket", "capital", "investment_evidence"]
SEED = 20261022  # random.Random(SEED).sample(22 zařazených, 6) → PINNED_SAMPLE
PINNED_SAMPLE = ["credo", "impulse", "lighthouse", "nation1", "tensor", "zaka"]


def fact_row(rec, field):
    if field in ("decision", "investor_type"):
        val = rec.get(field)
        if field == "decision" and rec.get("exclusion_rule"):
            val = f"{val} ({rec['exclusion_rule']})"
        deal = max(rec.get("investment_evidence") or [{}], key=lambda d: d.get("date", ""))
        # zdůvodnění agenta NENÍ citace ze zdroje → vlastní sloupec, aby si ho kontrolor nespletl se zdrojem
        return {"value": val, "source_url": deal.get("source_url", rec.get("website", "")),
                "quote": deal.get("quote", ""), "rationale": rec.get("decision_reason", "")}
    if field == "investment_evidence":
        d = max(rec.get("investment_evidence") or [{}], key=lambda d: d.get("date", ""))
        return {"value": f"{d.get('company')} | {d.get('date')} | {d.get('round')}",
                "source_url": d.get("source_url", ""), "quote": d.get("quote", "")}
    f = rec.get(field) or {}
    val = f.get("value")
    return {"value": json.dumps(val, ensure_ascii=False) + (f"  [{f['value_text']}]" if f.get("value_text") else ""),
            "source_url": f.get("source_url", ""), "quote": f.get("quote") or ""}


def agent_b_verdicts():
    out = {}
    for p in (DATA / "verification").glob("*.csv"):
        with open(p, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                field = "investment_evidence" if r["field"].startswith("investment_evidence") else r["field"]
                out[(r["id"], field)] = r["verdict"]
    return out


def main():
    recs = {r["id"]: r for r in load_records()}
    with open(DATA / "corrections.json", encoding="utf-8") as f:
        corr = json.load(f)
    corrected = {(c["id"], c["path"].split(".")[0]) for c in corr}
    b = agent_b_verdicts()

    # Vzorek byl vylosován 2026-10-22 ze 22 tehdy zařazených (seed níže). Po vyřazení Genesis (mimo rozsah) by stejný
    # seed losoval jiné záznamy – vzorek se ale po pohledu do dat měnit nesmí, proto je zafixovaný.
    sample = PINNED_SAMPLE

    items = [(rid, f, "1_random_sample") for rid in sample for f in FIELDS]
    for c in corr:
        top = c["path"].split(".")[0]
        if top in ("decision", "investor_type") and (c["id"], top, "1_random_sample") not in items:
            items.append((c["id"], top, "2_disputed"))
    with open(DATA / "quote_check.csv", encoding="utf-8") as f:
        for q in csv.DictReader(f):
            if q["verdict"] not in ("exact", "fuzzy") and q["decision"] == "include":
                key = (q["id"], q["field"], "3_quote_unconfirmed")
                if key not in items and (q["id"], q["field"], "1_random_sample") not in items:
                    items.append(key)

    rows = []
    for rid, field, why in dict.fromkeys(items):
        rec = recs[rid]
        fr = fact_row(rec, field)
        rows.append({
            "group": why, "id": rid, "name": rec["name"], "field": field,
            "value": fr["value"], "source_url": fr["source_url"], "quote": fr["quote"],
            "rationale": fr.get("rationale", ""),
            "agent_b_verdict": b.get((rid, field), ""),
            "corrected_after_b": "yes" if (rid, field) in corrected else "",
            "human_verdict": "", "human_comment": "",
        })
    out = DATA / "manual_check.csv"
    if out.exists():
        print(f"{out} už existuje – nepřepisuji (obsahuje ruční verdikty). Smaž ho ručně pro nové vygenerování.")
        return
    with open(out, "w", newline="", encoding="utf-8-sig") as f:  # BOM kvůli Excelu
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} řádků; náhodný vzorek: {', '.join(sample)}")


if __name__ == "__main__":
    main()
