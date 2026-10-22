# Plán: spolehlivá databáze investorů

Verze 1 — 2026-10-22. Plán vznikl dřív než data; co se na vzorce ukázalo jinak, je v sekci 7 (úpravy po pilotu).

## 1. Co je „investor" (definice)

Do databáze patří subjekt, který **investuje kapitál do soukromých firem za podíl (equity) nebo kvazi-equity
(konvertibilní úvěr, SAFE, mezanin) s cílem finančního výnosu, a dělá to opakovaně nebo k tomu má vyčleněný kapitál.**

Rozlišujeme tyto typy (`investor_type`):

| typ | popis | příklad |
|---|---|---|
| `vc` | fond rizikového kapitálu, investuje do startupů (pre-seed až growth) | Credo Ventures |
| `pe` | private equity, majoritní/minoritní podíly ve zralých firmách, buy-outy | Genesis Capital |
| `cvc` | korporátní VC — investiční rameno nefinanční firmy | Inven Capital (ČEZ) |
| `public_vc` | fond se státním / EU kapitálem, který sám investuje equity do firem | NRF, fondy EIF |
| `family_office` | správa majetku jedné / několika rodin, která přímo investuje do firem | |
| `angel` | fyzická osoba investující vlastní peníze do startupů | |
| `private_investor` | investiční skupina / holding velkého soukromého investora | Pale Fire Capital |

`cvc` a `public_vc` v zadání nejsou. Přidal jsem je, protože v Česku i jinde dělají velkou část dealů.
Kdybych je vyřadil, chyběli by v databázi skuteční investoři. Kdybych je zařadil jako `vc`, zkreslil bych typ.

## 2. Pravidla zařazení a vyřazení

### Zařazení — musí platit VŠECHNA
| # | pravidlo | jak se dokládá |
|---|---|---|
| I1 | **Identifikovatelná entita**: právnická osoba dohledatelná v registru (ARES / obchodní rejstřík / zahraniční ekvivalent) nebo fond správce v registru ČNB, případně fyzická osoba s veřejným profesním profilem | IČO / číslo registrace + URL registru |
| I2 | **Doložená investice do soukromé firmy** za posledních **36 měsíců** (tisková zpráva, článek, portfolio s datem, rejstřík) | ≥ 1 deal: firma, datum, zdroj |
| I3 | Investování je **hlavní deklarovaná činnost** (fondy) nebo **opakovaná** činnost (≥ 2 doložené investice u andělů, korporací, holdingů) | web / výroční zpráva / 2 dealy |
| I4 | Investuje do **soukromých firem** (ne jen do nemovitostí, kotovaných akcií, dluhopisů) | popis strategie |

### Vyřazení — stačí JEDNO
| # | důvod | proč |
|---|---|---|
| E1 | Crowdfundingová / investiční platforma (Fundlift, Pointer…) | zprostředkovatel, sám neinvestuje |
| E2 | Akcelerátor / inkubátor / soutěž **bez** vlastního investičního vozidla | dává program nebo grant, ne kapitál za podíl |
| E3 | Jen dluh: banka, leasing, P2P, čistý venture-debt fond | není equity investor (venture-debt jako *doplněk* VC nevadí) |
| E4 | Poradce, M&A boutique, investiční banka, asociace, agentura, dotační program, nadace | nevkládá vlastní kapitál |
| E5 | Fond, který investuje jen do realit / kotovaných aktiv (typicky český FKI na nemovitosti) | mimo cíl databáze |
| E6 | **Neaktivní**: poslední doložená investice starší než 36 měsíců | jde do tabulky `inactive`, ne do hlavní DB |
| E7 | Strategický kupec, který jen kupuje firmy do svého podnikání (M&A), bez investičního ramene | nejde o finanční investici |
| E8 | Duplicita (stejné IČO / doména / správce) | sloučit pod správce, fondy jako `funds[]` |

Hranice, o které je potřeba rozhodnout: **správce vs. fond**. Záznam = **správcovská společnost** (Credo Ventures),
jednotlivé fondy (Credo Stage 4, 5…) jsou její atributy. Investoři řeší vztah se správcem, ne s fondovým vehiklem.

