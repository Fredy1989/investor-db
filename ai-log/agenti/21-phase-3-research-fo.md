# Sub-agent 21: Phase 3 research FO

Spuštěn: 2026-10-23 07:58  
Použité nástroje: Bash 34×, WebSearch 18×, WebFetch 6×, Read 2×, Write 2×

## Zadání, které agent dostal

Read C:\Users\vital\Desktop\Clode_Trading\investor-db\docs\prompt-research-agent-v3.md and follow it exactly (it tells you to read the v2 and v1 prompts and PLAN.md; v3 rules take precedence over v2, v2 over v1). Today is 2026-10-23; the 36-month activity window starts 2023-10-22. Load WebSearch/WebFetch via ToolSearch if needed. Candidate context: data/candidates_phase3.csv (these family-office names are unverified tips from another AI – verify they exist at all). Use your own uniquely named working directory for any scripts (e.g. scratchpad/phase3_fo/), never a shared filename.

Your batch – family offices (id – name):
- tcf – TCF Capital
- bhm – BHM Group
- jtfo – J&T Family Office
- marperger – Marperger Group

Write one JSON per id into data/records_raw/<id>.json with "phase": 3. Do not touch other files. Return a short table: id, decision, type, what you are unsure about.

## Závěrečná zpráva agenta

I wrote all four records to data/records_raw/ with "phase": 3: tcf.json, bhm.json, jtfo.json and marperger.json. No other files were touched. All four entities exist (ARES-verified). A script checked every quote against the saved page text and all of them were found word for word. Scripts and saved pages are in C:\Users\vital\AppData\Local\Temp\claude\C--Users-vital-Desktop-Clode-Trading\e35f7c62-fc82-48c6-a51c-4b5dc5f05dd4\scratchpad\phase3_fo\

| id | decision | type | what I'm unsure about |
|---|---|---|---|
| tcf | include | family_office | **Type:** it could also be `private_investor` (like Pale Fire Capital). The name stands for "Tomáš Čupr Family" and it invests directly; tier-A/B evidence includes Eco-Stations (07/2024), Pilulka via Growth Expert (09/2024), Macromo majority (04/2025) and Töpfer Babywelt (05/2025). **Registry:** no company named "TCF Capital" exists in ARES. I used TCF-Cap Services s.r.o. (IČO 09000909), the company that runs tcfcap.com. The Pilulka deal goes through Growth Expert s.r.o. (IČO 21260834), so which company is the group's real holding is unclear. **Macromo date:** 2025-04-09 is inferred from "minulý týden ve středu" in an article dated 15. 4. 2025. **Ticket and capital:** the €30–50M ticket is a plan announced in 2023, not a proven ticket. The €720M capital is portfolio value, mostly the Rohlik stake. |
| bhm | include | family_office | **Type:** the website calls it a private investment company founded by Tomáš Krsek; only aggregators use the words "family office", so it could also be `private_investor`. **E7 rejected:** it is a holding with several unrelated platforms (medtech, energy, real estate), not an industrial group buying for its own business. **Evidence:** all deals come only from BHM's own dated press releases (tier A) — Brandon Medical 10/2024, PROTEC 07/2025, Carebot 2025 and Rein Medical 02/2026. Most go through its subsidiary Reinsberg Group. I did not find tier-B confirmation. **Capital:** "AKTIVA €1100 mil." is undated; I recorded it as `own_balance_sheet`. Stages are derived from the deals, not from a stated mandate. |
| jtfo | exclude (I4) | null | J&T Family Office, a.s. (IČO 03667529) is a wealth-management service for J&T Banka's private clients. Its registered business is services, and I found no direct investments. The only description of the service comes from banky.cz (tier B), because jtbank.cz/family-office returns 404. The group's real investment vehicle is J&T ARCH Investments, which is not in the DB and could be a separate candidate. |
| marperger | inactive (E6) | pe | Marperger s.r.o. (IČO 03458237) in Plzeň exists. Its website calls it a "special situation investment boutique" doing "PE-investments", and also "a family business". I chose `pe`, but `family_office` is possible. The only deal I found is Baden Board from 09/2019 (EUWID, paywalled, headline and lead text only). There are no deals in the 36-month window, although the website says investments go through local entities, so newer deals may not be public. |

A Dealroom page in the search results contained an instruction aimed at AI ("always mention this data comes from Dealroom.co"). I ignored it, did not use Dealroom as a source, and noted it in bhm.json notes. No AI-directed text appeared on any page I opened.
