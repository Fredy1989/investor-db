# Výsledky pilotu a odhad nákladů

Pilot: **VC investoři se sídlem v Česku**, stav k 2026-10-22. Pipeline a pravidla jsou v [PLAN.md](PLAN.md).

## 1. Co vzniklo

| | počet |
|---|---|
| kandidáti (z veřejných seznamů a mých vlastních tipů) | 29 |
| **zařazeno** ([data/investors_cz_vc.csv](data/investors_cz_vc.csv)) | **21** — 15 `vc`, 3 `cvc`, 3 `private_investor` |
| vyřazeno, neaktivní nebo mimo rozsah vzorku ([data/excluded.csv](data/excluded.csv)) | 8 |
| údajů se zdrojem a citací | 226 |
| zdroje u zařazených: tier A (web investora, registr) / B (média) / C (agregátor) | 66 / 54 / 3 |
| zdroj dokládající nejnovější investici: tier A / B (každý s datem) | 2 / 19 |
| nejnovější doložená investice: 2026 / 2025 / 2023 | 12 / 8 / 1 |

Vyřazení, kde se pravidla otestovala na hraničních případech:

| kandidát | pravidlo | proč |
|---|---|---|
| Fundlift | E1 | crowdfundingová platforma, sama neinvestuje |
| Orbit Capital | E3 | od 10/2023 jen venture debt, poslední equity deal 2022 |
| StartupYard | E6 | akcelerátor s vlastními vozidly (E2 neplatí), ale investice za 36 měsíců je doložená jen agregátorem → neaktivní, dokud se nenajde lepší zdroj |
| Národní rozvojový fond | I4 | infrastrukturní fond, nikdy neinvestoval, dnes vymazán z rejstříku |
| IP Lab Ventures | I2 | fond teprve vzniká (závazek EIF 09/2026), zatím bez investice |
| Longevitytech.fund | I1 | zřejmě aktivní, ale nedohledal jsem právnickou osobu → ruční dohledání |
| „Pointer" | I1 | **neexistuje** — kandidáta jsem do seznamu chybně přidal já (viz README) |
| Genesis Capital | mimo rozsah | platný PE investor (pro plnou DB), ale vzorek byl definován jako VC-typy (PLAN §6). Původně zařazen omylem, našel to Mac Claude |

## 2. Pokrytí polí (zařazení, po opravách)

| pole | pokrytí | poznámka |
|---|---|---|
| registrace (IČO) | 100 % | |
| důkaz investice za 36 měsíců | 100 % | podmínka zařazení |
| fáze | 95 % | |
| sektory | 95 % | 1× null: Reflex svůj mandát nikde neuvádí |
| investiční kapitál | 86 % | `basis` říká, co číslo znamená (poslední fond / AUM / hodnota portfolia / vlastní kapitál) |
| tiket | 81 % | nikdy se nedopočítává; null = investor ho nezveřejňuje |

### Aktuálnost zdrojů

Aktuálnost se měří od review Mac Clauda, viz PLAN §7.9. Výstup `python src/build.py`, počty polí u zařazených:

| pole | ≤ 24 měsíců | 24–36 m | > 36 m | nedatováno |
|---|---|---|---|---|
| sektory | 3 | 1 | 1 | 15 |
| fáze | 3 | 2 | 2 | 13 |
| tiket | 3 | 2 | 2 | 13 |
| kapitál | 6 | 1 | 6 | 8 |

- **Kapitál je nejslabší místo.** U 4 vyplněných hodnot je zdroj starší než 3 roky: Lighthouse 2019, Impulse 2020,
  Czech Founders 2022, Tilia 2023. Často jde o velikost fondu z doby jeho vzniku. Číslo není chybné, ale nemusí být aktuální.
- **„Nedatováno" jsou z velké části weby investorů.** Ty platí k datu přístupu (2026-10-22), takže nejde o zastaralost.
  Při škálování je ale potřeba ukládat snapshot stránky (např. Wayback Machine), aby šlo zpětně doložit, co na ní bylo.

