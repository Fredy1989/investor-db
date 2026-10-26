# Sub-agent 19: Blind verify V4

Spuštěn: 2026-10-22 17:19  
Použité nástroje: WebFetch 25×, WebSearch 6×, Bash 4×, Read 1×, Write 1×

## Zadání, které agent dostal

Read C:\Users\vital\Desktop\Clode_Trading\investor-db\docs\prompt-verifier-agent-v2.md and follow it exactly. Today is 2026-10-22. Load WebSearch/WebFetch via ToolSearch if needed. You are a BLIND verifier: read only data/blind/<id>.json and PLAN.md; do not open data/records_raw, data/records or data/quote_check.csv.

Your ids: seedstarter, lumus, seeders, czegg, jic, garageangels

## Závěrečná zpráva agenta

I checked all six records blind. I read only PLAN.md and data/blind/<id>.json, never records_raw, records or quote_check.csv. Every listed URL was opened with WebFetch, and I used WebSearch to look for newer or missing data. I wrote six CSVs to C:\Users\vital\Desktop\Clode_Trading\investor-db\data\verification_v2\ (seedstarter.csv, lumus.csv, seeders.csv, czegg.csv, jic.csv, garageangels.csv), one row per claim, 8 claims each.

| id | wrong | null_missed | unverifiable | Most serious problem |
|---|---|---|---|---|
| seedstarter | 1 | 2 | 0 | **Wrong registry number.** 45244782 belongs to the parent bank, Česká spořitelna, a.s. The investing entity is the subsidiary ČS Seed Starter, a.s., IČO 61058769 (confirmed in ARES). Two values are public but recorded as null: the ticket is 200k–1M EUR and the sector is fintech, both on seedstarter.cz. The current website also lists pre_seed as a stage, which the record lacks. |
| lumus | 1 | 0 | 0 | **Wrong investor_type.** The record says `angel`, but PLAN defines angel as a natural person. Lumus Investment Collective s.r.o. is a syndicate that invests through an SPV, which the taxonomy does not cover. Only one deal is documented (Kardi AI, 2025-04), and I3 asks for ≥2 for angels. |
| seeders | 0 | 0 | 0 | No errors. Exclusion under I2 holds up: the website lists portfolio companies without dates, and two searches found no dated tier A/B deal. There is also no legal entity, so I1 fails as well. |
| czegg | 0 | 1 | 3 | **Capital wrongly null.** CzechCrunch (2024-05-27) reports a portfolio value of about 500 mil. CZK, which fits basis `portfolio_value`. The Forbes source shows only its headline (paywall), so sectors, stages and the 25–50 mil. CZK ticket are unverifiable. The registry number is the STARTEEPO SICAV fund vehicle, not the manager PLAN §7.5 asks for. Exclusion under E5 is borderline: the fund buys shares when a company is placed on the stock exchange. |
| jic | 0 | 0 | 0 | No errors. One caveat: 400 mil. CZK is the fund's target size, and media report about 320 mil. allocated so far. `vc` is correct rather than `public_vc`, because public money is only about 10–15%. |
| garageangels | 1 | 0 | 2 | **Wrong decision (`include`).** In ARES, Garage Angels is a z.s. (an association, founded 2024-07-13). Sources describe it as a group of individual investors and name the people investing. So the entity does not invest; its members invest personally, and the association itself fits E4. The Forbes ticket (400k EUR average) and capital (>300 mil. CZK) are unverifiable behind a paywall. |

Three problems in PLAN.md itself, not in a single record:
- **CVC definition:** PLAN §1 defines `cvc` as the arm of a non-financial company, but Seed Starter is a bank's arm.
- **Groups and syndicates:** the taxonomy has no type for angel syndicates or networks such as Lumus and Garage Angels.
- **Registry rule:** the "manager, not fund vehicle" rule from §7.5 is not followed for CZEGG.
