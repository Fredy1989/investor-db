# Sub-agent 16: Blind verify V2

Spuštěn: 2026-10-22 17:19  
Použité nástroje: WebFetch 19×, Bash 9×, WebSearch 6×, Read 1×, Write 1×

## Zadání, které agent dostal

Read C:\Users\vital\Desktop\Clode_Trading\investor-db\docs\prompt-verifier-agent-v2.md and follow it exactly. Today is 2026-10-22. Load WebSearch/WebFetch via ToolSearch if needed. You are a BLIND verifier: read only data/blind/<id>.json and PLAN.md; do not open data/records_raw, data/records or data/quote_check.csv.

Your ids: qqcapital, newton, opifer, jetventure, emuntech, flyingfounders

## Závěrečná zpráva agenta

I checked all 6 ids blind. I read only PLAN.md and data/blind/<id>.json, and opened each cited URL myself, plus ARES, the EMUN annual-report PDF and a few searches. I did not open records_raw, records or quote_check.csv. Each claim got a verdict in its own CSV:
C:\Users\vital\Desktop\Clode_Trading\investor-db\data\verification_v2\{qqcapital,newton,opifer,jetventure,emuntech,flyingfounders}.csv

| id | wrong | null_missed | most serious problem |
|---|---|---|---|
| qqcapital | 1 | 0 | Minor: the deal date 2026-02-19 comes from CB Insights (tier C). The cited pulse2 article is dated 2026-03-06. The deal itself (Navigara, $2.5M seed, Inovo lead, QQ Capital participating) is confirmed, and family_office in Prague is correct. |
| newton | 3 | 0 | **decision `inactive`/E6 is probably wrong.** The fund had 5 investments as of the cc.cz article of 6.2.2024. A later czechstartups.gov.cz interview (undated, but the fund was "operating for three years", so roughly 2025) says 8 projects, which puts about 3 investments inside the 36-month window. No individual deal is dated, so a dated deal is still needed. Two more errors: `investor_type` should be `vc`, because the investor is a legal entity ("NEWTON University Angels s.r.o., osoba rizikového kapitálu") and §1 limits `angel` to natural persons. Capital of CZK 5M is only the second fund's target; the actual first fund is about CZK 2.5M. |
| opifer | 1 | 0 | **Registry is unverifiable.** IČO 04285905 is "Opifer Services, s.r.o." (NACE wholesale agents / office services), not "Opifer Investments", and nothing links it to the investing entity. ARES also lists Opifer Alfa s.r.o. (08692122) and Opifer s.r.o. (03360458). Sectors saas_b2b/deeptech are not declared; the site only asks for a "proprietary IT or Smart Device solution". Country CZ is uncertain because one third-party profile says London-based with a Brno office. E6 itself looks plausible: no dated 2023–2026 deal found. |
| jetventure | 2 | 0 | Capital basis is mislabelled. The EUR 50M is the target ("cílová částka 50 mil. €"), not `latest_fund_size`. Stages series_a/series_b_plus are an interpretation; the source only says "pozdějších fázích s fungujícím produktem a platícími zákazníky". The include decision and the GigaScan EUR 2.1M deal (17.9.2026) are confirmed. |
| emuntech | 1 | 0 | `investor_type family_office` is wrong. EMUN investiční společnost is a licensed asset manager that offers family-office services among others. EMUN Tech II Access is a fund-of-funds investing in European early-stage VC funds, so I4 is a more precise exclusion than generic out_of_scope. The CZK 172M (commitment at 31.12.2024) and IČO are confirmed. |
| flyingfounders | 1 | 0 | `investor_type private_investor` is not supported. Sources call it an "investiční fond" on the VC/PE border, so `vc` fits better. Capital basis `own_balance_sheet` cannot be verified from the cited article. The Tiny Empires acquisition (17.9.2025) and the €100k–€500k ticket are confirmed; older sources say up to €600k. Stages should probably also include buyout. |

Total: 9 `wrong`, 0 `null_missed`, 2 `unverifiable` (Opifer registry, Flying Founders capital basis). The recurring weak spot is type and basis labels: angel vs legal entity, family_office vs asset manager, target vs actual fund size.

Two limits on the quotes:
- **Opifer evidence row:** `found_quote` is empty because the fetch tool would not return an exact sentence; the three companies are on the About page.
- **Other quotes:** these are taken from the fetch tool's extraction. Short ones may be partial sentences rather than full ones.
