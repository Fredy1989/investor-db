# Odevzdání: souhrn odpovědí na zadání A

Tento dokument odpovídá bod po bodu na všechny požadavky z e-mailu. U každého je odkaz, kde je odpověď podrobně.
Stav k 2026-10-22.

---

## Požadavky na odevzdání (z e-mailu)

| požadavek | stav | kde |
|---|---|---|
| odkaz na veřejný repozitář na GitHubu | ⏳ před odesláním (repo je zatím soukromé) | — |
| **plán** | ✅ | [PLAN.md](PLAN.md) |
| **data ze vzorku se zdrojem u každého údaje** | ✅ | [data/Databaze_investoru.xlsx](data/Databaze_investoru.xlsx) (pro čtení), [data/investors_cz_vc.csv](data/investors_cz_vc.csv) a [data/records/](data/records/) (zdroj, datum, citace u každého údaje) |
| **výsledek měření přesnosti** | ✅ AI ověření / ⏳ ruční část | [RESULTS.md §3, §3b](RESULTS.md), [data/accuracy.csv](data/accuracy.csv) |
| kód s průběžnou historií commitů | ✅ | [src/](src/), `git log` (18+ commitů po krocích) |
| `ai-log/`: export konverzací s Claude Code | ⏳ export na konci | [ai-log/](ai-log/) |
| README: jak se pracovalo s AI, pokyny agentům, kontrola výstupu, kde se AI mýlila | ✅ | [README.md](README.md), [docs/](docs/) |
| nejasnosti rozhodnout a zdůvodnit | ✅ | README „Rozhodnutí…", níže |
| uvést, co v řešení chybí | ✅ | README „Co v řešení chybí", níže |

---

## Zadání A: odpovědi

### 1. Kdo v databázi bude a kdo ne (pravidla)

Investor = subjekt, který **investuje kapitál do soukromých firem za podíl, dělá to opakovaně nebo k tomu má vyčleněný kapitál
a má to doložené**. Podrobně v [PLAN.md §1–2](PLAN.md).

- **Zařazení (musí platit vše):**
  - I1: subjekt existuje (registr, IČO),
  - I2: má doloženou investici za posledních 36 měsíců (zdroj + datum),
  - I3: investování je jeho hlavní činnost,
  - I4: investuje do soukromých firem.
- **Vyřazení (stačí jedno):**
  - E1 crowdfunding,
  - E2 akcelerátor bez fondu,
  - E3 jen dluh,
  - E4 poradce / asociace / síť,
  - E5 jen burza nebo reality,
  - E6 neaktivní,
  - E7 strategický kupec,
  - E8 duplicita.
- **Typy:** VC, private equity, korporátní VC, státní VC, family office, anděl, andělský syndikát, velký soukromý investor.

Pravidla se v praxi osvědčila: vyřadila 23 z 59 kandidátů, mezi nimi crowdfundingové platformy, neexistující subjekt,
fond, který nikdy neinvestoval, a akciový fond se slovem „rizikový" v názvu. Odhalila i ~20 tis. vázaných zástupců
z registru ČNB, které jiná AI doporučovala jako „investory". Jsou to ale prodejci investičních produktů, ne investoři.

### 2. Jak se ověří pravost a správné zařazení

Pět vrstev, každou dělá někdo jiný, aby se chyby nesčítaly ([PLAN.md §4](PLAN.md), [README](README.md)):

1. **Rešeršní AI agent**: ke každému údaji URL, datum a **doslovnou citaci** ze zdroje. Chybějící údaj = prázdné pole, nikdy odhad.
2. **Strojová kontrola citací**: skript stáhne každý zdroj a hledá v něm citaci. Výsledek: 392 ze 425 doslova, **žádná vymyšlená URL ani citace**.
3. **Nezávislý ověřovací agent**: ve fázi 2 **slepý**, vidí jen tvrzení + URL a citaci si musí najít sám.
4. **Auditovatelné opravy**: 70 oprav v [corrections.json](data/corrections.json), u každé důvod a autor návrhu.
   Původní výstup AI zůstává beze změny v [records_raw/](data/records_raw/).
5. **Člověk**: ruční kontrola náhodného vzorku ([data/manual_check.csv](data/manual_check.csv), viz bod 6).

Navíc **druhé, úplně nezávislé řešení** stejného zadání jinou session Claude Code (Mac) a vzájemné review: [reviews/](reviews/).

### 3. Jaký okruh investorů jde z veřejných zdrojů získat, kolik jich bude a jak spolehlivě

Podrobně v [PLAN.md §5](PLAN.md):

