"""Strojová kontrola citací: stáhne každý zdroj a ověří, že citace na stránce opravdu je.

Chytá typické chyby LLM agentů: vymyšlenou URL (404), vymyšlenou nebo parafrázovanou citaci,
údaj „z paměti", ke kterému byl zdroj dohledán dodatečně.

Výstup: data/quote_check.csv
  exact      citace je na stránce doslova (po normalizaci mezer, uvozovek a velikosti písmen)
  fuzzy      ≥ 80 % pětic slov citace je na stránce (drobná odchylka, např. zalomení, formátování čísla)
  partial    40–80 % — citace je pravděpodobně upravená, nutná ruční kontrola
  not_found  < 40 % — citace na stránce není (halucinace nebo jiná verze stránky)
  fetch_failed / js_or_blocked — stránku nejde stáhnout nebo je prázdná (JS aplikace) → ruční kontrola

Použití: python src/check_quotes.py
"""
import csv
import hashlib
import io
import re
import sys
import time
import unicodedata

import requests
from bs4 import BeautifulSoup

from records import ROOT, iter_facts, load_records

CACHE = ROOT / "data" / "cache"
OUT = ROOT / "data" / "quote_check.csv"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) investor-db-quote-check/1.0"


def normalize(text):
    text = unicodedata.normalize("NFKC", text or "")
    text = text.replace(" ", " ")
    text = re.sub(r"[‘’‚‛`´]", "'", text)
    text = re.sub(r"[“”„‟«»]", '"', text)
    text = re.sub(r"[‐-―−]", "-", text)
    text = re.sub(r"\s+", " ", text)
    # HTML často vloží mezeru před interpunkci kvůli odkazům a <strong> („Delta Green ,")
    text = re.sub(r" ([,.;:!?\"'])", r"\1", text)
    return text.strip().lower()


def fetch(url):
    """Vrací (http_status, text stránky). Stránky se cachují, aby opakovaný běh nezatěžoval weby."""
    CACHE.mkdir(parents=True, exist_ok=True)
    key = CACHE / (hashlib.sha1(url.encode()).hexdigest() + ".txt")
    if key.exists():
        status, _, body = key.read_text(encoding="utf-8").partition("\n")
        return int(status), body
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=25)
        status = r.status_code
        ctype = r.headers.get("content-type", "")
        if "charset" not in ctype.lower():
            # bez charsetu v hlavičce requests předpokládá ISO-8859-1 → české stránky by byly rozbité
            r.encoding = r.apparent_encoding
        if "pdf" in ctype or url.lower().endswith(".pdf"):
            body = pdf_text(r.content)
        else:
            soup = BeautifulSoup(r.text, "html.parser")
            for tag in soup(["script", "style", "noscript"]):
                tag.decompose()
            # meta description často obsahuje text, který agent viděl ve výsledku vyhledávání
            metas = " ".join(m.get("content", "") for m in soup.find_all("meta") if m.get("content"))
            body = soup.get_text(" ") + " " + metas
    except requests.RequestException as e:
        return 0, f"ERROR {e.__class__.__name__}"  # síťová chyba se necachuje, příští běh to zkusí znovu
    key.write_text(f"{status}\n{body}", encoding="utf-8")
    time.sleep(0.5)
    return status, body


def pdf_text(content):
    try:
        from pypdf import PdfReader
    except ImportError:
        return ""
    reader = PdfReader(io.BytesIO(content))
    return " ".join((p.extract_text() or "") for p in reader.pages)


def ngram_score(quote, page, n=5):
    words = quote.split()
    if len(words) < n:
        return 1.0 if quote in page else 0.0
    grams = [" ".join(words[i:i + n]) for i in range(len(words) - n + 1)]
    return sum(g in page for g in grams) / len(grams)


def check(quote, status, page):
    if status == 0 or status >= 400:
        return "fetch_failed", 0.0
    page_n = normalize(page)
    if len(page_n) < 300:
        return "js_or_blocked", 0.0
    q = normalize(quote).strip('"').strip()
    if not q:
        return "no_quote", 0.0
    if q in page_n:
        return "exact", 1.0
    score = ngram_score(q, page_n)
    if score >= 0.8:
        return "fuzzy", score
    if score >= 0.4:
        return "partial", score
    return "not_found", score


def main():
    rows = []
    for rec in load_records():
        for field, idx, fact in iter_facts(rec):
            url = fact["source_url"]
            status, page = fetch(url)
            verdict, score = check(fact.get("quote", ""), status, page)
            rows.append({
                "id": rec["id"], "decision": rec.get("decision"), "field": field, "index": idx,
                "source_url": url, "source_tier": fact.get("source_tier", ""),
                "http_status": status, "verdict": verdict, "score": round(score, 2),
                "quote": (fact.get("quote") or "")[:300],
            })
            print(f"{rec['id']:<14} {field:<20} {verdict:<13} {url}", file=sys.stderr)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    total = len(rows)
    counts = {}
    for r in rows:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    print(f"\n{total} citací:")
    for k, v in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  {k:<14} {v:>4}  ({v / total:.0%})")


if __name__ == "__main__":
    main()