## 3. Povinná pole a zdroje

Každý údaj je samostatný objekt:
`{ value, source_url, source_date, accessed, quote, source_tier }`

- `source_date` = datum publikace zdroje (nebo `undated`, když ho stránka nemá),
- `accessed` = kdy jsme zdroj četli,
- `quote` = **doslovná citace** ze zdroje (≤ 300 znaků), na které údaj stojí → dá se strojově ověřit,
- `source_tier`: **A** primární (web investora, registr, výroční zpráva, EIF), **B** renomované médium / tisková zpráva
  firmy, do které se investovalo, **C** agregátor (Crunchbase, Dealroom, seznamy „top X").

| pole | povinné | poznámka |
|---|---|---|
| název, typ, země, web | ano | |
| registrace (IČO / registr) | ano u právnických osob | pravidlo I1 |
| sektory | ano | normalizovaná taxonomie (`fintech`, `saas_b2b`, `deeptech`, `ai`, `health`, `energy_climate`, `consumer`, `ecommerce`, `defence`, `mobility`, `industry`, `generalist`) |
| fáze | ano | `pre_seed`, `seed`, `series_a`, `series_b_plus`, `growth`, `buyout` |
| typický tiket (min–max, EUR) | ano, ale může být `null` | **nikdy se nedopočítává**; když ho investor nikde neuvádí, je `null` |
| investiční kapitál (EUR) | ano, ale může být `null` | `basis`: velikost posledního fondu / AUM / součet fondů — vždy uvedeno, co číslo znamená |
| důkaz investice | ano (≥ 1) | firma + datum + zdroj; pravidlo I2 |

**Zásada: chybějící údaj = `null`, ne odhad.** Odhad je horší než díra, protože vypadá jako fakt.
Měny se převádějí do EUR kurzem k datu zdroje a původní hodnota zůstává v `value_text`.

## 4. Jak ověřujeme pravost a zařazení

Pipeline (každý krok má jiného „autora", aby se chyby nenásobily):

1. **Kandidáti** — z veřejných seznamů: Wikipedia „Venture capital in the Czech Republic", přehledy médií
   (The Recursive, AIN, CzechCrunch), portfolio EIF / NRF, registr ČNB, členové CVCA. Kandidát ≠ investor.
2. **Rešerše (AI agent A)** — pro každého kandidáta vyplní záznam podle schématu, ke každému údaji URL + citaci.
   Instrukce: nic neodhadovat, chybějící = `null`, vyřazení zdůvodnit pravidlem E1–E8.
3. **Strojová kontrola citací** (`src/check_quotes.py`) — stáhne každý zdroj a ověří, že citace na stránce opravdu je.
   Chytá **halucinace** (vymyšlené URL, vymyšlené citáty, údaj „z hlavy"). Stránky, které se nedají stáhnout (JS, blokace),
   jdou do ruční kontroly.
4. **Nezávislé ověření (AI agent B)** — jiný agent bez přístupu k uvažování agenta A dostane jen záznam a pravidla
   a ověří: je to skutečný aktivní investor, sedí typ, sedí každý údaj se zdrojem. Výstup: `ok / chyba / nelze ověřit` pro každé pole.
5. **Ruční kontrola člověkem** — náhodný vzorek + všechny záznamy, kde se A a B neshodnou. Z ní se počítá přesnost.

### Metriky
- **Přesnost záznamu** = podíl zařazených záznamů, které jsou skutečně aktivní investor správného typu.
- **Přesnost pole** = podíl vyplněných polí, která odpovídají zdroji.
- **Pokrytí pole** = podíl záznamů, kde je pole vyplněné (ne `null`).
- **Úplnost (recall)** vůči referenčnímu seznamu — kolik známých investorů z nezávislého seznamu v DB je.

## 5. Odhad: kolik investorů se dá z veřejných zdrojů získat

| segment | kolik jich existuje | z toho veřejně ověřitelných (I1 + I2) | spolehlivost dat | z čeho vychází |
|---|---|---|---|---|
| VC (správci) | 4–7 tis. firem globálně; USA 3 417 (konec 2023) | **5–7 tis.** | vysoká: existence, typ, sektory; střední: tiket | NVCA Yearbook 2024 [1], odhad Konvoy [2] |
| PE (správci) | Preqin eviduje 10 300+ aktivních správců PE (včetně VC) | **5–7 tis.** bez VC | vysoká: existence, AUM; nízká: tiket | Preqin přes CBS Library [3] |
| Evropa PE+VC dohromady | Invest Europe sbírá data od 1 750+ firem | **1,5–2 tis.** | vysoká | Invest Europe Activity Report 2024 [4] |
| CVC | ~1–2 tis. aktivních | **1–1,5 tis.** | střední (často bez tiketu i kapitálu) | vlastní odhad, nízká jistota |
| Family office | 8 030 single FO globálně, 2 020 v Evropě | **1,5–2,5 tis.** (jen ty s veřejnými dealy) | **nízká**: FO nezveřejňují kapitál ani tikety | Deloitte 2024 [5] |
| Andělé | jen v sítích: UK 10 000, DE 7 500, FR 5 500 (2022); sítě ≈ 10 % trhu | **15–30 tis.** s ≥ 2 veřejnými investicemi | **nízká** u tiketu a kapitálu; GDPR (fyzické osoby) | EBAN přes Statista [6] |
| Velcí soukromí investoři / holdingy | | **1–3 tis.** | střední | vlastní odhad |

**Celkem: 30–50 tis. subjektů, z toho jádro s vysokou spolehlivostí (správci VC/PE/CVC) přibližně 12–16 tis.**

Očekávaná spolehlivost (hypotéza; pilot v sekci 6 ji potvrdí nebo vyvrátí):
- existence a typ u správců fondů: ≥ 95 % po ověření,
- sektory a fáze: ~ 90 %,
- tiket: pokrytí 50–70 %, přesnost ~ 85 %,
- kapitál: pokrytí 60–80 % u fondů, < 20 % u FO a andělů.

Proč tolik u andělů a FO nedoporučuji jako první vlnu: nemají registr, kapitál neuvádějí a jde o osobní údaje.
U andělů je potřeba právní titul (oprávněný zájem, GDPR čl. 6 odst. 1 písm. f) a ukládat jen profesní údaje.

Zdroje:
[1] https://nvca.org/nvca-yearbook/ (2024 Yearbook: „3,417 VC firms" ke konci 2023)
[2] https://www.konvoy.vc/blogs/venture-capital-statistics
[3] https://libguides.cbs.dk/newsletter/5426/database-prequin-private-equity-industry-data
[4] https://www.seca.ch/en/knowledge-library/newsletters/2025/seca-enewsletter-no-550/private-equity-int-news/investing-in-europe-private-equity-activity-2024/
[5] https://www.deloitte.com/content/dam/assets-shared/docs/services/deloitte-private/2024/2024-defining-the-family-office-landscape-executive-report.pdf
[6] https://www.statista.com/statistics/439305/business-angels-numbers-by-country-europe/

## 6. Pilot

Vzorek: **VC investoři se sídlem v Česku** (typy `vc`, `cvc`, `public_vc`, `private_investor`, pokud investují do startupů).
Úmyslně do vzorku dávám i hraniční kandidáty (crowdfunding, akcelerátory, venture debt), aby se pravidla vyřazení
otestovala na reálných případech, a ne jen na jasných fondech.

Výstupy:
- `data/candidates.csv` — všichni kandidáti a odkud se vzali,
- `data/records/*.json` — plné záznamy se zdroji,
- `data/investors_cz_vc.csv` — zařazení investoři (plochá tabulka, zdroj u každého údaje),
- `data/excluded.csv` — vyřazení s pravidlem,
- `data/quote_check.csv` — výsledek strojové kontroly citací,
- `data/verification.csv` — nezávislé ověření + ruční kontrola,
- `RESULTS.md` — změřená přesnost a odhad nákladů na celý svět.

## 7. Úpravy po pilotu

Doplněno po pilotu (viz `RESULTS.md`).
