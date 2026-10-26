# Sub-agent 18: Blind verify V5

Spuštěn: 2026-10-22 17:19  
Použité nástroje: WebFetch 17×, WebSearch 9×, Bash 3×, Read 1×, Write 1×, PowerShell 1×

## Zadání, které agent dostal

Read C:\Users\vital\Desktop\Clode_Trading\investor-db\docs\prompt-verifier-agent-v2.md and follow it exactly. Today is 2026-10-22. Load WebSearch/WebFetch via ToolSearch if needed. You are a BLIND verifier: read only data/blind/<id>.json and PLAN.md; do not open data/records_raw, data/records or data/quote_check.csv.

Your ids: fazole, limerock, directpro, iibio, partnersinnov, 3ts

## Závěrečná zpráva agenta

I checked all six ids blind. I read only PLAN.md and data/blind/<id>.json, and checked every claim against its URL with WebFetch, plus WebSearch where needed. The CSVs are written (8 rows each) to C:\Users\vital\Desktop\Clode_Trading\investor-db\data\verification_v2\{fazole,limerock,directpro,iibio,partnersinnov,3ts}.csv.

| id | wrong | null_missed | most serious problem |
|---|---|---|---|
| fazole | 0 | 0 | Capital `basis: own_balance_sheet` is not supported by the source, so I marked it unverifiable. The ticket is right in the source (1–20 mil. CZK), but its EUR values are null because the fx conversion never ran. |
| limerock | 2 | 2 | `out_of_scope` should be E6 (inactive): its only fund invested 2014–2016, no deal from 2023 or later turned up, and every portfolio company on its site is marked "Exited". The record name is also wrong: it is Limerock Advisory s.r.o. / Limerock Fund Manager, not "Limerock Ventures". Two public figures are missing: 12 mil. EUR fund (previous_fund_size) and max 2.75 mil. EUR ticket. Both are old, and the ticket comes only from an aggregator. |
| directpro | 0 | 0 | None. Exclude under I2 holds: the sub-fund was created 2025-11-11 and no deal was found. Direct PRO mostly holds the group's own companies, so E7 is worth considering too. |
| iibio | 1 | 0 | Stages leave out `pre_seed`: the site says "We can start at €150k to support business creation." Also, IČO 10885978 belongs to "Biotech Investments s.r.o." (the Prague 8 adviser), and only the shared address links it to i&i Bio. The €45M figure dates from 2021. |
| partnersinnov | 1 | 0 | Exclude is right, but rule E7 does not fit: this is a SICAV fund aiming for financial return, not a strategic buyer. The correct rule is I2 (fund founded 2026, no investment documented). |
| 3ts | 0 | 0 | None blocking. `out_of_scope` holds because the current team lists no Prague partner. `generalist` is imprecise (the source says technology, media, tech-enabled services). The Patronus date of 2026-05-04 is the Heuking press-release date; the round was announced 2026-04-28. |

Totals: 4 wrong, 2 null_missed, 1 unverifiable.
