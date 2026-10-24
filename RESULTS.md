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

**Výsledek (ruční kontrola provedena 2026-10-23, Vitalij Ljubačivskyj):**

Kontrolovalo se 6 investorů (Credo, Impulse, Lighthouse, N1, Tensor, ZAKA) × 5 údajů ze zadání
(doklad investice, sektor, fáze, výše investice, kapitál). Každý údaj byl porovnán se zdrojem otevřeným proklikem.

| | výsledek |
|---|---|
| | výsledek |
|---|---|
| **odpovědí celkem** | **30** (6 investorů × 5 údajů) |
| **sedí** | **29** |
| nesedí | 0 |
| nejde ověřit | 1 (tiket Tensoru je „neuvedeno"; nešlo ověřit, že veřejně opravdu neexistuje) |
| investor doložen (doklad investice sedí) | 6/6 |

*Oprava 2026-10-24:* dříve tu stálo „35/35". Odpověď „Doklad, že investuje" se v programu počítala dvakrát
(jako rozhodnutí o zařazení i jako doklad investice). Upozornil na to Mac Claude ve 2. review; výpočet je opravený.

**Jak to číst:**
- Kontrolují se **finální data po opravách**. Surový výstup AI měl 86 % (A), opravy přes ověřovatele a pravidla ho
  dotáhly na úroveň, kterou ruční kontrola nerozporovala.
- Vzorek je malý. Při 29 ověřitelných údajích bez chyby je 95% interval spolehlivosti zhruba **90–100 %**
  („pravidlo tří": 3/29). Na tvrzení „100 %" to nestačí, na tvrzení „kolem 90 % a víc" ano.
- **Vzorek 1 není úplně „čistý".** Byl vylosovaný předem, ale Mac Claude ve svém 1. review náhodou kontroloval právě
  tyto investory (Credo, Lighthouse, N1, Tensor, ZAKA) a jeho nálezy se opravily. Člověk tak kontroloval záznamy, které
  prošly kontrolou navíc. Výsledek proto platí pro takto dvakrát zkontrolovaná data, ne nutně pro typický záznam.
- **Proto vzorek 2:** 6 dalších investorů vylosovaných z kol 2–3 (ARX, BHM, Flying Founders, Jiří Hlavenka, JIC Ventures,
  Soulmates), kterých se žádné review navíc netýkalo. Prošli jen běžným postupem. List: „Ruční kontrola 2.xlsx".
  **Stav: čeká na vyplnění.**
- List „Sporné" (4 hraniční rozhodnutí: Pale Fire, StartupYard, NRF, Genesis) zůstal bez vyjádření a rozhodnutí v nich
  zůstávají podle pravidel.

### C) Shoda ověřovacího agenta s člověkem

Počítá se ze stejného listu, z polí, která se po ověření neměnila. Na tomhle čísle stojí škálování: pokud agent B
souhlasí s člověkem v ≥ 95 % případů, stačí lidsky kontrolovat jen statistický vzorek a sporné body.

**Výsledek (vzorek 1): shoda 16/17 = 94 %.** Jediná neshoda: tiket Tensoru. Ověřovatel ho označil „null_ok" (veřejně
neexistuje), člověk „nejde ověřit". Nejde o rozpor ve faktech, jen o přísnost: člověk nechtěl potvrdit, že údaj neexistuje.
*(Dříve „22/23 = 96 %", také se dvakrát počítala odpověď u dokladu investice.)*

- Ve faktech se AI ověřovatel s člověkem neshodl ani jednou. Přesná shoda je 94 %, těsně pod prahem 95 %.
- 17 porovnání je na pevný závěr málo. Vzorek 2 přidá dalších ~30 porovnání se **slepým** ověřovatelem.
- Pro odhad nákladů (§5) z toho plyne: lidská kontrola vzorku a sporných případů je nutná. Počítá s ní a nespoléhá jen na AI.

### D) Úplnost (recall) — křížově s nezávislým řešením na Macu

Druhá session Claude Code (Mac) řešila stejné zadání na stejném vzorku nezávisle. Výsledky se porovnaly až dodatečně.
Dva nezávislé „úlovky" stejné populace umožňují odhadnout její velikost (Lincoln–Petersen):

| | počet |
|---|---|
| zařazeno zde (VC-typy) | 21 |
| zařazeno na Macu | 17 |
| v obou | 15 |
| **odhad populace aktivních VC-typových investorů v ČR** | **21 · 17 / 15 ≈ 24** |
| odhad úplnosti tohoto řešení (původní, **vyvráceno v §3b**) | 21 / 24 ≈ 88 % → změřeno 66 % |

- Chybí tu **JIC Ventures** a **i&i Bio**. Našel je jen Mac.
- **Ztráta úplnosti vzniká při výběru kandidátů, ne při rešerši:** kdo se nedostane do seznamu kandidátů,
  v databázi nebude. Pro škálování to znamená brát kandidáty z víc nezávislých zdrojů (registry, portfolia EIF,
  média) a průnik průběžně měřit.
- Pozor: obě session čerpaly z podobných veřejných seznamů. Úlovky tedy nejsou úplně nezávislé a populace
  je spíš podhodnocená.
- **Potvrzeno oficiálním katalogem CzechStartups** ([docs/dalsi-zdroje-analyza.md](docs/dalsi-zdroje-analyza.md)).
  Katalog obsahuje 19 investorů z mého vzorku a ~17 dalších českých VC-like subjektů, které ve vzorku nejsou.
  **Změřeno ve fázi 2 (§3b): úplnost fáze 1 vůči katalogu je 19/29 = 66 %.**

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

## 3b. Fáze 2: nové kandidáty z katalogu a registru, pokyny v2, slepý ověřovatel

Po analýze dalších zdrojů ([docs/dalsi-zdroje-analyza.md](docs/dalsi-zdroje-analyza.md)) jsem pilot rozšířil o 30 kandidátů:
- 20 z katalogu CzechStartups,
- 8 z registru fondů ČNB,
- JIC Ventures a i&i Bio z Mac řešení.

Rešerše běžela podle [pokynů v2](docs/prompt-research-agent-v2.md). Ověřoval **slepý** ověřovatel ([v2](docs/prompt-verifier-agent-v2.md)),
který viděl jen tvrzení + URL ([data/blind/](data/blind/)) a citaci si musel ve zdroji najít sám.

### Výsledek

| | počet |
|---|---|
| kandidáti | 30 |
| **zařazeno (po opravách)** | **15**: 11 `vc`, 2 `family_office`, 1 `cvc`, 1 `angel_syndicate` |
| neaktivní (E6) | 4: NEWTON, KB SmartSolutions, UP271, Opifer |
| vyřazeno | 8: I2 ×4 (AgriBoom, Partners Innovation, Direct PRO, The Seeders), E5 ×2 (Double Speed, CZEGG), E4 (Garage Angels), I4 (EMUN TECH) |
| mimo rozsah (bez českého týmu) | 3: 3TS (AT), mAccelerator (PL), Limerock (SK) |

**Celkem v databázi: 36 zařazených investorů** (21 z fáze 1 + 15 z fáze 2).

### Přesnost surového výstupu v2 (slepý ověřovatel, `python src/measure.py`, část E)

| pole | ok | chyba | neověřitelné | null, ale existuje | přesnost |
|---|---|---|---|---|---|
| rozhodnutí | 15 | 1 | 0 | – | 94 % |
| typ investora | 14 | 2 | 0 | – | 88 % |
| registrace | 15 | 1 | 0 | 0 | 94 % |
| sektory | 14 | 1 | 0 | 1 | 93 % |
| fáze | 13 | 2 | 0 | 0 | 87 % |
| tiket | 7 | 1 | 1 | 1 | 88 % |
| kapitál | 3 | 4 | 3 | 1 | 43 % |
| nejnovější investice | 15 | 1 | 0 | 0 | 94 % |

- **Přesnost záznamu 13/16 = 81 %, přesnost polí 67/77 = 87 %**, správně vyřazené 11/14.
- **v1 × v2:**
  - Celková přesnost polí je podobná (86 % × 87 %), ale v2 měřil **přísnější, slepý** ověřovatel. Proti v1 (horní odhad) je to tedy zlepšení.
  - **Chyby přepočtu měn zmizely úplně** (v1: 8 ze 17 chyb, v2: 0), protože přepočet dělá kód.
  - Chyby v sektorech a fázích klesly z 5 na 3.
- **Nová slabina = kapitál (43 %).** 4 ze 7 chyb jsou cílová velikost fondu označená jako skutečná. Schéma pro cíl nemělo
  hodnotu `basis`, doplněno `target_fund_size` (PLAN §7.17). Agenti cíl správně uváděli v textu, chyba byla v mém schématu.
- **Chyby v mých pokynech v2, které odhalil slepý ověřovatel:**
  - andělské skupiny jako `angel` (Garage Angels je spolek, kde investují členové osobně, tedy E4; PLAN §7.15),
  - `cvc` příliš úzké pro banky (PLAN §7.16).
- 1 nález „null_missed" (Tachles, kapitál) je artefakt: slepé podklady vznikají před přepočtem měn. Hodnota v datech je.

### Úplnost změřená proti oficiálnímu katalogu (`python src/recall.py`)

| | |
|---|---|
| položky katalogu CzechStartups | 52 (10 bez rešerše: asociace, crowdfunding, zahraniční fondy podle popisu v katalogu) |
| z katalogu prošlo pravidly (referenční množina) | **29** |
| **úplnost fáze 1** (původní výběr kandidátů) | **19/29 = 66 %** |
| chyběly | Fazole, Flying Founders, Look AI, Lumus, PurposeTech, QQ Capital, RSJ, Seed Starter ČS, Soulmates, Tachles |
| úplnost **katalogu** vůči všem 36 zařazeným | 29/36 = 81 %; v katalogu chybí ZAKA, Aspire11, Aternus, i&i Bio, Jet Venture, JIC, JSK |

- **Původní odhad 88 %** z porovnání s Mac řešením byl o 22 bodů optimistický. Odhad 55–75 % z analýzy zdrojů (před fází 2) se potvrdil.
- **Ani oficiální katalog není úplný (81 %).** Úplnost dá teprve kombinace víc nezávislých zdrojů kandidátů:
  média + katalog + registr ČNB + druhé nezávislé řešení. Každý z nich přidal investory, které ostatní neměly.
- Lincoln–Petersen (fáze 1 × katalog) odhaduje ~32 aktivních investorů, ale nalezeno je jich 36. Zdroje nejsou nezávislé,
  takže odhad podhodnocuje. Skutečná populace aktivních VC-like investorů v ČR je **≥ 36**, realisticky 40–45.

### Náklady fáze 2

| | tokeny | volání nástrojů | čas agentů |
|---|---|---|---|
| rešerše (5 agentů, 30 kandidátů) | 922 tis. | 394 | 56 min |
| slepé ověření (5 agentů) | 658 tis. | 191 | 28 min |
| **na kandidáta** | **~53 tis.** | **~20** | **~2,8 min** |

- Spotřeba na kandidáta je podobná jako ve fázi 1 (~48 tis.). Odhad nákladů v §5 platí.
- **Podíl zařazených z nekurátorovaného vstupu je 15/30 = 50 %.** To přesně odpovídá předpokladu 50 % v odhadu nákladů (§5).

## 3c. Fáze 3: private equity, family office a jednotliví andělé

Fáze 1–2 ověřily pravidla jen na VC-like investorech. Fáze 3 je ověřila na zbylých typech ze zadání:
13 kandidátů, [pokyny v3](docs/prompt-research-agent-v3.md) (pravidla pro PE, FO a anděly včetně GDPR) a slepý ověřovatel.

### Výsledek

| typ | kandidáti | zařazeno | vyřazeno / neaktivní |
|---|---|---|---|
| private equity | Jet Investment, ARX Equity Partners, Benson Oak (+ Genesis z fáze 1) | **Jet Investment, ARX, Genesis** | Benson Oak: poslední investice 2011 (E6) |
| family office | TCF Capital, BHM Group, J&T Family Office, Marperger | **TCF, BHM** (oba jako `private_investor`, PLAN §7.21) | J&T FO: správa majetku, sám neinvestuje (I4); Marperger: poslední deal 2019 (E6) |
| jednotliví andělé | Hlavenka, Obluk, Dendis, Najvárek, Rostock-Poplar | **Jiří Hlavenka, Miloš Dendis, Michael Rostock-Poplar** | Obluk, Najvárek: méně než 2 doložené osobní investice (I3) |

**Celkem v databázi: 43 investorů** (fáze 1: 22 vč. Genesis, fáze 2: 15 bez Jet Venture, fáze 3: 7 nových + Jet Investment
sloučen s Jet Venture). Složení:

| typ | počet |
|---|---|
| VC fond | 25 |
| soukromý investor / investiční skupina | 5 |
| korporátní VC | 4 |
| private equity | 3 |
| anděl (fyzická osoba) | 3 |
| family office | 2 |
| andělský syndikát | 1 |

### Přesnost surového výstupu v3 (slepý ověřovatel, `measure.py` část F)

- **Rozhodnutí zařadit / vyřadit: 7/7 zařazených a 5/5 vyřazených správně (100 %).**
- **Přesnost polí 25/27 = 93 %.**
- Přesnost záznamu je jen 5/7 = 71 %, ale obě chyby jsou **typ family office × soukromý investor** (TCF, BHM).
  Nejde o fakta, ale o nejasnou hranici v plánu, kterou fáze 3 odhalila a PLAN §7.21 ji upřesnil.
- Kapitál: TCF uvádí „720 mil. EUR", ale je to hodnota podílu v Rohlik Group, ne kapitál k investování.
  BHM uvádí „1,1 mld. EUR", ale jsou to aktiva celé skupiny. Obojí označeno správným `basis`.

### Ověření odhadu spolehlivosti z plánu (pokrytí polí podle typu, `build.py`)

| typ | počet | sektory | tiket | kapitál |
|---|---|---|---|---|
| VC fond | 25 | 96 % | 84 % | 84 % |
| soukromý investor | 5 | 100 % | 60 % | 100 % |
| korporátní VC | 4 | 100 % | 75 % | 25 % |
| private equity | 3 | 100 % | 67 % | 100 % |
| anděl | 3 | 33 % | 33 % | 0 % (úmyslně, GDPR) |
| family office | 2 | 100 % | 0 % | 0 % |

- **Odhad z PLAN §5 se potvrdil:** VC a PE zveřejňují tiket i kapitál nejčastěji, family office a andělé skoro nikdy.
- U PE je kapitál vždy známý (velikost fondu je veřejná), tiket ne. Fondy uvádějí hodnotu cílových firem, ne vlastní vklad.
- Korporátní VC zveřejňují kapitál jen výjimečně (rozhoduje o něm mateřská firma).
- U andělů je kapitál prázdný úmyslně: je to osobní majetek. Zjišťovat ho by bylo proti GDPR a pro zadání zbytečné.

### Náklady fáze 3

| | tokeny | volání nástrojů | čas agentů |
|---|---|---|---|
| rešerše (3 agenti, 12 kandidátů) | 537 tis. | 185 | 28 min |
| slepé ověření (3 agenti) | 407 tis. | 119 | 15 min |
| **na kandidáta** | **~79 tis.** | **~25** | **~3,6 min** |

PE, FO a andělé stojí **~1,6× víc než VC** (~79 tis. vs. ~50 tis. tokenů). Mají méně veřejných zdrojů a víc slepých
uliček, např. neexistující „TCF Capital" v rejstříku nebo deal pod jiným jménem vozidla. Odhad nákladů pro celý rozsah
(§5) s tím počítá jen částečně, proto je horní hranice 125 tis. EUR realističtější než dolní.

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
