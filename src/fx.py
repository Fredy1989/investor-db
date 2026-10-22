"""Přepočet měn do EUR referenčním kurzem ECB k datu zdroje.

Přepočet dělá kód, ne LLM. V pilotu agenti použili pevný kurz z pokynů (1 USD = 0,92 EUR),
což byla nejčastější chyba ověřená agentem B (viz RESULTS.md).

Fakt s jinou měnou nese v záznamu objekt `original`:
  {"currency": "USD", "amount": 88e6}                  -> value.eur
  {"currency": "USD", "min": 1e6, "max": 5e6}          -> value.min_eur / value.max_eur
Kurz se bere k `source_date`; u nedatovaného zdroje k datu přístupu (`accessed`).
O víkendu / svátku platí poslední kurz před tímto dnem.

Použití: python src/fx.py   (přepočítá a uloží záznamy; kurzy cachuje v data/fx_ecb.csv)
"""
import csv
import re
import json

import requests

from records import ROOT, RECORDS, load_records

FX_CACHE = ROOT / "data" / "fx_ecb.csv"
ECB = "https://data-api.ecb.europa.eu/service/data/EXR/D.{cur}.EUR.SP00.A?startPeriod=2014-01-01&format=csvdata"


def load_rates(currencies):
    rates = {}
    if FX_CACHE.exists():
        with open(FX_CACHE, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                rates.setdefault(r["currency"], {})[r["date"]] = float(r["rate"])
    missing = [c for c in currencies if c not in rates]
    for cur in missing:
        resp = requests.get(ECB.format(cur=cur), timeout=60)
        resp.raise_for_status()
        rows = csv.DictReader(resp.text.splitlines())
        rates[cur] = {r["TIME_PERIOD"]: float(r["OBS_VALUE"]) for r in rows if r["OBS_VALUE"]}
    if missing:
        with open(FX_CACHE, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["currency", "date", "rate"])
            for cur, by_date in sorted(rates.items()):
                for d, v in sorted(by_date.items()):
                    w.writerow([cur, d, v])
    return rates


def rate_on(rates, cur, date):
    """Kolik jednotek měny za 1 EUR k danému dni (poslední dostupný kurz ≤ date)."""
    days = [d for d in rates[cur] if d <= date]
    if not days:
        raise ValueError(f"žádný kurz {cur} k {date}")
    d = max(days)
    return rates[cur][d], d


def convert_fact(fact, rates):
    orig = fact.get("original")
    if not orig or orig["currency"] == "EUR":
        return False
    date = fact.get("source_date")
    if not date or date == "undated":
        date = fact.get("accessed", "2026-10-22")
    rate, rate_date = rate_on(rates, orig["currency"], date)
    value = fact.setdefault("value", {}) or {}
    if "amount" in orig:
        value["eur"] = round(orig["amount"] / rate)
    if "min" in orig:
        value["min_eur"] = round(orig["min"] / rate) if orig["min"] is not None else None
    if "max" in orig:
        value["max_eur"] = round(orig["max"] / rate) if orig["max"] is not None else None
    fact["value"] = value
    fact["fx"] = {"source": "ECB", "rate_date": rate_date, "eur_rate": rate, "currency": orig["currency"]}
    if fact.get("value_text"):
        # agent do textu psal vlastní (chybný) přepočet – ten odstranit, ať text neodporuje hodnotě
        text = OLD_FX.sub("", fact["value_text"])
        text = re.sub(r"\(\s*[;,]?\s*\)|\(\s*[;,]\s*", lambda m: "" if m.group().endswith(")") else "(", text)
        text = re.sub(r"\s+;", ";", re.sub(r"\(\s+", "(", text))
        text = re.sub(r"\s{2,}", " ", text).strip(" ;,")
        fact["value_text"] = f"{text} · přepočet ECB k {rate_date}: 1 EUR = {rate} {orig['currency']}"
    return True


OLD_FX = re.compile(r"(přepočet |kurz(em)? )?1 (USD|CZK) = 0,\d+ EUR( → [^;)]*)?;?")


def main():
    recs = load_records()
    currencies = sorted({f["original"]["currency"]
                         for r in recs for f in [r.get("ticket"), r.get("capital"), *(r.get("funds") or [])]
                         if isinstance(f, dict) and f.get("original") and f["original"]["currency"] != "EUR"})
    rates = load_rates(currencies)
    for r in recs:
        changed = False
        for key in ("ticket", "capital"):
            if isinstance(r.get(key), dict):
                changed |= convert_fact(r[key], rates)
        for fund in r.get("funds") or []:
            if fund.get("original"):
                date = fund["original"].get("date") or fund.get("source_date")
                tmp = {"original": fund["original"], "source_date": date, "value": {}}
                if convert_fact(tmp, rates):
                    fund["size_eur"] = tmp["value"]["eur"]
                    fund["fx"] = tmp["fx"]
                    changed = True
        if changed:
            with open(RECORDS / f"{r['id']}.json", "w", encoding="utf-8") as f:
                json.dump(r, f, ensure_ascii=False, indent=2)
            print(f"přepočteno: {r['id']}")


if __name__ == "__main__":
    main()
