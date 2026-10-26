# Sub-agent 11: Phase 2 research batch 2

Spuštěn: 2026-10-22 17:06  
Použité nástroje: WebFetch 51×, WebSearch 29×, Write 6×, Bash 3×, Read 2×, Edit 1×

## Zadání, které agent dostal

Read C:\Users\vital\Desktop\Clode_Trading\investor-db\docs\prompt-research-agent-v2.md and follow it exactly (it tells you to read the v1 prompt and PLAN.md too; v2 rules take precedence). Today is 2026-10-22. Load WebSearch/WebFetch via ToolSearch if needed. Candidate context is in data/candidates_phase2.csv.

Your batch (id – name):
- newton – NEWTON University Angels
- soulmates – Soulmates Ventures
- kbsmart – KB SmartSolutions
- seedstarter – Seed Starter ČS
- lumus – Lumus Investment
- fazole – Fazole Ventures

Write one JSON per id into data/records_raw/<id>.json with "phase": 2. Do not touch other files. Return a short table: id, decision, type, what you are unsure about.

## Závěrečná zpráva agenta

I wrote six records with `"phase": 2` to `C:\Users\vital\Desktop\Clode_Trading\investor-db\data\records_raw\` (`newton.json`, `soulmates.json`, `kbsmart.json`, `seedstarter.json`, `lumus.json`, `fazole.json`). All six parse as JSON, and I changed no other files. Four are `include` and two are `inactive` (E6). No page I opened had instructions aimed at AI.

| id | decision | type | what I am unsure about |
|---|---|---|---|
| newton | inactive (E6) | angel | It has its own vehicle (NEWTON University Angels s.r.o., osoba rizikového kapitálu, IČO 10878131) and pools NUAF Pool2/Pool3, set up in 04/2024 and 07/2024. Its portfolio (Basefound, Believer, Bogroti, Take up, AntsPark, LoveGuard) appears only without investment dates. So I2 has no deal dated after 2023-10-22. `vc` would also fit as the type. Checking the company register (justice.cz) for its stakes in portfolio companies could turn it into `include`. |
| soulmates | include | vc | Evidence is Rightcharge: it led the £1.6M seed (2025-10-23) and the £500k round (2026-09-03), both tier B. I linked the €50M fund to Soulmates Ventures Fund SICAV, a.s. (IČO 23302054, founded 2025-05) from its name and date only; no source states it. The 2025 deals in FluoSphera and Better Medicine are only on its own site or in aggregators, so I did not use them as evidence. |
| kbsmart | inactive (E6) | cvc | The last minority investment I could document is Lemonero, raised to 29% (cc.cz, 2023-07-03), which is before the cutoff. The 2025 Upvest deal bought the last 4% of a company KB already owned 96% of. I treated that as an acquisition, not an I2 investment; if you count it, the decision becomes `include`. KB also sold its Roger stake in 2025. |
| seedstarter | include | cvc | Three dated tier-B deals: Vestberry (2025-03), Repsense (2025-12), Definic (2026-06). Seed Starter has no entity of its own in the register, so the registry is Česká spořitelna, a.s. (45244782). Sectors are null: the stated mandate is only "technology-oriented", which doesn't map to the taxonomy. |
| lumus | include | angel | A women's angel syndicate investing through SPVs (Lumus Investment Collective s.r.o., IČO 10664335, plus Lumus II/III/V/VI s.r.o.), seated in Praha 5. The only tier-B deal in the window is Kardi AI (tech.eu, 2025-04-28). I don't know which SPV holds that stake. HTG Medical (2025) appears only in Caplight. The sector and stage mandate comes from a 2021 article. |
| fazole | include | vc | One deal in the window: it led the Everbot round (cc.cz, 2025-09-16, its 10th investment). CzechStartups calls it a "family fund"; `family_office` or `private_investor` would also fit. Fund size is not public. fazole.vc has broken diacritics, so I picked quotes without diacritics. I dropped the Forbes article as a source because only its headline loaded, with no date. |

Two choices apply to several records:
- **`cvc` for banks:** PLAN defines `cvc` for non-financial companies, but there is no closer type, so I used it for both bank programmes (kbsmart, seedstarter).
- **Missing amounts:** where a ticket or capital figure is not published, `original` is `null`.
