# Review od Mac Clauda + shrnutí nezávislého řešení

Autor: Claude Code na Macu (Opus 5.5), 22. 10. 2026. Hodnocený stav: `main` @ `4931ed8`.
Kontext: na Macu vzniklo **nezávislé řešení stejného zadání A** na stejném vzorku (VC v ČR). Obě relace pracovaly odděleně a výsledky se porovnaly až dodatečně. Mac řešení zatím není na GitHubu (lokálně `~/Desktop/clientelo-databaze-investoru`, 14 commitů), proto jsou jeho klíčová čísla níže.

## 0. Nejzávažnější nálezy (TL;DR)

1. **Ruční kontrola člověkem chybí v obou řešeních.** Tady 0/58. Na Macu ji udělal Claude, což také není „ručne overená vzorka“. Bez ní není A10 splněné.
2. **Kontrola aktuálnosti nestačí, když se datum zdroje zapíše jako `undated`.** Lighthouse: kapitál 23 mil. EUR je z článku CzechCrunch **ze 7. 6. 2019**, v záznamu je `undated`.
3. **Ověřovací agent B není slepý.** Vidí celé záznamy včetně citací agenta A, takže může „odkývat“ podstrčený text. Na Macu ověřovatel dostal jen hodnotu + URL a citaci si musel najít sám.
4. **Odhad nákladů je pravděpodobně 2–5× podhodnocený.** `subagent_tokens` ze statistik agentů nejsou účtované tokeny. Agentní smyčka posílá celý kontext znovu při každém volání nástroje.
5. **Genesis Capital (`pe`) je zařazený ve vzorku, jehož rozsah PE nezahrnuje** (PLAN §6: `vc, cvc, public_vc, private_investor`). Počet 22 zařazených by měl být 21.

## 1. Nezávislé Mac řešení v kostce (pro porovnání)

| | Mac | toto repo |
|---|---|---|
| kandidáti / zařazeno | 30 / 17 | 29 / 22 |
| okno aktivity | 24 měsíců | 36 měsíců |
| strojová kontrola citací | 190/190 (po opravě 3 chyb checkeru) | 218/226 doslova |
| ověřovatel: pole doložená zdrojem | 176/190 = 92,6 % (14 částečně, 0 nedoloženo) | 104/121 = 86 % |
| ruční kontrola (Claude, vzorek losovaný předem) | 37/40 faktů, 17/18 zařazení, shoda s ověřovatelem 90 % | 0/58 |
| aktuálnost (věcná pole) | 15 aktuálních, 5 zastaralých, **43 nedatovaných** z 63 | neměřeno |
| NULL_MISSED (vůči tomuto repu) | 3 z 9 prázdných polí (tiket Rockaway, tiket a web Lighthouse) | 6/14 |
| opravy | 22 v `corrections.json` (styl převzatý odsud) | 38 |
| náklady svět | ≈ 90 tis. EUR (50–150 tis.), LLM $0,4–1,0 / kandidát | 60–70 tis. EUR, $0,30 / kandidát |

**Shoda v zařazení:** 15 subjektů (Credo, Czech Founders, DEPO, Inven, J&T, KAYA, Lighthouse, Miton, Nation 1/N1, Presto, Purple, Reflex, Rockaway, Tensor, Tilia).
- **Jen toto repo:** Aspire11, Pale Fire, Springtide, Y Soft Ventures, ZAKA VC (Macu chyběli) + Impulse a Genesis (rozdíl v pravidlech).
- **Jen Mac:** JIC Ventures, i&i Bio (tady chybí) + Orbit (Mac ho nakonec také vyřadil novým pravidlem V12 = vaše E3).
- **Odhad populace (Lincoln-Petersen)** ≈ 17·21/15 ≈ 24 aktivních VC-typových investorů. Každé řešení samo pokrylo ~70–85 %. **Úplnost se ztrácí při výběru kandidátů, ne při rešerši.**

**Co Mac převzal odsud:** `corrections.json`, venture debt jako explicitní pravidlo, zdroj AIN.ua (2024) a IČO 07723172 pro Nation 1 (ověřeno: ARES Smart Management VC s.r.o., Národní 135/14 = adresa Nation1 u CVCA), metriku vynechaných údajů.

## 2. Review (body 1–4 z INBOXu)

### 2.1 Pravidla zařazení a vyřazení (PLAN §2)

- **Rozsah vzorku vs. Genesis:** viz TL;DR 5. Buď Genesis vyřadit („mimo rozsah vzorku“), nebo rozšířit rozsah v §6 a zdůvodnit.
- **Sídlo vs. domicil fondu chybí.** KAYA (GP lucemburský), Tensor (GP a fond LU, PitchBook uvádí HQ Niederanven), i&i Bio („a Luxembourg-based venture capital firm“) a N1 (lucemburské fondy). Dva ověřovatelé tyto případy na Macu rozhodli různě. Návrh: `country` = tým a správcovská firma, `fund_domicile` zvlášť.
- **E6 (36 měsíců) × aktivní investor:** Impulse má poslední jasný deal 12/2023. Pro „skutečného investora“ k obchodnímu kontaktu je to hraniční. Mac zvolil 24 měsíců. Ani jedno není špatně, ale v README stojí za to zmínit citlivost: kolik subjektů by vypadlo při 24 měsících (Impulse, možná další).
- **Tier C:** pravidlo §7.4 („agregátor nestačí“) platí jen pro důkaz investice. U Impulse jsou ale sektory a tiket jen z Vestbee (C) a u Tensoru je důkaz DYNANIC z Dealroom (C). Sjednotit: buď pravidlo pro všechna pole, nebo výslovně jen pro I2.
- **Neidentifikovatelný kandidát:** dobře vyřešeno přes `I1` jako `exclusion_rule` (Mac musel doplnit V11).

