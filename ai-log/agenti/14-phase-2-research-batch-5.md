# Sub-agent 14: Phase 2 research batch 5

Spuštěn: 2026-10-22 17:06  
Použité nástroje: WebFetch 35×, WebSearch 18×, Bash 7×, Read 4×, Grep 1×, Write 1×

## Zadání, které agent dostal

Read C:\Users\vital\Desktop\Clode_Trading\investor-db\docs\prompt-research-agent-v2.md and follow it exactly (it tells you to read the v1 prompt and PLAN.md too; v2 rules take precedence). Today is 2026-10-22. Load WebSearch/WebFetch via ToolSearch if needed. Candidate context is in data/candidates_phase2.csv.

Your batch (id – name):
- partnersinnov – Partners Innovation Fund (Partners investiční společnost; in ČNB register)
- doublespeed – Double Speed rizikový fond (Partners investiční společnost; in ČNB register)
- emuntech – EMUN TECH (EMUN investiční společnost / multi-family office; does it invest directly in startups?)
- aternus – ATERNUS (podfond TECH I; family office from Třinec)
- jic – JIC Ventures (Brno)
- iibio – i&i Bio (biotech VC; check whether the team/manager is Czech or Luxembourg-based)

Write one JSON per id into data/records_raw/<id>.json with "phase": 2. Do not touch other files. Return a short table: id, decision, type, what you are unsure about.

## Závěrečná zpráva agenta

I wrote all 6 records to `C:\Users\vital\Desktop\Clode_Trading\investor-db\data\records_raw\<id>.json` with `"phase": 2` and changed no other files. Three are included, two are excluded and EMUN is out of scope.

| id | decision | type | what I am unsure about |
|---|---|---|---|
| partnersinnov | exclude (E7) | cvc | Its stated aim is to invest in the Partners Group's own financial and distribution companies (fintech/insurtech only on a small scale). Created 1/2026, first closing 7/2026, no deals named. The manager is QI investiční společnost (Conseq), not Partners IS as the candidate list said. E7 is the closest rule; I2 (no documented investment) would also fit. |
| doublespeed | exclude (E5) | null | Not a borderline case: it is a retail fund that buys listed global stocks with leverage. "Rizikový" means high-risk, not venture capital. Fund IČO 75164078, manager IČO 24716006. |
| emuntech | out_of_scope | family_office | I found no "EMUN TECH (I)", only EMUN TECH II Access: a fund of European early-stage VC funds with 172M CZK committed at 31.12.2024. No direct startup investments found. The other funds are PE, credit, infrastructure and Global Unicorns, which buys late-stage stakes in companies worth over USD 1B. The annual report has no exact publication date, so I put "2025". emun.cz/cz returned HTTP 500, so I used the English page. |
| aternus | include | family_office | Deal evidence: Jutro Medical Series A extension (AIN, 2025-12-16, tier B). Woltair 2022 is listed only as a second deal for I3. The source says just "Aternus", so I don't know which entity made the investment: ATERNUS, a.s. (IČO 25865056), Aternus Family Office s.r.o. (26795043), or ATERNUS SICAV podfond TECH I. ARES gives ATERNUS, a.s. the address Anežská 986/10, Praha 1, the same as EMUN's, while the website says Třinec. I couldn't find TECH I's investment policy. Sectors set to "generalist" because the website lists broad tech. |
| jic | include | vc | Could be public_vc: the manager is a subsidiary of the regional agency JIC, but 85% of the new fund's money is private. The new 400M CZK fund is not final-closed and I found neither its legal form nor its IČO, so the registry field is JIC Ventures, s.r.o. (04156293). Deals: FaceUp Series A (EEN, 2026-05-21, tier B) and Customerscore.io (date only "2025"). |
| iibio | include | vc | The fund (i&i Biotech Fund I SCSp) is domiciled in Luxembourg; the adviser Biotech Investments s.r.o. (10885978) is in Prague, so country = CZ. The website doesn't name the Luxembourg GP, and I didn't confirm team members from a primary source. The capital figure ">45M EUR" comes from an undated page and may be out of date. Stages: the website says only "early stage", which I recorded as seed + series_a. The Würzburg quote is part of a longer sentence. Deals: T-CURX (2025-12-17) and KyDo (2025-09-22), both tier B. |

None of the pages I opened contained instructions aimed at AI. Every IČO comes from an ARES page I opened, except EMUN's, which is from its 2024 annual report. Aggregators (Caplight, CB Insights, PitchBook) were used only to find deals, not as evidence.
