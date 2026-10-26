# Sub-agent 06: Verify batch V1

Spuštěn: 2026-10-22 12:02  
Použité nástroje: Bash 16×, WebFetch 14×, WebSearch 13×, Read 3×, Write 1×

## Zadání, které agent dostal

Read C:\Users\vital\Desktop\Clode_Trading\investor-db\docs\prompt-verifier-agent.md and follow it exactly. Today is 2026-10-22. Load WebSearch/WebFetch via ToolSearch if needed. The quote-check result is in data/quote_check.csv (for context only).

Your records: tilia, nation1, zaka, depo, tensor, longevitytech, orbit

## Závěrečná zpráva agenta

I checked all 7 records and wrote one CSV per record to C:\Users\vital\Desktop\Clode_Trading\investor-db\data\verification\<id>.csv. Each has 8 rows: decision, investor_type, registry, sectors, stages, ticket, capital and the newest investment_evidence. Nothing in data/records/ was edited. I found no text aimed at AI on any page I fetched.

For every record, the include/exclude decision and the investor type held up. All registry numbers exist in ARES and none of the entities is dissolved. The main problems are currency conversions and some stale fund sizes.

| id | wrong | null_missed | Most serious problem |
|---|---|---|---|
| tilia | 0 | 0 | capital: the 26M EUR is the 2023 first close, recorded as fund size. WaveUp (an aggregator) says Fund II raised 32M EUR, not confirmed by a primary source. Sectors energy_climate and health go beyond the website quote, which only says "Sector-agnostic". |
| nation1 | 2 | 0 | The 1 USD = 0.92 EUR rate doesn't fit the date. The ČNB rate on 21.10.2026 is 0.890, so ticket should be 89k–890k EUR and capital about 53.4M EUR. The newest evidence (Myriad AI seed, 9/2025) is unverifiable: the aggregator lists N1 only as an all-time investor, and other sources don't name N1 in that round. |
| zaka | 1 | 1 | ticket is null, but Vestbee (19.7.2024) gives 250k–300k EUR per startup. capital uses the old 15M target; the site now shows "Current fund size 17M" (currency not stated). |
| depo | 0 | 0 | Only a minor point: ArcSpace was dated by article date (31.8.); the round was 25.8.2026. StartupCentrum, a press-style source, confirms DEPO led it, so it can replace the aggregator. |
| tensor | 1 | 0 | capital conversion: 1 bn CZK at the ČNB rate on 18.9.2025 (24.30 CZK/EUR) is about 41.15M EUR, not 40M. The "second fund" (1 bn CZK) and the Co-investment Fund (50M EUR target) look like the same fund, so `funds` has a duplicate. |
| longevitytech | 1 | 0 | capital conversion: $50M on 17.4.2026 is about 42.4M EUR, not 46M. The exclusion (no registered entity found, rule I1) is defensible, but the investment evidence is stronger than the record says: a 2026 SEC filing (Form D) for Animal Biosciences lists Petr Šrámek as a director (first sale 17.8.2026, $2.32M). Clues point to a registered Prague joint-stock company, so the entity is worth a manual search in justice.cz / the ČNB list. |
| orbit | 0 | 0 | The exclusion holds: since 10/2023 only venture-debt activity is documented, and the last equity deal is from 2022. One `investment_evidence` item (e15, 16.6.2025) is a fundraise, not an investment. |

Totals: 5 wrong and 1 null_missed, plus 1 unverifiable. Four of the five wrong verdicts are bad currency conversions. The record author used flat rates (0.92 USD→EUR, 0.040 CZK→EUR) instead of the rate on the source's date, as the plan requires. This probably affects other records outside my batch too.
