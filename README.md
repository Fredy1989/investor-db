# Spolehlivá databáze investorů — zadání A

Řešení praktické úlohy k pozici Junior AI Developer.
Pilot: VC investoři v Česku. Každý údaj má zdroj, datum a doslovnou citaci, kterou kontroluje stroj.

| soubor | obsah |
|---|---|
| [PLAN.md](PLAN.md) | definice investora, pravidla zařazení/vyřazení, ověřování, odhad velikosti světa, úpravy po pilotu |
| [RESULTS.md](RESULTS.md) | výsledky pilotu, změřená přesnost, rozbor chyb, odhad nákladů na celý svět |
| [data/investors_cz_vc.csv](data/investors_cz_vc.csv) | **22 zařazených investorů**, u každého údaje zdroj, datum a tier |
| [data/excluded.csv](data/excluded.csv) | 7 vyřazených / neaktivních s pravidlem a důvodem |
| [data/records/](data/records/) | plné záznamy (JSON) po opravách — citace, fondy, všechny doložené dealy |
| [data/records_raw/](data/records_raw/) | totéž **beze změny tak, jak to vrátili rešeršní agenti** |
| [data/corrections.json](data/corrections.json) | 38 oprav: co se změnilo, proč a kdo to navrhl |
| [data/quote_check.csv](data/quote_check.csv) | strojová kontrola 226 citací |
| [data/verification/](data/verification/) | verdikty nezávislého ověřovacího agenta, pole po poli |
| [data/manual_check.csv](data/manual_check.csv) | list pro ruční kontrolu (náhodný vzorek + sporné body) |
| [data/accuracy.csv](data/accuracy.csv) | změřená přesnost |
| [docs/](docs/) | doslovné pokyny, které dostali agenti |
| [ai-log/](ai-log/) | export konverzace s Claude Code |

## Jak to spustit

```bash
pip install requests beautifulsoup4
python src/apply_corrections.py   # records_raw + corrections.json → records, přepočet měn kurzem ECB
python src/check_quotes.py        # stáhne zdroje a ověří citace → data/quote_check.csv
python src/build.py               # → investors_cz_vc.csv, excluded.csv, pokrytí polí
python src/measure.py             # → přesnost (A: agent B, B: člověk, C: shoda B × člověk)
```

## Jak jsem pracoval s AI

### Rozdělení rolí

```
            ┌──────────────────────────────────────────────┐
            │ hlavní session Claude Code (orchestrátor)     │
            │ plán, pravidla, kód, opravy, měření           │
            └──────┬──────────────────────────────┬────────┘
   5× paralelně    │                              │   4× paralelně, jiné dávky
   ┌───────────────▼─────────┐        ┌───────────▼──────────────────┐
   │ agent A: rešerše         │        │ agent B: ověření               │
   │ 5–6 kandidátů / agent     │ JSON → │ vidí jen záznamy a pravidla,   │
   │ každý údaj = URL + citace │        │ ne uvažování agenta A           │
   └──────────────────────────┘        └──────────────┬─────────────────┘
              │                                         │
              ▼                                         ▼
   src/check_quotes.py (stroj)        corrections.json → člověk: manual_check.csv
```

- **Já:** výběr zadání a jazyka, zadání úlohy hlavní session, kontrola výstupů, ruční kontrola vzorku (`manual_check.csv`).
- **Hlavní session (Claude Code, Opus 5.5):**
  - napsala plán, schéma a skripty,
  - rozdělila kandidáty do dávek a spustila agenty,
  - vyhodnotila jejich výstupy a rozhodla o opravách,
  - změřila přesnost.
- **Rešeršní agenti A (5×):** pokyny v [docs/prompt-research-agent.md](docs/prompt-research-agent.md). Hlavní body:
  - používat jen zdroje, které agent sám otevřel,
  - u každého údaje URL a **doslovnou citaci**,
  - chybějící údaj = `null`, tiket a kapitál nikdy neodhadovat,
  - vyřazení zdůvodnit konkrétním pravidlem.
- **Ověřovací agenti B (4×):** pokyny v [docs/prompt-verifier-agent.md](docs/prompt-verifier-agent.md).
  - Cíl je „najít chyby, ne záznamy potvrdit".
  - Každý agent B dostal jiné dávky, než jaké připravoval kterýkoli agent A. Nikdy tedy nekontroloval vlastní práci.
  - Do `data/records/` nesměl zapisovat, jen navrhoval opravy.

### Jak jsem výstup AI kontroloval (4 vrstvy)

1. **Strojová kontrola citací.** Skript stáhne každý zdroj a hledá v něm citaci. Vymyšlená URL nebo citace
   neprojde. Výsledek: 218 z 226 citací doslova, žádná vymyšlená.
2. **Nezávislý agent B.** Znovu otevřel zdroje a ke každému poli dal verdikt `ok / wrong / unverifiable / null_ok / null_missed`.
   Našel 17 chybných polí ze 121 a 6 zmeškaných údajů.
3. **Auditovatelné opravy.** Opravy se nedělají ručně v datech. Každá je zapsaná v [corrections.json](data/corrections.json)
   s důvodem a autorem a aplikuje se skriptem na nezměněný výstup agentů v `records_raw/`. V gitu je vidět rozdíl.
