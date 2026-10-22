"""Načtení záznamů a vytažení všech „faktů" (údaj + zdroj + citace) z JSON záznamu."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECORDS = ROOT / "data" / "records"

FACT_FIELDS = ["registry", "sectors", "stages", "ticket", "capital"]


def load_records():
    out = []
    for p in sorted(RECORDS.glob("*.json")):
        with open(p, encoding="utf-8") as f:
            out.append(json.load(f))
    return out


def iter_facts(rec):
    """Vrací (field, index, fact_dict) pro každý údaj, který má zdroj."""
    for field in FACT_FIELDS:
        fact = rec.get(field)
        if isinstance(fact, dict) and fact.get("source_url"):
            yield field, 0, fact
    for i, fund in enumerate(rec.get("funds") or []):
        if fund.get("source_url"):
            yield "funds", i, fund
    for i, ev in enumerate(rec.get("investment_evidence") or []):
        if ev.get("source_url"):
            yield "investment_evidence", i, ev
