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
| `public_vc` | fond se státním / EU kapitálem, který sám investuje equity do firem | (v pilotu žádný — NRF se ukázal jako neinvestující, viz §7) |
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
| E1 | Crowdfundingová / investiční platforma (např. Fundlift) | zprostředkovatel, sám neinvestuje |
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
| CVC | 2 344 korporací aktivně investujících do startupů (2024) | **1,5–2 tis.** (část investuje jen přímo z rozvahy bez identifikovatelného ramene) | střední (často bez tiketu i kapitálu) | Global Corporate Venturing [7] |
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
[7] https://globalventuring.com/corporate-investors-trends-2025/ („2,344 corporate investors actively taking part in startup funding rounds in 2024"; doplněno po review Mac Clauda)

Velcí soukromí investoři (holdingy) zůstávají **vlastním odhadem bez přímého zdroje**. Veřejné statistiky počítají
osoby (UHNW), ne jejich investiční vozidla, a převod mezi nimi neznám.

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

Pilot (viz [RESULTS.md](RESULTS.md)) ukázal, co v plánu chybělo nebo bylo špatně:

1. **Přepočet měn nesmí dělat LLM.** 8 ze 17 chybných polí byl kurz. Záznam teď nese `original` (částka, měna)
   a EUR počítá [src/fx.py](src/fx.py) podle kurzu ECB k datu zdroje; nedatovaný zdroj → datum přístupu.
2. **Vyřazení může mít i důvod „nesplněno I1–I4", ne jen E1–E8.** Subjekt, který neexistuje (I1) nebo nikdy
   neinvestoval (I4), nespadá pod žádné E-pravidlo. Kódy `I1`–`I4` jsou proto platné hodnoty `exclusion_rule`.
3. **Sektory a fáze jen z deklarovaného mandátu.** Když je investor neuvádí a jsou odvozené z dealů, pole má
   `derived_from: investment_evidence` a nemá citaci. Agenti měli sklon zobecňovat ze 2–3 dealů.
4. **Důkaz I2 jen z agregátoru (tier C) nestačí.** Bez potvrzení z tieru A/B jde subjekt do `inactive` a čeká na
   lepší zdroj (StartupYard). Agregátory jsou v pilotu dobré na nalezení dealu, ne na jeho doložení.
5. **Vztah správce × fond je třeba upřesnit u každého záznamu.** U KAYA, Miton a J&T není jisté, která právnická osoba
   je správce. U J&T je v záznamu fondový vehikl SICAV. Pro škálování: pole `registry` = správce,
   fondové vehikly zvlášť ve `funds[].registry`.
6. **Kapitál potřebuje víc typů `basis`:** přibyly `previous_fund_size` (aktuální fond neznámý) a `portfolio_value`
   (Miton: hodnota portfolia, ne volný kapitál). Bez `basis` by čísla nebyla porovnatelná.
7. **Měna neuvedená ve zdroji** („0.5-2m", „17M") → `currency_assumed: true`. Údaj se nezahazuje, ale je označený.
8. **Kandidáty z „vlastní znalosti" (i mojí) nepovažovat za fakta.** Dva ze tří takových tipů byly chybné
   (Pointer neexistuje, NRF nebyl investor). Pravidla je vyřadila, ale kandidát by měl mít vždy zdroj.

### Doplněno po nezávislém review (Mac Claude, 2026-10-22)

9. **Datum zdroje je povinné, `undated` jen u webu investora.** Kapitál Lighthouse byl z článku ze 7. 6. 2019,
   ale v záznamu stál jako `undated`, takže zastaralost nešla poznat. `build.py` teď měří aktuálnost:
   ≤ 24 měsíců / 24–36 / > 36 = zastaralé / nedatováno.
10. **Ověřovatel musí být „slepý".** Agent B viděl citace agenta A, takže mohl jen potvrdit, že citace na stránce je.
    Ve v2 dostane ověřovatel jen tvrzení + URL a citaci si najde sám.
11. **Pravidlo „agregátor (tier C) nestačí" platí jen pro důkaz investice (I2).** Ostatní pole z tieru C jsou povolená,
    ale v tabulce jsou označená tierem, aby šla filtrovat.
12. **Sídlo ≠ domicil fondu.** `country` = sídlo týmu / správcovské firmy. Lucemburské GP a fondy (KAYA, Tensor, N1)
    patří do `funds[].domicile`, aby různí ověřovatelé nerozhodovali zemi různě.
13. **Rozsah vzorku se musí dodržet i u zařazení.** Genesis Capital je platný PE investor, ale vzorek byl
    definován jako VC-typy (§6). Proto `decision = out_of_scope`: do plné DB patří, do počtu ve vzorku ne.
14. **Citlivost okna aktivity:** při 24 měsících místo 36 by ze vzorku vypadl jen Impulse (poslední doložený deal 12/2023).