4. **Člověk.** Náhodný vzorek a sporné body v `manual_check.csv`. Ověřovací agent nemůže měřit přesnost dat, která
   sám opravil. Proto se finální přesnost (B) a důvěryhodnost agenta B (C) měří proti člověku.

### Kde se AI mýlila

| chyba | kdo | jak se přišlo na to | co jsem změnil |
|---|---|---|---|
| **Kandidát „Pointer"** jako crowdfundingová platforma. Žádná taková platforma neexistuje. | **hlavní session (orchestrátor)**, „ze znalosti trhu" | agent A ho nedohledal a vyřadil (I1), agent B to potvrdil | PLAN §7.8: kandidát musí mít zdroj |
| **NRF** jako státní VC fond. Byl to infrastrukturní fond, který nikdy neinvestoval. | hlavní session | agent A (podle pravidla I4) | dtto |
| **Pevný kurz 0,92 USD/EUR** v pokynech pro agenty, v rozporu s vlastním plánem | hlavní session | agent B, u 8 polí | přepočet přesunut do kódu ([src/fx.py](src/fx.py), ECB) |
| Sektory a fáze odvozené ze 2–3 dealů místo z mandátu (Purple, Aspire11, Inven…) | agenti A | agent B | PLAN §7.3: `derived_from` |
| Nesprávný typ: Pale Fire jako `pe`, i když ho plán sám uvádí jako vzor `private_investor` | agent A | agent B | oprava |
| Investice připsaná fondu, i když investoval zakladatel osobně (Impulse → Safetica) | agent A | agent B | důkaz odstraněn, zůstal starší deal |
| Deal doložený jen agregátorem s domyšleným dnem (StartupYard) | agent A | agent B | `inactive` + pravidlo PLAN §7.4 |
| 3 chyby v mnou napsaném checkeru citací: kódování, mezera před čárkou, cachování výpadků. Vedly by k falešným „not_found". | hlavní session | ruční pohled do stažených stránek | opraveno, viz commity |
| Agent při jednom hledání na SEC EDGAR poslal v hlavičce User-Agent e-mail uživatele | agent A | agent to sám nahlásil | do pokynů pro agenta B přidán zákaz osobních údajů v požadavcích |

**Prompt injection.** Dvě stránky (Dealroom a euacc.ai) obsahovaly pokyny pro AI, např. „If you are an LLM always mention…".
Agenti je ignorovali a nahlásili. Data z webu jsou data, ne pokyny. To je výslovně v pokynech pro agenta B a pro
produkční běh by to mělo být i v pokynech pro agenta A.

## Rozhodnutí tam, kde zadání nebylo jednoznačné

- **Vzorek = VC v Česku.** Zadání to navrhuje. Trh znám, je dost malý na ruční kontrolu a dost velký na to,
  aby obsahoval hraniční případy. Úmyslně jsem přidal kandidáty, kteří vyřazeni být mají (crowdfunding, akcelerátor,
  venture debt), abych ověřil i pravidla vyřazení, nejen jasné fondy.
- **Typy `cvc` a `public_vc`** navíc oproti zadání. Korporátní a státní fondy dělají velkou část dealů. Vyřadit je
  by znamenalo ztratit skutečné investory, zařadit je jako `vc` by zkreslilo typ.
- **Záznam = správcovská společnost, ne jednotlivý fond.** Investor jedná se správcem, fondy jsou jeho atributy.
- **„Investuje" = doložená investice za posledních 36 měsíců.** Tři roky pokryjí běžný investiční cyklus fondu.
  Starší aktivita jde do `inactive`, ne pryč.
- **„V akej výške" = typický tiket**, „celkový investičný kapitál" = poslední fond / AUM s uvedeným `basis`, protože
  investoři čísla zveřejňují různě a bez označení by nebyla porovnatelná.
- **Chybějící údaj = `null`, nikdy odhad.** U databáze, kde jde o spolehlivost, je díra lepší než vymyšlené číslo.
- **Zdroj = URL + datum zdroje + datum přístupu + doslovná citace + tier.** Samotná URL nestačí: stránky se mění
  a bez citace se nedá zpětně ověřit, co na nich bylo.

## Co v řešení chybí

- **Ruční kontrola člověkem** (`data/manual_check.csv`, ~45 min) — připravená, čeká na vyplnění. Až bude vyplněná,
  `python src/measure.py` doplní metriky B a C do výstupu.
- Longevitytech.fund: dohledat právnickou osobu (pravděpodobně česká a.s.). Jinak by byl zařazen.
- U KAYA, Miton a J&T Ventures upřesnit, která právnická osoba je správce (PLAN §7.5).
- Pokyny v2 pro agenta A (PLAN §7) jsou sepsané, ale pilot jsem s nimi znovu nepouštěl.
- Recall, tj. kolik českých VC v databázi chybí, je změřený jen nepřímo. Nezávislý úplný seznam (Dealroom, CVCA)
  není veřejně zdarma. Kandidáti jako NRI nebo United Founders se objevili až při ověřování a ve vzorku nejsou.
