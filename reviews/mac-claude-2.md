# Review od Mac Clauda, 2. kolo (před odevzdáním)

Autor: Claude Code na Macu (Opus 5.5), 24. 10. 2026. Hodnocený stav: `main` @ `cd67913`.
Čísla jsou ověřená přímo v datech (`data/*.csv`, `data/records/`), ne v textech.

## Verdikt

**Řešení zadání A splňuje a je kvalitní.** Před odesláním je potřeba opravit **4 věci**, jinak se hodnotitel bude doptávat a u jedné může zpochybnit hlavní číslo. Odhad práce: 1–2 hodiny.

## 1. Kontrola proti zadání

| co zadání chce | stav | poznámka |
|---|---|---|
| databáze investorů všech typů | ✅ | 43 investorů: 25 VC, 5 soukromých investorů, 4 CVC, 3 PE, 3 andělé, 2 FO, 1 syndikát (ověřeno v CSV) |
| každý záznam je skutečný investor | ✅ | všech 43 má datovaný doklad investice; nejstarší 2023-12-20 (Impulse), tedy v okně 36 měsíců |
| sektor, do čeho, kolik, celkový kapitál | ⚠️ | VC a PE většinou ano. FO a andělé čísla nezveřejňují, což je vysvětlené. Hlavenka a Rostock-Poplar ale nemají ani sektor, viz §3 |
| odkud informace pochází | ✅ | odkaz a citace; texty typu „nenalezeno“ nebo „neuvádí se – osobní údaj“ nejsou údaje bez zdroje, to je v pořádku |
| plán: pravidla, ověřování, odhad počtu, z čeho vychází | ✅ | |
| ověření na vzorku jedné země | ✅ | 71 kandidátů ve 3 kolech |
| přesnost na **ručně** ověřeném vzorku | ⚠️ | hotové, ale viz §2 bod 1 |
| odhad nákladů na svět | ✅ | 85–125 tis. EUR; nezávislý Mac odhad ≈ 90 tis. EUR (50–150 tis.), $0,4–1,0 na kandidáta. **Sedí.** |
| jen veřejná data | ✅ | sekce o placených databázích s cenami je silná a předem odpovídá na otázku „proč jste nepoužili PitchBook“ |
| README o práci s AI | ✅ | čtivé, lidské, chyby AI ve skupinách, detaily v rozbalovacích sekcích |
| `ai-log`, veřejné repo | ❌ | víte o tom |

## 2. Co opravit před odesláním

**1. Ruční kontrola: čísla nesedí a vzorek je zkreslený.** Nejdůležitější bod.
- **Popis nesedí s čísly.** README a ODEVZDANI píšou „6 investorů × 5 údajů“ a „35 z 35 údajů“, ale 6 × 5 = 30. V `manual_check.csv` je 30 údajů + 6 rozhodnutí = 36 kontrol: 35 `ok`, 1 `unverifiable`, 0 chyb. Návrh textu: *„36 kontrol (6 rozhodnutí o zařazení + 30 údajů): 35 odpovídá zdroji, 1 nešlo ověřit, 0 chyb.“*
- **Vzorek nebyl čistý, a je to moje chyba.** INBOX mě v 1. kole žádal kontrolovat *jiné* záznamy než ruční vzorek. Já jsem ale zkontroloval přesně ty z něj (Credo, Lighthouse, Nation 1, Tensor, ZAKA). Moje nálezy se pak opravily (Lighthouse datum, Tensor doklad, Nation 1 IČO) a člověk kontroloval už opravené záznamy. **100 % proto popisuje záznamy, které prošly kontrolou navíc, ne typický záznam.**
- **Návrh:** ručně zkontrolovat 6–8 náhodných investorů z 2. a 3. kola, kterých se žádné review netýkalo (~30–40 min, Excel už je připravený). Výsledek uvést zvlášť a v textu poctivě říct, proč existují dva vzorky. Tohle je jediný bod, kde zkušený hodnotitel může zpochybnit hlavní číslo.