### 2.2 Namátková kontrola záznamů (mimo váš náhodný vzorek)

| záznam | zjištění | závažnost |
|---|---|---|
| **nation1** | IČO 07723172 odvozené z výsledku vyhledávání (PDF EIF), které agent podle `notes` **neotevřel**. To je v rozporu s pravidlem „jen otevřené zdroje“. Výsledek ale sedí: adresa v ARES odpovídá adrese Nation1 u CVCA (https://cvca.cz/en/membership/). Doplnit tento zdroj místo PDF. | střední (postup), výsledek OK |
| **lighthouse** | `capital` 23 mil. EUR: zdroj cc.cz je **ze 7. 6. 2019**, v záznamu `undated`. Údaj je 7 let starý a nedá se poznat jako zastaralý. | **vysoká** |
| **tensor** | Důkaz DYNANIC: `app.dealroom.co/news/...` vrací bez přihlášení **HTTP 403** (Mac, 22. 10.). Je to agregátor (tier C) a sporně „veřejně dostupný“. Druhý důkaz (Wultra, Forbes 2025-09-18) je zmínka v rozhovoru („ještě před uzavřením fondu uskutečnil Tensor několik investic…“), ne datovaný deal; datum = datum článku. Aktivita je doložená, ale slabě. Lepší zdroj: AppFactor (lead, 02/2026) nebo ValkaAI (Seznam Zprávy 24. 2. 2026), obojí Mac ověřil. | střední |
| **zaka** | Promakhos: na zaka.vc/news je datum **04/23/2025**, v záznamu 2025-04-28. Yenmo (Vestbee 10. 3. 2025) sedí. Tiket €250–300k je z článku o fundraisingu (7/2024), tedy plán, ne praxe. | nízká |
| **credo** | bez nálezu (shoduje se s Mac záznamem: IČO 28538137, Theorema 3/2026, Supernova 9/2025) | – |
| **impulse** | Zdůvodnění v `manual_check.csv` stále zmiňuje Safetica, i když README říká, že důkaz byl odstraněn. | nízká |

**Formát listu pro ruční kontrolu:** u řádků `decision` je ve sloupci `quote` zdůvodnění agenta, ne citace ze zdroje (shoda se stránkou 0 % u Credo, Impulse i Lighthouse). Kontrolor ho snadno vezme jako doslovný text zdroje. Navrhuji sloupec přejmenovat na `rationale`, případně přidat skutečnou citaci.

### 2.3 Metodika přesnosti a odhad nákladů

- **Metrika A** je dobře rozdělená (ok / wrong / unverifiable / null_ok / null_missed) a přísnější než Mac (měří i vynechané údaje). Ale **ověřovatel B vidí citace agenta A**, takže SUPPORTED může znamenat jen „citace je na stránce“, ne nezávislé ověření. Doporučuji ověřovateli posílat jen tvrzení + URL.
- **Metrika B/C** (proti člověku) je správný návrh, ale bez vyplnění nemá žádné číslo. Do odevzdání je to nejslabší bod.
- **Aktuálnost** se neměří. `source_date: undated` u 2019 článku ukazuje, že ji nelze měřit ani zpětně. Návrh: `STALE` = zdroj starší 24 (36) měsíců u kapitálu a tiketu.
- **Náklady:**
  - `~48 tis. tokenů / kandidát` je statistika agenta, ne účtovaný vstup.
  - Při ~20 voláních nástrojů a kontextu, který narůstá s 5–6 kandidáty v jednom agentovi, je účtovaný vstup řádově 10× větší (většinou cache reads za $0,20 / 1 M u Opus 5.5).
  - Mac model, kde každý kandidát má vlastní běh: ≈ $0,87 (Opus 5.5) / $0,48 (Sonnet 5.5) na kandidáta včetně ověření.
  - **Cena vyhledávání není předpoklad:** ceník Anthropic (22. 10. 2026) uvádí web search $10 / 1 000 dotazů a web fetch bez příplatku.
- **Rate limity:** Mac pilot narazil na HTTP 429 už při 2 paralelních ověřovatelích. Ve „20 paralelních agentech“ je to reálné omezení času běhu.

### 2.4 Co by vytkl hodnotitel

1. Chybí ruční kontrola (výslovný požadavek).
2. Genesis v počtu zařazených (nekonzistence se svým plánem).
3. Zastaralé hodnoty bez data (Lighthouse), tedy „spolehlivost“ jen na půl.
4. Důkazy z agregátorů za přihlášením (Dealroom 403) u požadavku „výhradně verejne dostupné dáta“.
5. **README** je silné: konkrétní tabulka chyb včetně vlastních chyb orchestrátoru, prompt injection, auditovatelné opravy. Slabší místo: role „Já“ je napsaná za uživatele a ten by ji měl potvrdit vlastními slovy.

## 3. Kontrola proti zadání (bod 5a: nezávisle, před čtením `docs/requirements-check.md`)

Mac provedl tuto kontrolu nejdřív pro **vlastní** řešení. Bylo commitnuto dřív, než otevřel váš soubor; výsledek je v `docs/requirements-check.md` v Mac repu, zatím jen lokálně. Stejný rozpis aplikovaný na **toto** repo:

| # | požadavek | stav | důvod |
|---|---|---|---|
| A1 | databáze VC, PE, FO, angel, soukromí investoři | ⚠️ | typy v plánu ✅; data jen VC (+ Genesis PE mimo rozsah) |
| A2 | každý záznam skutečný investor | ✅ | agent B 20/23; negativní kontroly vyřazeny |
| A3 | sektor, co, v jaké výši, kapitál, odkud | ⚠️ | zdroj u každého vyplněného údaje ✅; null u 8 polí; Lighthouse kapitál zastaralý bez data |
| A4 | začít plánem | ✅ | první commit `b5ace12` = plán |
| A5 | pravidla kdo ano / ne | ✅ | I1–I4, E1–E8 (+ výhrady §2.1) |
| A6 | jak ověřit pravost a zařazení | ✅ | 5 kroků, metriky |
| A7 | odhad okruhu, počtu, spolehlivosti + z čeho | ⚠️ | CVC a soukromí investoři bez zdroje (podklad: GCV 2025, 2 344 aktivních korporátních investorů v 2024; Altrata 2025, 510 810 UHNW osob) |
| A8 | ověřit na menší vzorce | ✅ | |
| A9 | u každého záznamu zdroj + datum dokládající investici | ⚠️ | 22/22 datovaný deal; Tensor slabě (agregátor 403 + zmínka v rozhovoru) |
| A10 | přesnost na ručně ověřené vzorce | ❌ | 0/58 vyplněno |
| A11 | odhad nákladů svět | ⚠️ | struktura ✅; tokeny agenta ≠ účtované tokeny |
| A12 | výhradně veřejná data | ⚠️ | Dealroom app vrací bez přihlášení 403 |
| G1 | README o práci s AI (pokyny, kontrola, chyby) | ✅ | |
| G2 | nejasnosti rozhodnout a zdůvodnit | ✅ | |
| G3 | co chybí | ✅ | |
| G4 | v repu plán, data se zdrojem u každého údaje, výsledek měření | ⚠️ | výsledek měření bez ruční části |
| G5 | průběžná historie commitů | ✅ | po krocích; e-mail autora v pořádku, jméno jen „vital“ (kosmetické) |
| G6 | `ai-log` export | ❌ | |
| G7 | veřejné repo | ❌ | souhlas: pod osobním účtem, ne `wristradar26-creator` |

## 4. Porovnání s Android Claudem (bod 5b: po přečtení `docs/requirements-check.md`)

| bod | Android | Mac | kdo má pravdu |
|---|---|---|---|
| ruční kontrola | ❌ | ❌ (Mac u sebe nejdřív ⚠️, po přečtení vašeho souboru přehodnotil) | **Android**: AI kontrola není ruční |
| z čeho odhad vychází | ⚠️ CVC a soukromí investoři | Mac měl stejnou díru u sebe a přehlédl ji | **Android**; Mac doplnil GCV + Altrata (výše) |
| cena search API | ⚠️ předpoklad | ověřeno z ceníku | **Mac** |
| historie commitů | ✅ | ⚠️ u Mac repa (e-mail autora = hostname počítače) | **shoda**: u tohoto repa je e-mail v pořádku; problém má jen Mac repo |
| A3 pokrytí | ⚠️ | ⚠️ + Lighthouse zastaralý | Mac: kontrola musí jít i do dat zdroje, nejen „zdroj existuje“ |
| A9 důkaz investice | ✅ 22/22 | ⚠️ Tensor | Mac: počet ✅, kvalita u 1 záznamu slabá |
| A12 veřejná data | ✅ „všech 226 se stáhlo bez přihlášení“ | ⚠️ Dealroom 403 | rozpor: z Macu 22. 10. vrací 403. Mohl to být rozdílný User-Agent nebo blokace; stojí za to ověřit znovu |
| Genesis | nezmíněno | ⚠️ A1 | Mac |
| veřejné repo pod osobním účtem | ✅ dobrý postřeh | převzato | Android |

**Co Android přehlédl:** Genesis mimo rozsah, zastaralý a nedatovaný kapitál Lighthouse, kvalitu důkazu u Tensoru, Dealroom 403 a účtování tokenů.
**Co přehlédl Mac (u sebe):** ruční kontrola ≠ AI kontrola, odhad bez podkladu u soukromých investorů.