| segment | odhad veřejně ověřitelných | spolehlivost | z čeho odhad vychází |
|---|---|---|---|
| VC | 5–7 tis. | vysoká | NVCA Yearbook (USA 3 417 firem) |
| private equity | 5–7 tis. | vysoká (existence, AUM), nízká (tiket) | Preqin (10 300+ správců PE vč. VC) |
| korporátní VC | 1,5–2 tis. | střední | Global Corporate Venturing (2 344 v roce 2024) |
| family office | 1,5–2,5 tis. | nízká: kapitál ani tikety nezveřejňují | Deloitte (8 030 single FO) |
| andělé | 15–30 tis. | nízká + GDPR (fyzické osoby) | EBAN (sítě ≈ 10 % trhu) |
| velcí soukromí investoři | 1–3 tis. | střední | vlastní odhad (bez přímého zdroje) |
| **celkem** | **30–50 tis.**, jádro VC/PE/CVC 12–16 tis. | | |

Pilot odhad spolehlivosti zpřesnil. Tiket je veřejný u ~72 % a kapitál u ~72 % zařazených. Family office a syndikáty je
zveřejňují nejméně. Rozhodnutí „je to investor" je spolehlivé (94–100 %), nejslabší je velikost kapitálu.

### 4. Ověření na menší vzorce

**VC-like investoři v Česku**, ve dvou fázích ([RESULTS.md](RESULTS.md)):

| | kandidáti | zařazeno | vyřazeno |
|---|---|---|---|
| fáze 1: kandidáti z médií a přehledů | 29 | 21 | 8 |
| fáze 2: oficiální katalog CzechInvest, registr ČNB, druhé řešení | 30 | 15 | 15 |
| **celkem** | **59** | **36** | **23** |

Výsledek je v [Databaze_investoru.xlsx](data/Databaze_investoru.xlsx). Jeden řádek = jeden investor:
sektor, do čeho investuje, typická výše investice, celkový kapitál a doklad investice (firma + datum).
**Kliknutím na hodnotu se otevře zdroj.**

### 5. U každého záznamu zdroj a datum, které dokládají, že subjekt investuje

✅ Všech 36 zařazených má **poslední doloženou investici s datem** (všechny po 2023-10-22) a odkazem na článek nebo
tiskovou zprávu (tier A/B). Agregátory (Crunchbase, Dealroom…) se smí použít k **nalezení** dealu, ne k jeho **doložení**.

### 6. Přesnost na ručně ověřené vzorce

| měření | kdo ověřoval | výsledek |
|---|---|---|
| A: fáze 1, surový výstup AI | ověřovací AI agent (viděl citace) | záznam **87 %**, údaje **86 %** |
| E: fáze 2, surový výstup AI (pokyny v2) | **slepý** AI ověřovatel | záznam **81 %**, údaje **87 %** |
| B: finální data po opravách | **člověk**, náhodný vzorek 6 investorů × 5 údajů | ⏳ vyplňuje se |
| C: shoda AI ověřovatele s člověkem | | ⏳ z téhož listu |
| úplnost proti oficiálnímu katalogu | skript | fáze 1 našla **66 %** investorů z katalogu |

Nejčastější chyby AI a jejich náprava: přepočet měn (přesunut z AI do kódu, chyby klesly z 8 na 0), cílová velikost fondu
vykázaná jako skutečná, sektory domyšlené z několika dealů. Rozbor je v [RESULTS.md §3](RESULTS.md).

### 7. Odhad nákladů na rozšíření na celý svět

Z naměřené spotřeby pilotu: ~50 tis. tokenů a ~20 volání nástrojů na kandidáta, polovina kandidátů projde pravidly.
Podrobně v [RESULTS.md §5](RESULTS.md).

| | jádro VC / PE / korporátní VC | celý rozsah vč. FO a andělů |
|---|---|---|
| kandidátů | ~30 tis. | ~100 tis. |
| AI + vyhledávání ($0,55–0,95 / kandidát) | 15–25 tis. EUR | 49–85 tis. EUR |
| lidská kontrola vzorku + sporné případy | ~9 tis. EUR | ~24 tis. EUR |
| vývoj (fronta, deduplikace, registry, monitoring) | 10–15 tis. EUR | 10–15 tis. EUR |
| **první naplnění celkem** | **≈ 35–50 tis. EUR** | **≈ 85–125 tis. EUR** |
| údržba | ≈ 40 % ročně | |

---

## Placené databáze: proč nejsou použité a kolik by stály

Při přípravě jsem zjišťoval (i s pomocí jiných AI, DeepSeek a Gemini), jestli data o investorech nejde jednoduše koupit.
Jde, ale za poplatek:

