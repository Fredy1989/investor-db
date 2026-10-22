# Kontrola řešení proti zadání

Autor: Claude Code (Windows / Android session, Opus 5.5), 2026-10-22, commit `235113a`.
Zadání je doslovně v [ZADANI.md](ZADANI.md). Každý bod jsem ověřoval proti obsahu repa (data, skripty), ne podle paměti.

Legenda: ✅ splněno · ⚠️ splněno s výhradou · ❌ nesplněno

## Zadání A

| # | požadavek | stav | kde | jak ověřeno / výhrada |
|---|---|---|---|---|
| 1 | Plán: kdo v databázi bude a kdo ne (pravidla zařazení / vyřazení) | ✅ | PLAN §1–2 | definice, 7 typů, pravidla I1–I4 (vše musí platit), E1–E8 (stačí jedno); v pilotu otestováno na 7 vyřazených |
| 2 | Jak se ověří pravost a správné zařazení | ✅ | PLAN §4 | 5 kroků: kandidát, rešerše, strojová kontrola citací, nezávislý agent B, člověk; metriky přesnosti, pokrytí a recall |
| 3 | Jaký okruh investorů jde z veřejných zdrojů získat a kolik jich bude | ✅ | PLAN §5 | 30–50 tis. subjektů, jádro VC/PE/CVC 12–16 tis., rozpad po 7 segmentech |
| 4 | Jaká bude spoľahlivosť dát | ✅ | PLAN §5, RESULTS §3 | hypotéza po polích; pilot ji změřil (A: 86 % polí, 92 % bez chyby kurzu) |
| 5 | Z čeho odhad vychází | ⚠️ | PLAN §5 | VC (NVCA), PE (Preqin), PE+VC v Evropě (Invest Europe), FO (Deloitte) a andělé (EBAN) mají zdroje. **CVC a velcí soukromí investoři jsou jen vlastní odhad**, označený „nízká jistota". Hodnotitel to může vytknout. Možné zlepšení: dohledat zdroj (např. počty CVC z GCV / CB Insights) |
| 6 | Ověření plánu na menší vzorce (VC v jedné zemi) | ✅ | RESULTS §1 | Česko: 29 kandidátů → 22 zařazeno, 7 vyřazeno s pravidlem; záměrně i hraniční případy |
| 7 | U každého záznamu zdroj a datum, které dokládají, že investuje | ✅ | `data/investors_cz_vc.csv` (`last_deal_*`) | 22/22 má datovaný deal po 2023-10-22. Zdroj nejnovějšího dealu je u 2 záznamů tier A a u 20 tier B. Původně byl DEPO doložen jen agregátorem a KAYA stránkou bez data; obojí opraveno (`corrections.json`, poslední 2 položky) |
| 8 | U každého investora sektor, co a v jaké výši investuje, celkový kapitál, odkud informace jsou | ⚠️ | RESULTS §2, README „Rozhodnutí" | zdroj je u každého vyplněného údaje (URL + datum + citace + tier). **Pokrytí:** sektory 95 %, fáze 95 %, tiket 82 %, kapitál 86 %. Chybí: tiket u 4 (Aspire11, Pale Fire, Tensor, Y Soft), kapitál u 3 (DEPO, Springtide, Y Soft), sektor u 1 (Reflex). Úmyslně `null` místo odhadu; zdůvodněno v README |
| 9 | **Přesnost na ručně ověřené vzorce** | ❌ | `data/manual_check.csv`, `src/measure.py` | Zatím je změřená jen přesnost **AI ověřovatelem** (agent B: 87 % záznamů, 86 % polí). Ruční list je připravený (58 řádků: náhodný vzorek 6 záznamů × 8 polí + sporné body), **čeká na vyplnění člověkem**. Nejslabší bod řešení. |
| 10 | Odhad nákladů na rozšíření na celý svět | ✅ | RESULTS §5 | z naměřené spotřeby pilotu (~48 tis. tokenů a ~20 volání nástrojů na kandidáta) + ceník modelů: jádro ≈ 28–35 tis. EUR, celý rozsah ≈ 60–70 tis. EUR. Výhrada: cena vyhledávacího API (~$10 / 1 000 dotazů) je předpoklad, je potřeba ji ověřit |
| 11 | Jen veřejně dostupná data | ✅ | `data/quote_check.csv` | všech 226 zdrojů se stáhlo bez přihlášení (i Dealroom, CB Insights, Unquote, Caplight) a citace na nich byly nalezeny. Jediný „neveřejný" vstup by byl PitchBook; v datech použit není (jen zmínka v `notes`) |

## Obecné požadavky

| # | požadavek | stav | kde | výhrada |
|---|---|---|---|---|
| 12 | README: jak se s AI pracovalo, pokyny agentům, kontrola výstupu, kde se AI mýlila | ✅ | README, `docs/prompt-*.md` | 9 konkrétních chyb AI včetně chyb orchestrátoru (vymyšlený kandidát „Pointer", pevný kurz v pokynech) |
| 13 | Nejasnosti rozhodnout a zdůvodnit v README | ✅ | README „Rozhodnutí…" | 7 rozhodnutí (vzorek, typy navíc, správce vs. fond, 36 měsíců, tiket/kapitál, null, formát zdroje) |
| 14 | Uvést, co v řešení chybí | ✅ | README „Co v řešení chybí" | |
| 15 | Kód s průběžnou historií commitů | ✅ | git log | 8+ commitů po krocích (plán → skripty → vzorek → ověření → opravy → výsledky → README → kontrola) |
| 16 | `ai-log/` s exportem konverzace (`/export`) | ❌ | `ai-log/` | zatím jen README; export udělá uživatel na konci |
| 17 | Veřejný repozitář na GitHubu | ❌ | | záměrně až po dokončení, pod osobním účtem uživatele (ne `wristradar26-creator`) |

## Co je potřeba dodělat před odevzdáním (podle důležitosti)

1. **Ruční kontrola** `data/manual_check.csv` → `python src/measure.py` → doplnit čísla B a C do RESULTS §3.
2. `/export` do `ai-log/`.
3. Zapracovat nálezy z nezávislého review (Mac Claude).
4. Volitelně: zdroj pro odhad počtu CVC (bod 5), ověřit cenu search API (bod 10).
5. Veřejné repo pod osobním účtem a e-mail do 30. 10.
