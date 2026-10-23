# Spolehlivá databáze investorů — zadání A

Řešení praktické úlohy k pozici Junior AI Developer.
Pilot: investoři v Česku všech typů ze zadání, ve třech fázích (71 kandidátů → **43 zařazených**). Každý údaj má zdroj, datum
a doslovnou citaci, kterou kontroluje stroj. Úplnost je změřená proti oficiálnímu katalogu CzechInvest.

| soubor | obsah |
|---|---|
| [ODEVZDANI.md](ODEVZDANI.md) | **začni tady:** odpovědi na všechny body zadání, placené databáze (ceny, proč nepoužité), hlavní rozhodnutí |
| [PLAN.md](PLAN.md) | definice investora, pravidla zařazení/vyřazení, ověřování, odhad velikosti světa, úpravy po pilotu |
| [RESULTS.md](RESULTS.md) | výsledky pilotu, změřená přesnost, rozbor chyb, odhad nákladů na celý svět |
| [data/Databaze_investoru.xlsx](data/Databaze_investoru.xlsx) | **výsledek pro čtení: 43 investorů, jen to, co chce zadání** (sektor, do čeho a v jaké výši investuje, kapitál, doklad investice s datem); klik na hodnotu otevře zdroj; list Vyřazení s důvodem |
| [data/investors_cz_vc.csv](data/investors_cz_vc.csv) | totéž strojově: u každého údaje URL zdroje, datum a tier |
| [data/excluded.csv](data/excluded.csv) | 28 vyřazených / neaktivních / mimo rozsah, s pravidlem a důvodem |
| [data/records/](data/records/) | plné záznamy (JSON) po opravách — citace, fondy, všechny doložené dealy |
| [data/records_raw/](data/records_raw/) | totéž **beze změny tak, jak to vrátili rešeršní agenti** |
| [data/corrections.json](data/corrections.json) | 89 oprav: co se změnilo, proč a kdo to navrhl (ověřovací agent / slepý ověřovatel / orchestrátor / review Mac Clauda) |
| [docs/ZADANI.md](docs/ZADANI.md), [docs/requirements-check.md](docs/requirements-check.md) | zadání doslovně a kontrola řešení proti němu bod po bodu |
| [data/quote_check.csv](data/quote_check.csv) | strojová kontrola 494 citací |
| [data/verification/](data/verification/), [data/verification_v2/](data/verification_v2/) | verdikty ověřovacího agenta (fáze 1) a slepého ověřovatele (fáze 2), pole po poli |
| [data/blind/](data/blind/) | slepé podklady pro ověřovatele fáze 2: jen tvrzení + URL |
| [data/reference_czechstartups.csv](data/reference_czechstartups.csv), [data/recall.csv](data/recall.csv) | oficiální katalog CzechInvest jako referenční seznam a výsledek měření úplnosti |
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
python src/measure.py             # → přesnost (A: agent B, B: člověk, C: shoda B × člověk, E: fáze 2 slepě)
python src/recall.py              # → úplnost vůči katalogu CzechStartups
python src/simple_xlsx.py databaze  # → „Databáze investorů.xlsx“ (jeden řádek = investor, klik na hodnotu = zdroj)
python src/simple_xlsx.py kontrola  # → „Ruční kontrola.xlsx“ (6 vylosovaných investorů, políčko u každého údaje)
python src/simple_xlsx.py import    # vyplněná kontrola → data/manual_check.csv → src/measure.py
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

### Jak jsem výstup AI kontroloval (5 vrstev)

1. **Strojová kontrola citací.** Skript stáhne každý zdroj a hledá v něm citaci. Vymyšlená URL nebo citace
   neprojde. Výsledek: 459 z 494 citací doslova (zbytek hlavně prázdná pole a weby blokující stahování), žádná vymyšlená.