**2. ODEVZDANI.md má zastaralá čísla.** README a data mají správná:

| ODEVZDANI.md | skutečnost |
|---|---|
| „Stav k 2026-10-22“ | obsah z 23.–24. 10. |
| §2: „392 ze 425 citací“ | 494 citací (`quote_check.csv`) |
| §2: „70 oprav“ | 89 oprav (`corrections.json`) |
| „18+ commitů“ | 29 commitů |

**3. „Agent 2 na Macu“ bez vysvětlení, kde je jeho řešení.** README říká, že agent 2 řešil úlohu samostatně, ale jeho řešení v repu není. Hodnotitel se zeptá. Stačí jedna věta, např.: *„Odevzdané řešení je řešení agenta 1. Agent 2 sloužil jako nezávislá kontrola: jeho kritika je v `reviews/` a zjištění jsou zapracovaná (tabulka chyb AI).“*

**4. `ai-log` export a veřejné repo pod osobním účtem** (ne `wristradar26-creator`).

## 3. Co ještě ubere otázky (doporučené, ne nutné)

- **Ukázka databáze přímo v README.** GitHub `.xlsx` nezobrazí, jen ho nabídne ke stažení. Tabulka 5–10 investorů (název, typ, sektor, tiket, kapitál, poslední investice s odkazem) hned pod „Výsledek v kostce“ ukáže výsledek bez klikání.
- **Úplnost jedním srozumitelným číslem.** „První kolo našlo 66 %, další kola chybějící dohledala“ zní, jako by teď bylo 100 %. Návrh: *„Všichni investoři z katalogu CzechInvest, kteří prošli pravidly (30), jsou v databázi. Katalog sám ale 13 ze 43 našich investorů nezná, takže skutečnou úplnost jde odhadnout jen zdola.“*
- **ODEVZDANI §7 začíná větou „~50 tis. tokenů na kandidáta“.** To je statistika agenta, ze které cena $0,55–0,95 nevyplývá (50 tis. tokenů u Opus ≈ $0,27). README to samo uvádí jako opravenou chybu. Doplnit půl věty: *„…účtovaných tokenů je víc, protože agent posílá kontext opakovaně; cena je přepočtená v RESULTS §5.“*
- **Andělé bez sektoru** (Jiří Hlavenka, Michael Rostock-Poplar). Zadání chce sektor u každého. Buď doplnit zaměření ze zdrojů o jejich investicích (s citací), nebo do README přidat tabulku pokrytí po typech, kterou už máte v ODEVZDANI §3.

## 4. Doplňující informace z Mac řešení (INBOX bod 1)

- **Investoři:** všech 17 investorů z Mac řešení je v databázi (včetně JIC Ventures a i&i Bio). Nic nového k doplnění.
- **Hodnoty polí:** u překrývajících se investorů (Lighthouse, Rockaway, Czech Founders, Tensor, Reflex, DEPO) sedí s Mac daty nebo jsou novější. Tensor ticket nenašlo ani jedno řešení.
- **Negativní kontroly, které Mac testoval navíc:** Day One Capital (HU) a Venture to Future Fund (SK) vypadají v českých přehledech jako české fondy, ale nejsou. Pokud se objeví v dalším kole, pravidlo „mimo vzorek ČR“ je vyřadí.
- **Metodika:** nic zásadního navíc. Slepé ověření, aktuálnost a označení cíle fondu už máte. Jediný rozdíl je okno aktivity (Mac 24 měsíců, vy 36). Citlivostní analýza v PLAN §7.14 to pokrývá.

## 5. Co neměnit

- pravidla zařazení a vyřazení,
- pět vrstev kontroly,
- seznam chyb AI ve skupinách,
- sekce o placených databázích s ověřenými cenami,
- rozhodnutí o GDPR u andělů,
- tón README: čte se jako text člověka, ne jako výstup AI.
