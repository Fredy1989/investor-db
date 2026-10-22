# Další zdroje: analýza (2026-10-22, večer)

Vitalij dodal materiály ze složky `Desktop\Clientelo` (nejsou v repu):
- přepisy konzultací s jinými AI (Gemini, DeepSeek),
- 8 exportů z registru ČNB (JERRS),
- katalog investorů z portálu CzechStartups (CzechInvest) jako `Book1.xlsx`.

Vše jsem prošel. Přepisy jiných AI beru jako **tipy, ne fakta**: každý údaj z nich musí projít stejným ověřením jako výstup mých agentů.

## 1. Registr ČNB: k čemu je a k čemu ne

| export | obsah | záznamů | použití pro databázi investorů |
|---|---|---|---|
| Investiční fondy vč. podfondů + obhospodařovatel/administrátor/depozitář (2× totožný soubor) | fondy a podfondy, IČO, správce | 888 fondů, 89 správců | **I1 (registrace)** a **kandidáti** — viz níže |
| Investiční společnosti | správci (AMISTA, ČSOB AM, EMUN…) | ~15 | správci fondů; většinou retail/reality, ne VC |
| Podílové fondy a jejich depozitář | fondy pro veřejnost | 372 | mimo cíl (E5: kotovaná aktiva) |
| Obchodníci s cennými papíry | brokeři | 79 | **E4** — zprostředkovatelé, nejsou investoři |
| Investiční zprostředkovatelé | firmy | ~107 | **E4** |
| Vázaní zástupci | převážně fyzické osoby | 20 103 | **E4 + GDPR** — zprostředkovatelé a osobní údaje; do DB nepatří |
| Poskytovatelé DIP | instituce | ~35 | mimo cíl |

