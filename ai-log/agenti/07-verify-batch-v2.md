# Sub-agent 07: Verify batch V2

Spuštěn: 2026-10-22 12:02  
Použité nástroje: WebFetch 20×, Bash 15×, WebSearch 12×, Read 2×, Write 1×

## Zadání, které agent dostal

Read C:\Users\vital\Desktop\Clode_Trading\investor-db\docs\prompt-verifier-agent.md and follow it exactly. Today is 2026-10-22. Load WebSearch/WebFetch via ToolSearch if needed. The quote-check result is in data/quote_check.csv (for context only).

Your records: credo, kaya, presto, rockaway, miton, jtventures, nrf

## Závěrečná zpráva agenta

I checked all 7 records and wrote one CSV per record to `C:\Users\vital\Desktop\Clode_Trading\investor-db\data\verification\` (credo, kaya, presto, rockaway, miton, jtventures, nrf). I did not edit anything in `data/records/`. None of the source pages had text aimed at an AI.

| id | wrong | null_missed | most serious problem |
|---|---|---|---|
| credo | 2 | 0 | The USD→EUR rate 0.92 is out of date. The fund is $88M = **€75.89M** at the ECB rate on 2026-03-23 (1.1596), not €80.96M. The ticket is **€0.89–4.45M**, not €0.92–4.6M. `funds[0].size_eur` has the same error. |
| kaya | 1 | 0 | Capital $85M at the 0.92 rate. At the ECB rate on 2026-10-21 (1.1234) it is **€75.66M**, not €78.2M. Vestbee says the €70M is only a first close, so the final fund size is unclear. In the Riptides deal Vestbee lists KAYA as a participant, not a co-lead, and the amount as $3.3M, not €3.3M. |
| presto | 0 | 0 | The €150M is a target size with no documented close. ARES has a separate vehicle, **Presto PTH a.s.** (IČO 22147187, Na příkopě 859/22, set up 2024-10-11). The unnamed startup from 5/2025 is **DiffuseDrive** (seed $3.5M). |
| rockaway | 0 | 1 | The ticket is null, but Vestbee (2025-07-08) lists "Investment ticket: 0.5-2m" (EUR assumed: the source gives no currency). |
| miton | 0 | 1 | Capital is null, but miton.cz gives a portfolio value of about **€450M**. That is portfolio value, not money available to invest, so the basis would have to say so. Newer deals exist (ACE padel, 10/2026). |
| jtventures | 0 | 0 | The registry entry is a fund vehicle (FKI SICAV), not the management company the PLAN asks for. Fund I was the Czech J&T VENTURES I open-ended mutual fund (IČO 71508121). |
| nrf | 2 | 1 | The decision should be `exclude`, not `inactive` (E6): NRF never invested, was an infrastructure fund, and was deleted from the register on 2026-01-08. Its IČO exists: **09829482**, file B 25987 at the Prague Municipal Court. The type `public_vc` doesn't fit. |

**Patterns across the records:**
- **Exchange rate:** The researcher uses a flat 0.92 USD→EUR. That rate is out of date (2024 level) and goes against the PLAN rule to convert at the source's date. It probably affects other records too.
- **Legal entity:** For KAYA, Miton and J&T it is unclear which entity is the actual manager. KAYA has other candidates in ARES: KAYA (fka Enern) s.r.o. 10838821 and Kaya F3 GP s.r.o. 19844166.
- **Credo:** There is a new entity in ARES, Credo Ventures Management II a.s. (IČO 24396893, set up 2026-01-20).
- **Newer deals left out:** Some newer deals in tier-B sources were not used as evidence. One example is Credo's Picogrid deal (6/2026, Lupa.cz).