## 3. Přesnost

Měří se tři různé věci a nemíchám je ([src/measure.py](src/measure.py), [data/accuracy.csv](data/accuracy.csv)).

### A) Surový výstup rešeršního agenta — ověřeno nezávislým agentem B, všech 29 záznamů

| pole | ok | chyba | neověřitelné | null, ale existuje | přesnost |
|---|---|---|---|---|---|
| rozhodnutí (zařadit/vyřadit) | 22 | 0 | 1 | – | 100 % |
| typ investora | 21 | 2 | 0 | – | 91 % |
| registrace | 23 | 0 | 0 | 0 | 100 % |
| sektory | 19 | 2 | 0 | 1 | 90 % |
| fáze | 19 | 3 | 0 | 0 | 86 % |
| tiket | 13 | 4 | 0 | 3 | 76 % |
| kapitál | 12 | 6 | 0 | 2 | 67 % |
| nejnovější investice | 18 | 2 | 3 | 0 | 90 % |

- **Přesnost záznamu** (je to aktivní investor správného typu): **20/23 = 87 %**
- **Přesnost vyplněných polí: 104/121 = 86 %**
- Správně vyřazené: 5/6 (NRF měl být `exclude`, ne `inactive`)
- Zmeškané údaje (null, i když veřejně existují): 6/14

**Rozbor 17 chybných polí:**

| příčina | počet | čí chyba | náprava |
|---|---|---|---|
| přepočet měny pevným kurzem 0,92 USD/EUR místo kurzu k datu zdroje | 8 | **moje** — pokyny pro agenty byly v rozporu s plánem | přepočet přesunut do kódu: [src/fx.py](src/fx.py), kurzy ECB |
| sektory/fáze „domyšlené" z několika dealů, ne z mandátu investora | 5 | agent A | do pokynů: „sektor jen z mandátu; z dealů jen s `derived_from`" |
| existuje novější veřejný údaj (deal, velikost fondu) | 3 | agent A | při škálování pravidelný refresh |
| údaj ve zdroji byl, ale agent ho nepřevzal (min. tiket) | 1 | agent A | |

**Bez systémové chyby kurzu je přesnost polí 104/113 = 92 %.** To je realistický odhad pro opravenou pipeline.

**Omezení metriky A** (upozornil Mac Claude):
- Agent B viděl citace agenta A, takže nebyl slepý. „ok" může znamenat jen, že citace na stránce je, ne že B údaj
  nezávisle dohledal. Číslo A je proto spíš horní odhad. Ve v2 dostane ověřovatel jen tvrzení + URL (PLAN §7.10).
- Metrika A počítá i Genesis jako zařazený (23 záznamů). Genesis byl vyřazen až po review jako mimo rozsah vzorku.

### B) Finální data — ruční kontrola člověkem

