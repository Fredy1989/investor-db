# Sub-agent 20: Phase 3 research PE

Spuštěn: 2026-10-23 07:58  
Použité nástroje: Bash 28×, WebSearch 8×, WebFetch 5×, Read 2×, Write 1×

## Zadání, které agent dostal

Read C:\Users\vital\Desktop\Clode_Trading\investor-db\docs\prompt-research-agent-v3.md and follow it exactly (it tells you to read the v2 and v1 prompts and PLAN.md; v3 rules take precedence over v2, v2 over v1). Today is 2026-10-23; the 36-month activity window starts 2023-10-22. Load WebSearch/WebFetch via ToolSearch if needed. Candidate context: data/candidates_phase3.csv. Use your own uniquely named working directory for any scripts (e.g. scratchpad/phase3_pe/), never a shared filename.

Your batch – private equity (id – name):
- jetinvest – Jet Investment (PE manager; its VC arm "Jet Venture 1" already exists as record data/records/jetventure.json – this record is the PE part)
- arx – ARX Equity Partners
- bensonoak – Benson Oak Capital

Write one JSON per id into data/records_raw/<id>.json with "phase": 3. Do not touch other files. Return a short table: id, decision, type, what you are unsure about.

## Závěrečná zpráva agenta

I wrote three records with "phase": 3. All 24 quotes were checked by a script against the text of the pages I fetched, and they all matched. I wrote no other files. My working files are in C:\Users\vital\AppData\Local\Temp\claude\C--Users-vital-Desktop-Clode-Trading\e35f7c62-fc82-48c6-a51c-4b5dc5f05dd4\scratchpad\phase3_pe\.

| id | decision | type | what I'm unsure about |
|---|---|---|---|
| jetinvest | include | pe | **Same IČO as `jetventure`.** `registry` is Jet Investment, a.s. (03890333), which is also the registry on the existing `jetventure` record. I kept it as a separate PE record, as the candidate note says; whether to merge manager and arms is your call. I did not check in the ČNB register (JERRS) who formally manages the Jet 3 and Jet 4 SICAV funds. **Capital:** Jet 4 fund target of more than €300m (`target_fund_size`), from Forbes 2026-03-31. **Jet 3 size:** I left it as null. The website gives €185m, but that is "invested capital", not the fund's committed size. The sources also disagree on Jet 3's start year (website says 2024, CzechCrunch says 2022). **Ticket:** the €10–60m figure is the value of one acquisition, not necessarily the equity cheque. **Deal date:** the Náš Chléb article is dated 2025-07-30, but Jet's own press release says it entered in June 2025. Evidence: PEKAŘI a spol., 100% via Jet 3, 2026-09-11 (Jet website, tier A, plus CzechCrunch, tier B); Náš Chléb, 80% via Jet 3, 2025-07-30 (CzechCrunch, tier B). |
| arx | include | pe | **All deal evidence is from ARX's own website** (tier A, dated press releases); I found no media coverage of the deals. Deals: Medicofit (SI) 2026-08-26, Direct4me (SI) 2026-03-16, HLB PROXY (CZ) 2026-01-30. **Capital:** ARX CE V target €100m (`target_fund_size`), first close €78m in 10/2024. I could not find a final close, and fund domicile is unknown. **Ticket** is null: the website gives only the value of target companies (€10–50m). ARES also lists ARX Equity Co-Invest a.s. (IČO 19161239, set up 2023); its link to ARX is not verified. Note that arx.cz is an unrelated accounting firm. Registry: Arx Equity Partners s.r.o. (64943356), Praha 1, which matches the website. |
| bensonoak | inactive (E6) | pe | **No PE investment found after 2023-10-22.** The latest documented one is Click Insurance (08/2011, investor website), and the website (bensonoakcapital.com) has no news since 2012. **Registry:** the IČO is uncertain. ARES has Benson Oak, spol. s r.o. (41190106, founded 1991, consulting), but its address does not match the website's (Rašínovo nábřeží). The fund itself is a Dutch cooperative (Benson Oak Capital Coöperatief U.A.). **Separate VC arm:** Benson Oak Ventures (Web3/B2C, offices in Tel Aviv, Prague, London and NY; $100m fund announced in 2018) is a different VC vehicle whose team seems to be in Israel. I did not include it here or check its recent activity; it could be a separate candidate but is probably out of scope. |
