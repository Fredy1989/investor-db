# Sub-agent 17: Blind verify V3

Spuštěn: 2026-10-22 17:19  
Použité nástroje: WebFetch 21×, WebSearch 7×, Bash 4×, Read 1×, Write 1×

## Zadání, které agent dostal

Read C:\Users\vital\Desktop\Clode_Trading\investor-db\docs\prompt-verifier-agent-v2.md and follow it exactly. Today is 2026-10-22. Load WebSearch/WebFetch via ToolSearch if needed. You are a BLIND verifier: read only data/blind/<id>.json and PLAN.md; do not open data/records_raw, data/records or data/quote_check.csv.

Your ids: lookai, kbsmart, rsj, jsk, aternus, purposetech

## Závěrečná zpráva agenta

I checked all 6 ids blind, reading only data/blind/<id>.json and PLAN.md. I opened every source URL myself and did a few extra web searches. I found 5 `wrong` claims, no `null_missed`, and no wrong `decision`.

Results are in C:\Users\vital\Desktop\Clode_Trading\investor-db\data\verification_v2\ as lookai.csv, kbsmart.csv, rsj.csv, jsk.csv, aternus.csv and purposetech.csv, one row per claim (8 each).

| id | wrong | null_missed | most serious problem |
|---|---|---|---|
| lookai | 2 | 0 | **ticket:** €250k is the starting ticket, not the max. AIN 2023 says "start from €250,000 and can reach up to €1 million of reinvestment capital". **capital:** €20M is a 2023 fundraising target, not a closed fund. It should be `target_fund_size`, and I found no close. |
| kbsmart | 1 | 0 | **investor_type `cvc`:** PLAN §1 defines cvc as the investment arm of a *non-financial* company, and KB is a bank. Either broaden the definition or change the type. |
| rsj | 0 | 0 | No errors. Two notes: RSJ Tech and Angel Tech mainly invest in other VC funds (fund-of-funds), and `deeptech` comes from one underlying fund (Lunar), not RSJ's own mandate. |
| jsk | 1 | 0 | **capital:** the website says "TARGET FUND SIZE €20M", so the basis should be `target_fund_size`, not `latest_fund_size`. The only firm figure is €10M of internal capital. |
| aternus | 1 | 0 | **sectors `generalist`:** the website names technology, marketplaces, SaaS, fintech and deep tech (plus real estate). It should map to saas_b2b, fintech, deeptech and ecommerce. |
| purposetech | 1 | 0 | **capital:** the record holds "just under 60M CZK" as the latest fund, but that is the first fund. The newest fund, PT Capital, is up to €10M (240M CZK) per cc.cz, 10 Feb 2026, and the EUR value is null. |

Three other things to check, recorded as `ok` with a comment:
- **lookai:** the registry number belongs to the fund vehicle "Look AI Ventures SICAV, a.s.", which may not be the manager (§7.5). I couldn't find who manages it.
- **kbsmart:** `inactive`/E6 holds up. Buying the last 4% of Upvest in 2025 tidies up a subsidiary rather than making a new venture investment. The last real new investment was in 8/2022. E7 is a possible alternative rule.
- **purposetech:** the investment evidence is a portfolio summary with no dated deal (Tingit 2/2026 and Lifeyear 7/2025 only appear on funding.tech.eu, which is tier C). Separately, aternus has two possible registry entities: ATERNUS, a.s. and Aternus Family Office s.r.o.

One limitation: I copied the `found_quote` values from the fetch tool's extracts of each page, not from the raw HTML.
