# Sub-agent 12: Phase 2 research batch 3

Spuštěn: 2026-10-22 17:06  
Použité nástroje: Bash 36×, WebSearch 21×, Read 2×, WebFetch 2×, Grep 1×, Write 1×

## Zadání, které agent dostal

Read C:\Users\vital\Desktop\Clode_Trading\investor-db\docs\prompt-research-agent-v2.md and follow it exactly (it tells you to read the v1 prompt and PLAN.md too; v2 rules take precedence). Today is 2026-10-22. Load WebSearch/WebFetch via ToolSearch if needed. Candidate context is in data/candidates_phase2.csv.

Your batch (id – name):
- garageangels – Garage Angels
- up271 – UP271
- opifer – Opifer Investments
- rsj – RSJ Investments (VC activity via RSJ Angel Tech / RSJ Tech funds)
- seeders – The Seeders
- limerock – Limerock Ventures (advisory firm that also invests – test rule E4)

Write one JSON per id into data/records_raw/<id>.json with "phase": 2. Do not touch other files. Return a short table: id, decision, type, what you are unsure about.

## Závěrečná zpráva agenta

I wrote all 6 records to `C:\Users\vital\Desktop\Clode_Trading\investor-db\data\records_raw\<id>.json` with `"phase": 2`. A script checked every quote against the saved page text (whitespace ignored), and all of them matched. I changed no other files.

| id | decision | type | what I'm unsure about |
|---|---|---|---|
| garageangels | include | angel | It is unclear which legal entity actually invests: the club Garage Angels z.s. (IČO 21814414), Garage Angels Management s.r.o. (21657505), or the members through separate vehicles. The press only calls it a group or club. Proof of investment: VR Life seed round (Lupa, 2026-02-23) and Sendance (Forbes, 2026-02-16), both from dated tier-B articles. The g-angels.cz site would not open (redirect loop). Groundcom has no date in Forbes; the June 2025 date is only in Caplight, so I set `date: null`. Ticket is only an average of about €400k (stored in `original.average`), with min and max left null. |
| up271 | inactive (E6) | family_office | I found no dated UP271 deal after 2023-10-22, and the portfolio page has no dates. The Poetizer deal was Janeček personally, which fails rule 5. NutritionPro (2021) went through UP21. The type is an inference: Janeček is the sole owner. The link to UP21 is unclear (the site says UP271 builds on UP21's history); if UP21 ever enters the database, check rule E8. |
| opifer | inactive (E6) | vc | The website is from 2018 and I found no deal since then. The registry choice is uncertain: I used Opifer Services, s.r.o. (04285905, Brno, owned by the UK company Opifer Ltd.). ARES also lists Opifer s.r.o. (Ostrava) and Opifer Alfa s.r.o. Mapping "proprietary IT / Smart Device" to the sector list is approximate. |
| rsj | include | vc | RSJ mostly invests in other VC funds rather than startups. I included it because it invested directly as co-lead in the Hedepy round on 2024-01-25 (AIN.ua, tier B). That is the only direct deal I found inside the 36-month window, and I don't know which RSJ fund it came from. Fund sizes and vintages are not published. If "VC-type" is read strictly, a fund of funds could fall out of scope. |
| seeders | exclude (I2) | angel | Founded in 2024 around the Niceboy founders; ticket 1–10M CZK (amount kept as given, not converted). I found no documented investment in an outside company: the "Projekty" on its site are members' own firms plus a real-estate project. No company registration found either (ARES has nothing, the site shows no IČO), so I1 is also unmet. Searches mostly return an unrelated Indian syndicate called Seeders. |
| limerock | out_of_scope | vc | On the E4 test: E4 does not apply, because Limerock has its own investment vehicle (a fund manager registered with the Slovak central bank). It is out of scope because it is based in Bratislava with no Czech team. Its only documented fund (JEREMIE Co-Investment Fund) has made no new investment decisions since 2016-11-01. The SIH page blocked access, so I could not check whether there is a newer fund. |

No page contained instructions aimed at an AI.

Working files (downloaded page texts and the builder script) are in `C:\Users\vital\AppData\Local\Temp\claude\C--Users-vital-Desktop-Clode-Trading\e35f7c62-fc82-48c6-a51c-4b5dc5f05dd4\scratchpad`.