2. **Nezávislý agent B.** Znovu otevřel zdroje a ke každému poli dal verdikt `ok / wrong / unverifiable / null_ok / null_missed`.
   Ve fázi 1 našel 17 chybných polí ze 121 a 6 zmeškaných údajů. Ve fázi 2 byl **slepý**: dostal jen tvrzení + URL
   ([data/blind/](data/blind/)) a citaci si musel najít sám. Našel 10 chybných polí ze 77.
3. **Auditovatelné opravy.** Opravy se nedělají ručně v datech. Každá je zapsaná v [corrections.json](data/corrections.json)
   s důvodem a autorem a aplikuje se skriptem na nezměněný výstup agentů v `records_raw/`. V gitu je vidět rozdíl.
4. **Člověk.** Náhodný vzorek a sporné body v `manual_check.csv`. Ověřovací agent nemůže měřit přesnost dat, která
   sám opravil. Proto se finální přesnost (B) a důvěryhodnost agenta B (C) měří proti člověku.
5. **Druhé, nezávislé řešení (Mac Claude).**
   - Druhá session Claude Code na jiném počítači vyřešila stejné zadání sama, bez přístupu k tomuto repu.
   - Potom napsala review tohoto řešení a nezávislou kontrolu proti zadání.
   - Výsledek: [reviews/mac-claude.md](reviews/mac-claude.md) a odpověď na review [reviews/odpoved-android.md](reviews/odpoved-android.md).
   - Každý nález jsem ověřil proti zdrojům, než jsem ho převzal. Jeden se nepotvrdil: Dealroom u mě vrací 200, ne 403.
   - Průnik obou řešení zároveň dává odhad úplnosti (RESULTS §3D).

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
| **Genesis (PE) zařazen do vzorku, který byl podle vlastního plánu jen pro VC-typy** | hlavní session (přehlédla při kontrole proti zadání) | review Mac Clauda | `out_of_scope`, zařazených 21 |
| **Kapitál Lighthouse z článku z roku 2019 zapsán jako `undated`**, takže zastaralost nešla poznat | agent A | review Mac Clauda | datum doplněno; nová metrika aktuálnosti (PLAN §7.9) |
| **Odhad nákladů ze statistik agentů**, které nejsou účtované tokeny (kontext se při každém volání posílá znovu) → 2–3× podhodnoceno | hlavní session | review Mac Clauda | RESULTS §5 přepočten: jádro 35–50 tis., svět 85–125 tis. EUR |
| Ověřovací agent nebyl „slepý": viděl citace agenta A | hlavní session (návrh pipeline) | review Mac Clauda | přiznáno jako omezení metriky A; v2 = jen tvrzení + URL |
| IČO Nation 1 odvozené z výsledku vyhledávání, který agent neotevřel | agent A | review Mac Clauda | doloženo adresou v adresáři CVCA |
| Důkaz Tensoru jen z agregátoru; v listu pro ruční kontrolu splývalo zdůvodnění agenta s citací | agent A / hlavní session | review Mac Clauda | nahrazeno tier B (AppFactor, lead); sloupec `rationale` |
| **Pokyny v2 dovolily andělské „skupiny" jako `angel`**, i když plán definuje anděla jako fyzickou osobu | hlavní session | slepý ověřovatel (fáze 2) | nový typ `angel_syndicate`; spolek, kde investují členové (Garage Angels), = E4 (PLAN §7.15) |
| Schéma nemělo `basis` pro cílovou velikost fondu → cíle vykázané jako skutečné fondy (4×) | hlavní session (schéma) | slepý ověřovatel | `target_fund_size` (PLAN §7.17) |
| Registr: IČO mateřské banky místo investující dceřiné firmy (Seed Starter ČS) | agent A v2 | slepý ověřovatel | oprava na ČS Seed Starter, a.s. |
| Dva ověřovatelé si ve sdíleném adresáři přepsali skript stejného jména | infrastruktura agentů | agent to sám nahlásil | výsledky zkontrolovány (beze změny); v produkci vlastní adresář pro každého agenta |
| **Odhad úplnosti 88 %** z porovnání se druhým AI řešením (obě braly kandidáty ze stejných přehledů) | hlavní session | oficiální katalog CzechInvest | změřeno: 66 % (RESULTS §3b) |
| Tipy jiné AI (DeepSeek) na family office a anděly: ze 4 FO prošla pravidly jen 2, u anděla špatné jméno („Michal Rostock" místo Michael Rostock-Poplar) | DeepSeek (konzultace uživatele) | rešeršní agent fáze 3 | tipy jiných AI se ověřují stejně jako vlastní kandidáti (PLAN §7.24) |
| Typ „family office" převzatý z agregátoru, i když se subjekt sám označuje jako investiční skupina (TCF, BHM) | agent A v3 | slepý ověřovatel | pravidlo: rozhoduje vlastní označení subjektu (PLAN §7.21) |
| „Kapitál" 720 mil. EUR byl ve skutečnosti hodnota podílu v Rohlik Group, 1,1 mld. EUR aktiva celé skupiny | agent A v3 | slepý ověřovatel | správný `basis` (hodnota portfolia / aktiva skupiny) |
| Jet Investment (PE) a Jet Venture (VC) jako dva investoři, i když jde o jednoho správce | hlavní session (výběr kandidátů) | rešeršní agent (stejné IČO) | sloučeno do jednoho záznamu (E8, PLAN §7.22) |

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
  Zadání sice říká, že u každého investora „musí byť uvedené" sektor, tiket a kapitál, ale ne všichni investoři
  tyto údaje zveřejňují. Výsledek u 43 zařazených (podrobně podle typu v RESULTS §3c):
  - tiket chybí u 13 (např. Aspire11, Pale Fire, Tensor, Tachles, family office, andělé),
  - kapitál chybí u 13 (např. DEPO, Fazole, QQ Capital, Seed Starter; u 3 andělů úmyslně kvůli GDPR),
  - sektor chybí u 3 (Reflex a dva andělé, kteří zaměření nedeklarují).

  Rodinné kanceláře a syndikáty čísla zveřejňují nejméně, což odpovídá odhadu spolehlivosti v PLAN §5.

  U každého `null` je v `notes` záznamu, co se hledalo. Vymýšlet čísla, aby tabulka byla plná, by šlo proti hlavnímu
  požadavku na spolehlivost. Plnost polí je proto měřená zvlášť jako pokrytí (RESULTS §2), aby bylo vidět, kolik chybí.
- **Zdroj = URL + datum zdroje + datum přístupu + doslovná citace + tier.** Samotná URL nestačí: stránky se mění
  a bez citace se nedá zpětně ověřit, co na nich bylo.

## Co v řešení chybí

- **Ruční kontrola** proběhla jen na vzorku 6 investorů z fáze 1: 35/35 údajů sedí, shoda s AI ověřovatelem 96 %
  (RESULTS §3 B, C). Fáze 2 a 3 ověřil slepý AI ověřovatel, ne člověk.
- Longevitytech.fund: dohledat právnickou osobu (pravděpodobně česká a.s.). Jinak by byl zařazen.
- U KAYA, Miton a J&T Ventures upřesnit, která právnická osoba je správce (PLAN §7.5).
- **Úplnost:** fáze 1 našla 66 % investorů z oficiálního katalogu (RESULTS §3b). Fáze 2 chybějící dohledala.
  - Ani katalog ale není úplný (81 %), populace aktivních je ≥ 36, realisticky 40–45.
  - Ruční kontrola pokrývá jen fázi 1. Fáze 2 je ověřená slepým ověřovatelem, ne člověkem.
- NEWTON University Angels je hraniční případ: investice zřejmě v okně jsou (5 → 8 projektů), ale chybí deal s datem.
  Zůstává `inactive`.
- Ve vzorku jsou nedatované zdroje (hlavně weby investorů) bez snapshotu stránky. Zpětně tedy nejde doložit,
  co na stránce v den přístupu bylo (RESULTS §2).