**Závěr:**
- Konzultace s Gemini doporučovala exporty zprostředkovatelů a vázaných zástupců jako „aktivní investory". **Podle pravidel E4 to investoři nejsou.** Prodávají investiční produkty, sami do firem kapitál nevkládají. Navíc jde o desítky tisíc fyzických osob. Pravidla tak zabránila zařazení zhruba 20 tis. „náhodných firem a osob".
- **Užitečný je jen registr fondů**, a to částečně. Ze 21 zařazených investorů jsou v něm vidět jen Inven, J&T Ventures, Rockaway Ventures a KAYA (přes podfondy ENERN TECH III/IV, KAYA dříve Enern). Většina českých VC jsou malí správci podle **§ 15 ZISIF** („osoba rizikového kapitálu") nebo mají fondy v Lucembursku. Ti jsou v jiném seznamu ČNB, který export neobsahuje.
  → Pro I1 při škálování: stáhnout i seznam správců dle § 15 ZISIF a EuVECA.

## 2. Registr fondů ČNB jako zdroj kandidátů

Fondy s VC klíčovými slovy v názvu (37), které v mém vzorku nejsou a stojí za ověření:
- **Jet Venture 1** (VC rameno Jet Investment),
- **JSK Investments Venture Capital Fund I**,
- **STARTEEPO / CZEGG Ventures**,
- **Soulmates Ventures Fund**,
- **Look AI Ventures I**,
- **Direct PRO Ventures**,
- **Partners Innovation Fund**,
- **Double Speed rizikový fond**,
- **EMUN TECH II**,
- **ATERNUS TECH I**,
- **RSJ Angel Tech / RSJ Tech I–IV**.

Plus kontrolní případy:
- **Conseq Venture Debt** a **Conseq-Orbit** jsou venture debt, tedy E3. Odpovídá to vyřazení Orbit Capital.
- **Green Tech for Future** a **PREMIOT** jsou v likvidaci, tedy E6.

## 3. Katalog CzechStartups jako referenční seznam pro úplnost (recall)

Katalog má 52 položek. Roztřídil jsem je podle pravidel z PLAN.md:

| kategorie | počet | položky |
|---|---|---|
| **v mém vzorku zařazeno** | 19 | KAYA, Czech Founders, Purple, Tensor, Impulse, J&T, Tilia, Pale Fire, N1, Lighthouse, Presto, Reflex, Credo, Inven, Miton, Rockaway, Springtide, Y Soft, DEPO |
| v mém vzorku, vyřazeno / mimo rozsah | 3 | StartupYard (E6), Fundlift (E1), Genesis (mimo rozsah) |
| duplicita (E8) | 1 | Enern = dřívější název KAYA |
| asociace / sítě (E4) | 4 | CBAA, CVCA, EBAN; Limerock je primárně poradce (E4, k ověření) |
| crowdfunding / platformy (E1) | 4 | Penězdroj, Startovač, Hithit, Startupstart.cz |
| zahraniční sídlo (mimo vzorek ČR) | 2–4 | Heartcore (DK), Taiwania (TW); 3TS Capital a mAccelerator (PL) k ověření |
| **chybí ve vzorku, česká VC-like, neověřené** | **~17** | Tachles VC, QQ Capital, AgriBoom Ventures, Flying Founders, Look AI Ventures, PurposeTech, NEWTON University Angels, Soulmates Ventures, KB SmartSolutions (CVC), Seed Starter ČS (CVC), Lumus Investment, Fazole Ventures, Garage Angels, UP271, Opifer, RSJ Investments, The Seeders |

**Dopad na úplnost:**
- Proti katalogu mám 19 z ~36 relevantních českých subjektů. Část z ~17 chybějících ale nemusí být aktivní (pravidlo E6), případně jde o andělské skupiny. Skutečnou úplnost dá až jejich ověření.
- **Odhad ≈ 88 % z porovnání s Mac řešením byl příliš optimistický.** Obě session braly kandidáty z podobných veřejných přehledů, takže jejich seznamy nebyly nezávislé. Lincoln–Petersen pak populaci podhodnotí. Varování v RESULTS §3D se tím potvrdilo.
- Realisticky: **úplnost vzorku je spíš 55–75 %**, podle toho, kolik ze 17 bude aktivních.
- Poučení je stejné jako v §3D, jen silnější: úplnost se ztrácí už při výběru kandidátů. Oficiální katalog (CzechInvest) a registr (ČNB) měly být mezi zdroji kandidátů od začátku.

## 4. Další tipy z konzultací s AI (k ověření, ne fakta)

| tip | zdroj | hodnocení |
|---|---|---|
| Apify aktory (databáze investorů za $6,40–40 / 1 000 firem) | DeepSeek | Agregátor (tier C) a placený. Hodí se jako levný **zdroj kandidátů** při škálování: 100 tis. kandidátů ≈ $0,6–4 tis. Ověření tím nenahradí. Do odhadu nákladů jako alternativa vstupu |
| family office v ČR (Sev.en, BHM, TCF Capital, J&T Family Office, EMUN, Aternus…) | DeepSeek (komerční databáze, neověřeno) | kandidáti pro segment FO; Aternus a EMUN mají tech fondy v registru ČNB |
| další české VC/andělé (Air Ventures, Benson Oak, Koopeo, Garage Angels, The Seeders) | DeepSeek (VŠE práce + Crunchbase) | kandidáti; DeepSeek údaje o tiketech nepřebírám bez zdroje |
| okno aktivity 12–24 měsíců | DeepSeek | v souladu s citlivostní analýzou PLAN §7.14 (při 24 m vypadne jen Impulse) |
| SEC IAPD pro ověření US family office | DeepSeek | v souladu s RESULTS §5 (registry před LLM) |

## 5. Navržený další krok (čeká na rozhodnutí)

**Pilot, fáze 2:** ~30 nových kandidátů (17 z katalogu + ~10 z registru ČNB + JIC Ventures a i&i Bio od Mac Clauda) projít pokyny v2:
- měna jako `original`, přepočet kódem,
- sektory jen z mandátu,
- slepý ověřovatel.

Výsledek dá:
1. úplnost změřenou proti oficiálnímu katalogu místo odhadu,
2. test pokynů v2 proti v1,
3. přesnější podíl zařazených kandidátů (yield) pro odhad nákladů.