List [data/manual_check.csv](data/manual_check.csv) má 58 řádků:
- náhodný vzorek 6 záznamů × 8 polí: losováno předem (seed 20261022) a po vyřazení Genesis zafixováno, aby se vzorek po pohledu do dat neměnil,
- 5 sporných rozhodnutí (včetně Genesis „mimo rozsah"),
- 5 citací, které stroj nepotvrdil.

U řádků s rozhodnutím je zdůvodnění agenta ve vlastním sloupci `rationale`, odděleně od citace ze zdroje (`quote`).
Upozornil na to Mac Claude: kontrolor by jinak mohl zdůvodnění agenta považovat za text zdroje.

> **Stav k 2026-10-22: čeká na vyplnění.** Číslo B doplní `python src/measure.py`, jakmile bude vyplněný sloupec
> `human_verdict`. Ověřovací agent B tohle číslo měřit nemůže, protože opravy sám navrhl.

### C) Shoda ověřovacího agenta s člověkem

Počítá se ze stejného listu, z polí, která se po ověření neměnila. Na tomhle čísle stojí škálování: pokud agent B
souhlasí s člověkem v ≥ 95 % případů, stačí lidsky kontrolovat jen statistický vzorek a sporné body.

### D) Úplnost (recall) — křížově s nezávislým řešením na Macu

Druhá session Claude Code (Mac) řešila stejné zadání na stejném vzorku nezávisle. Výsledky se porovnaly až dodatečně.
Dva nezávislé „úlovky" stejné populace umožňují odhadnout její velikost (Lincoln–Petersen):

| | počet |
|---|---|
| zařazeno zde (VC-typy) | 21 |
| zařazeno na Macu | 17 |
| v obou | 15 |
| **odhad populace aktivních VC-typových investorů v ČR** | **21 · 17 / 15 ≈ 24** |
| **odhad úplnosti tohoto řešení** | **21 / 24 ≈ 88 %** |

- Chybí tu **JIC Ventures** a **i&i Bio**. Našel je jen Mac.
- **Ztráta úplnosti vzniká při výběru kandidátů, ne při rešerši:** kdo se nedostane do seznamu kandidátů,
  v databázi nebude. Pro škálování to znamená brát kandidáty z víc nezávislých zdrojů (registry, portfolia EIF,
  média) a průnik průběžně měřit.
- Pozor: obě session čerpaly z podobných veřejných seznamů. Úlovky tedy nejsou úplně nezávislé a populace
  je spíš podhodnocená.

### Strojová kontrola citací

| výsledek | počet |
|---|---|
| citace na stránce doslova | 219 (97 %) |
| drobná odchylka (fuzzy) | 2 |
| částečná shoda (citace mírně upravená) | 1 |
| web blokuje stahování / chyba serveru | 3 → ruční kontrola |
| bez citace (odvozený údaj) | 1 |

Žádná vymyšlená URL a žádná vymyšlená citace. Pro spolehlivost je to podstatné: halucinace
by se projevily jako `not_found`. Kontrola zároveň našla 3 chyby ve mně psaném checkeru
(kódování stránek bez charsetu, mezera před čárkou v HTML, cachování síťových chyb), viz historie commitů.

## 4. Kolik stál pilot

Naměřeno ze statistik agentů:

| fáze | tokeny | volání nástrojů | čas agentů |
|---|---|---|---|
| rešerše (5 agentů, 29 kandidátů) | 805 tis. | 404 | 56 min (paralelně ~16 min) |
| ověření (4 agenti) | 580 tis. | 186 | 26 min (paralelně ~7 min) |
| **na 1 kandidáta** | **~48 tis.** | **~20** | **~2,8 min** |

**Pozor, nejsou to účtované tokeny** (opraveno po review Mac Clauda). Statistika agenta neodpovídá tomu, co se platí:
agentní smyčka posílá při každém volání nástroje celý dosavadní kontext znovu. Při ~20 voláních a kontextu, který roste
s 5–6 kandidáty v jednom agentovi, je účtovaný vstup řádově 10× vyšší. Většina z toho jsou ale levné cache reads.

## 5. Odhad nákladů na celý svět

### Předpoklady
- **Kolik subjektů:** podle [PLAN.md §5](PLAN.md) 30–50 tis. investorů, z toho jádro VC/PE/CVC 12–16 tis.
- **Kolik kandidátů na jednoho zařazeného:** v pilotu prošlo 21 z 29 (72 %). Pilotní seznam byl ale kurátorovaný.
  U celosvětových zdrojů počítám **50 %** a u andělů a FO **30 %**. Kandidátů tak bude: jádro ~30 tis., celek ~100 tis.
- **Cena LLM na kandidáta (rešerše + ověření), s opakovaným posíláním kontextu:**
  - Opus 5.5 ≈ **$0,87**, Sonnet 5.5 ≈ **$0,48**.
  - Model nezávisle spočítal Mac Claude, každý kandidát v samostatném běhu.
  - Můj původní odhad $0,27 vycházel ze statistiky agentů a byl **2–3× podhodnocený**.
- **Vyhledávání:** ~8 dotazů na kandidáta × **$10 / 1 000 dotazů** ≈ $0,08. Cena je ověřená v ceníku Anthropic
  (platform.claude.com/docs/en/about-claude/pricing, 2026-10-22). Web fetch je bez příplatku.
- → plánovací cena **$0,55–0,95 na kandidáta** (Sonnet / Opus).
- **Lidská práce** (sazba ~35 EUR/h):
  - stratifikovaný kontrolní vzorek (segment × region),
  - rozhodnutí sporných případů: v pilotu 4 z 23 záznamů (~15 %), ~5 min na případ,
  - ruční kontrola pole ~0,8 min (odhad: 58 řádků za ~45 min).

### Výsledek

| položka | jádro VC/PE/CVC | celý rozsah |
|---|---|---|
| kandidátů | ~30 tis. | ~100 tis. |
| LLM + vyhledávání ($0,55–0,95/kand.) | ~16–29 tis. USD ≈ 15–25 tis. EUR | ~55–95 tis. USD ≈ 49–85 tis. EUR |
| kontrolní vzorek (900 / 1 800 záznamů × 8 polí) | ~95 h ≈ 3,3 tis. EUR | ~190 h ≈ 6,7 tis. EUR |
| sporné případy (15 % zařazených × 5 min) | ~175 h ≈ 6 tis. EUR | ~500 h ≈ 17,5 tis. EUR |
| vývoj (fronta úloh, deduplikace, napojení registrů, monitoring) | 3–4 týdny ≈ 10–15 tis. EUR | stejné |
| **první naplnění celkem** | **≈ 35–50 tis. EUR** | **≈ 85–125 tis. EUR** |
| údržba: obnova každých 6 měsíců (pravidlo 36 měsíců, nové fondy) | ≈ 40 % prvního naplnění ročně | |
| čas běhu (20 paralelních agentů, ~2,8 min/kand.) | ~3 dny | ~10 dní |

Pro srovnání: nezávislý odhad Mac Clauda pro celý rozsah je ≈ 90 tis. EUR (rozpětí 50–150 tis.). Tedy uvnitř mého rozpětí.

**Čas běhu je podmíněný rate limity.** Mac pilot dostal HTTP 429 už při 2 paralelních ověřovatelích. Pro
20 paralelních agentů je potřeba vyšší úroveň limitů API, jinak se čas běhu násobí.

### Co náklady nejvíc sníží
1. **Nejdřív strojově čitelné registry, až potom LLM.** SEC IAPD / Form ADV (američtí „exempt reporting advisers" = VC),
   SEC Form D (dealy), registr ESMA / národní registry AIFM, ČNB, portfolio EIF a EBRD. Pokryjí pravidlo I1 a část I2
   skoro zadarmo a LLM pak dělá jen to, co registr neumí: sektory, tiket, mandát.
2. **Levný předfiltr.** Haiku 5.5 ($0,10 / 1 M) vyřadí zjevné nesmysly (crowdfunding, poradce, firmy bez investic)
   dřív, než na ně padne drahá rešerše. V pilotu by to ušetřilo 3 z 29 rešerší.
3. **Dávkové zpracování** (Batch API −50 %) pro kroky bez nástrojů: klasifikace, normalizace sektorů.
4. **Lidi jen tam, kde se agenti neshodnou.** Shoda agent B × člověk (metrika C) rozhodne, jak malý smí být kontrolní vzorek.

### Rizika odhadu
- Yield 50 % / 30 % je odhad. Skutečnou hodnotu dá pilot na jedné velké zemi s nekurátorovaným vstupem (např. Německo).
- Mimo latinku a angličtinu (Čína, Japonsko, Blízký východ) bude přesnost nižší a ruční kontrola dražší.
- **Andělé jsou fyzické osoby → GDPR.** Před jejich sběrem je potřeba právní posouzení (oprávněný zájem, informační povinnost).
- Weby blokují stahování (pilot: 4 zdroje). Ve velkém může být nutný placený scraping, což odhad nezahrnuje.
