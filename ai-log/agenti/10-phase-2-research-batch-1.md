# Sub-agent 10: Phase 2 research batch 1

Spuštěn: 2026-10-22 17:06  
Použité nástroje: WebFetch 44×, WebSearch 27×, Bash 11×, Read 2×, Write 1×, PowerShell 1×

## Zadání, které agent dostal

Read C:\Users\vital\Desktop\Clode_Trading\investor-db\docs\prompt-research-agent-v2.md and follow it exactly (it tells you to read the v1 prompt and PLAN.md too; v2 rules take precedence). Today is 2026-10-22. Load WebSearch/WebFetch via ToolSearch if needed. Candidate context is in data/candidates_phase2.csv.

Your batch (id – name):
- tachles – Tachles VC
- qqcapital – QQ Capital
- agriboom – AgriBoom Ventures
- flyingfounders – Flying Founders
- lookai – Look AI Ventures (LAIV)
- purposetech – PurposeTech

Write one JSON per id into data/records_raw/<id>.json with "phase": 2. Do not touch other files. Return a short table: id, decision, type, what you are unsure about.

## Závěrečná zpráva agenta

I wrote all six records to `C:\Users\vital\Desktop\Clode_Trading\investor-db\data\records_raw\` (`tachles.json`, `qqcapital.json`, `agriboom.json`, `flyingfounders.json`, `lookai.json`, `purposetech.json`), each with `"phase": 2`. No other project files were changed.

Five are `include` and AgriBoom is `exclude`. Nothing turned out to be a duplicate (E8), and no page contained instructions aimed at an AI. Every IČO comes from an ARES record I opened directly.

| id | decision | type | What I'm unsure about |
|---|---|---|---|
| tachles | include | vc | It has offices in Prague, Tel Aviv and Atlanta. The Czech manager, Tachles VC Management s.r.o., is owned by a Delaware LLC, and the website shows a US address. I set country CZ because of the Czech team and Czech s.r.o., but it could be argued. The fund size (about CZK 500M, first phase) dates from 6/2024. The 2025–26 deals other than Boost.space appear only in aggregators. Cybersecurity has no category in the sector list, so I mapped it to ai + saas_b2b + deeptech. |
| qqcapital | include | family_office | The only A/B evidence is the Navigara seed round, from a Pulse2 article of 2026-03-06. The round date 2026-02-19 comes from aggregators. The website says "early-stage to growth-stage", and how I split that into stages is my interpretation. Ticket and capital are not published. |
| agriboom | exclude (I2) | cvc | It is a €60M fund launched 12/2024, but I found no investment backed by an A/B source. The only case, Plantee, ended with AGRO CS buying the company outright rather than the fund investing. The Forbes.cz articles are paywalled and Crunchbase returned 403. The registry entry is AGRO CS a.s., the fund's GP; the fund itself has no IČO I could find. `inactive` would also be a defensible decision. |
| flyingfounders | include | private_investor | It is an s.r.o. owned by two entrepreneurs (Truban, Zvada) investing their own money, so `vc` is an alternative type. The founders are Slovak and the company is Czech, so where the team actually sits is unclear. Of the two deals, Tolgee (CzechCrunch 9/2024) is the strong one. Tiny Empires (9/2025) is a newsletter buyout sourced from the seller's own post. The ticket is €100–500k on the website and €100–600k in the press. |
| lookai | include | vc | Which entity counts as the manager is open. The record uses the SICAV (17604087). The legal manager is FTP Dimension investiční společnost (29659302), and the operating team is Look AI Investments, a.s. (06385745). Capital of €20M is the 2023 target, not a confirmed close. |
| purposetech | include | vc | The ticket (€0.5–1M) belongs to the new fund PT Capital; the first fund's ticket is unknown. Capital is "necelých 60 mil. Kč" (just under CZK 60M), so I stored 60,000,000 as an upper bound. The newest deal I could date to a specific article is eNOugh (9/2024). A 2/2026 article confirms 11 investments in total, without dates. |

Some quotes came through the fetch tool's extract, which caps quotes at about 125 characters, so the machine quote check may flag a few. This mainly affects cc.cz and the CzechStartups profiles. I listed these risks in each record's `notes`.
