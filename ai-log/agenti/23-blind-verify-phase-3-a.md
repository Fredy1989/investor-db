# Sub-agent 23: Blind verify phase 3 A

Spuštěn: 2026-10-23 08:09  
Použité nástroje: WebFetch 14×, Bash 9×, WebSearch 6×, Read 1×, Write 1×

## Zadání, které agent dostal

Read C:\Users\vital\Desktop\Clode_Trading\investor-db\docs\prompt-verifier-agent-v2.md and follow it exactly. Also read docs/prompt-research-agent-v3.md section "změny v3" – for this batch PE, family offices and individual angels ARE in scope (PE buyouts count; angels are natural persons, need ≥2 documented investments with ≥1 after 2023-10-22; angel capital is intentionally null for GDPR reasons – treat that as null_ok). Today is 2026-10-23. Load WebSearch/WebFetch via ToolSearch if needed. You are a BLIND verifier: read only data/blind/<id>.json, PLAN.md and the prompt files; do not open data/records_raw, data/records or data/quote_check.csv. Use your own uniquely named scratch directory (e.g. scratchpad/verify3_a/) for any scripts. For natural persons, do not collect or write any private personal data.

Your ids: jetinvest, tcf, hlavenka, obluk

## Závěrečná zpráva agenta

I checked all four records blind and wrote a CSV for each, with one row per claim. There is 1 `wrong` (tcf capital) and 1 `null_missed` (hlavenka ticket). All four decisions hold.

| id | wrong | null_missed | most serious issue |
|---|---|---|---|
| jetinvest | 0 | 0 | No errors. The 10–60M EUR ticket is the value of one acquisition, not an equity ticket; the "od 10 milionů" in the cc.cz headline is the investor's minimum commitment (400k EUR). The Forbes article used for sectors and capital is paid content made with Jet Investment (BrandVoice), so it is closer to tier A than B. |
| tcf | 1 | 0 | **capital**: the 720M EUR quote exists in newstream, but cc.cz (6/2023) says 720M EUR is the value of Čupr's ~42% stake in Rohlik Group, not capital to invest. It should be null or carry that note. |
| hlavenka | 0 | 1 | **ticket**: the record is inconsistent. `original` has min 500,000 CZK but `min_eur` is null. Public figures exist (from 0.5M CZK in 2020; "nízké jednotky milionů korun" in 2021), but both sources are over 36 months old. |
| obluk | 0 | 0 | Exclude under I3 holds: two searches found no documented personal investment after 2023-10-22. His current role is partner at Evolution Equity Partners (a foreign VC), so the v3 rule "invests mainly as a fund partner" would also fit. The decision has no `source_url`. |

Notes by record:
- **jetinvest:** Every claim is ok.
  - The PEKAŘI a spol. deal (11. 9. 2026, Jet 3 fund, 100% stake) is confirmed on Jet Investment's own site.
  - ARES confirms IČO 03890333, Jet Investment, a.s., Brno.
  - The Jet 4 target "přes 300 milionů eur" is correctly labelled `target_fund_size`; other outlets give up to 350M EUR.
- **tcf:**
  - The Töpfer Babywelt deal is confirmed (Forbes, 2025-05-12); TCF Capital invested, not Čupr personally.
  - **Type:** `family_office` is defensible: Deloitte and Techleap call it Čupr's "Family Office TCF Capital". Its own site and Forbes say "investiční skupina", though, which matches PLAN's `private_investor`. The boundary between those two types should be made explicit in PLAN.
  - **Registry:** 09000909 (TCF-Cap Services s.r.o.) is confirmed by tcfcap.com/legal and ARES. Per finmag.cz, part of its assets moved to Casually Holding a.s. (IČO 23314061) on 1. 10. 2025, so it is unclear which entity holds the portfolio.
  - **Sectors:** the current website says "technologie a dlouhověkost", so health is missing.
  - **Ticket:** the 30–50M EUR figure comes from a 2023 article and describes a plan.
- **hlavenka:**
  - Elredo (1. 10. 2026, round led by JIC Ventures, Hlavenka joined) is confirmed.
  - At least 2 documented tier-B investments are satisfied by older deals: Twigsee, Reknihy and Loklok (cc.cz, 2020), plus FaceUp and Cleany (sj.news, 2021).
  - Jinej fond is not documented as a legal vehicle, so `angel` is correct.
  - Capital null is ok (GDPR).

No private personal data was collected for Hlavenka or Obluk. I did not open records_raw, records or quote_check.csv.

Files are in C:\Users\vital\Desktop\Clode_Trading\investor-db\data\verification_v2:
- jetinvest.csv
- tcf.csv
- hlavenka.csv
- obluk.csv

The script that wrote them is C:\Users\vital\AppData\Local\Temp\claude\C--Users-vital-Desktop-Clode-Trading\e35f7c62-fc82-48c6-a51c-4b5dc5f05dd4\scratchpad\verify3_a\write_csv.py.