| zdroj | co nabízí | cena (ověřeno 2026-10-22) |
|---|---|---|
| **Apify: Startup Investor Database** (johnvc) | 10 469 investičních firem; AUM jen když ho firma zveřejní, tiket u kontaktů | **$0,04 / firma** (≈ $420 za celou databázi) + $0,02 / kontakt ([apify.com](https://apify.com/johnvc/startup-investors-data-scraper)) |
| Apify: Crunchbase „Instant DB" (memo23) | 19 000+ VC, andělé, FO, akcelerátory | od $8 / 1 000 záznamů |
| Apify: Venture Capital & Investor Data (datahyena) | VC fondy, typ, země, doména | od $20 / 1 000 |
| **Crunchbase Pro** | investoři, kola financování; export omezen (~2 000 řádků / měsíc) | **$49 / měsíc** při roční platbě ($588 / rok) |
| **Dealroom** | evropský ekosystém, investoři, exporty | **€12 500 / rok** (Premium, od 3 uživatelů) |
| **PitchBook** | nejúplnější VC/PE data vč. AUM a dealů | **$12–40 tis. / uživatel / rok** (ceník neveřejný, odhady odběratelů) |
| **Preqin** | PE, fondy, family office, LP | **~$25–80 tis. / rok** (medián smluv ~$49 tis.; ceník neveřejný) |
| OpenVC, NFX Signal | 20 000+ investorů | zdarma k prohlížení, **bez exportu** |

DeepSeek zmiňoval i Apify databázi „14 161 firem za $6,40 / 1 000". **Tu se mi nepodařilo dohledat**, proto ji neuvádím jako fakt.

### Proč jsem je nepoužil

1. **Zadání to vylučuje:** „Používajte výhradne verejne dostupné dáta." Placená databáze není veřejně dostupná.
2. **Licence nedovoluje data zveřejnit.** Výsledek musí být ve veřejném repozitáři. Crunchbase, PitchBook i Dealroom
   v licenci zakazují další šíření exportovaných dat.
3. **Agregátor nedokládá, že subjekt investuje.** Je to „přepis přepisu" bez zdroje u jednotlivého údaje.
   Spolehlivost je hlavní požadavek zadání a pilot ukázal proč:
   - údaje z agregátorů se lišily od primárních zdrojů (datum dealu, role ve kole, měna),
   - Apify databáze uvádí AUM jen tam, kde ho firma sama zveřejní, takže by stejně chybělo,
   - i tak by každý záznam musel projít stejným ověřením. Placená data by **ušetřila jen hledání kandidátů, ne ověření**.
4. **Stejný výsledek šel získat zdarma z oficiálních zdrojů:** katalog investorů CzechInvest a registr fondů ČNB.
   Fáze 2 ukázala, že právě tyhle zdroje nejvíc zvýšily úplnost.

### Kdy by se placená data vyplatila (při rozšíření na svět)

Jako **levný zdroj kandidátů**, ne jako výsledek:
- Celou Apify databázi (~10 tis. firem) lze stáhnout za ~$420 a pak ji projít stejným ověřením.
- Tím by se ušetřila část vyhledávání a zvýšila úplnost, která se podle pilotu ztrácí právě při výběru kandidátů.
- Ve výsledné databázi by ale zůstaly jen údaje doložené veřejným zdrojem.

PitchBook nebo Preqin za desítky tisíc dolarů ročně se vyplatí jen tehdy, když firma potřebuje data průběžně a nesmí je zveřejňovat.
Pro tuto úlohu ne.

---

## Proč je řešení v tomto stavu (hlavní rozhodnutí)

| rozhodnutí | proč |
|---|---|
| **vzorek = VC-like investoři v Česku** | zadání to navrhuje; český trh je dost malý na ruční kontrolu a znám ho |
| **ostatní typy (PE, family office, jednotliví andělé) jen v plánu, ne ve vzorku** | zadání chce plán pro celou databázi, ale ověření „na menší vzorce, např. VC fondech v jedné zemi"; pravidla pro ostatní typy jsou napsaná, na datech zatím neotestovaná (2 FO a 1 andělský syndikát se do vzorku dostaly přirozeně) |
| **chybějící údaj = prázdné pole, nikdy odhad** | spolehlivost je hlavní požadavek; vymyšlené číslo vypadá jako fakt |
| **investor = doložená investice za 36 měsíců** | „každý záznam musí být skutečný investor": tvrzení na webu nestačí, musí být vidět skutečná investice |
| **u každého údaje doslovná citace, kterou kontroluje stroj** | AI agenti umí vymýšlet zdroje; citace se dá automaticky ověřit |
| **přepočet měn dělá kód, ne AI** | v pilotu to byla nejčastější chyba AI |
| **dvě fáze pilotu** | po první fázi jsem zjistil, že jsem 34 % investorů vůbec nenašel; druhá fáze to změřila a opravila |
| **druhé nezávislé AI řešení + slepé ověření** | AI kontrolující samu sebe přehlíží vlastní chyby; nezávislé řešení našlo chyby, které moje kontrola minula |
| **žádné placené databáze** | viz předchozí sekce |

## Co v řešení chybí

- **Ruční kontrola člověkem** (měření B a C): list je připravený, vyplňuje se.
- **Ostatní typy investorů na datech** (PE, family office, jednotliví andělé): jen v plánu.
- **Export konverzace do `ai-log/`** a **zveřejnění repozitáře**: poslední kroky před odesláním.
- Hraniční případy k ručnímu dořešení: NEWTON University Angels, Longevitytech.fund, a u KAYA, Miton a J&T, která právnická osoba je správce.
