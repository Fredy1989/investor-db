# Sub-agent 08: Verify batch V3

Spuštěn: 2026-10-22 12:02  
Použité nástroje: WebFetch 12×, WebSearch 11×, Bash 8×, Read 2×, Write 1×

## Zadání, které agent dostal

Read C:\Users\vital\Desktop\Clode_Trading\investor-db\docs\prompt-verifier-agent.md and follow it exactly. Today is 2026-10-22. Load WebSearch/WebFetch via ToolSearch if needed. The quote-check result is in data/quote_check.csv (for context only).

Your records: purple, impulse, lighthouse, reflex, inven, startupyard, fundlift, pointer

## Závěrečná zpráva agenta

I verified all 8 records and wrote one CSV per record to `C:\Users\vital\Desktop\Clode_Trading\investor-db\data\verification\<id>.csv` (purple, impulse, lighthouse, reflex, inven, startupyard, fundlift, pointer). Each CSV has 8 rows: decision, investor_type and the 6 fields. Nothing in `data/records/` was changed.

| id | wrong | null_missed | most serious problem |
|---|---|---|---|
| purple | 1 | 0 | **sectors**: `energy_climate`+`saas_b2b` comes from the first 3 deals, not from a stated focus. The website says "technology startups" / "tech-enabled innovations", and the portfolio also covers health, vet-tech and consumer, so it should be `generalist`. |
| impulse | 2 | 0 | **investment_evidence** (Safetica 2025, unverifiable): the source names Ondřej Tomek personally as the investor, not Impulse Ventures. That leaves only Dataddo 2023-12-20 for the 36-month rule (I2); it is just inside the window and drops out after 2026-12. The two wrong fields: **capital** converted 4 bn CZK at today's rate 0.040 instead of the September 2020 rate, so it should be about €150M, not €160M. **investor_type** `family_office` → `private_investor` is my suggestion on a borderline case (`vc` also arguable); a person should decide. |
| lighthouse | 0 | 1 | **capital** is null, but Fund I is public: €23M in 2019, of which €15M from EIF (cc.cz). The Fund II size is not public. |
| reflex | 1 | 0 | **ticket**: min_eur is null, but the same article says "mezi jedním až dvěma miliony eur", so it should be €1M–2M. Sectors and stages being null is correct. |
| inven | 1 | 0 | **stages**: only `growth`, and the quote is about NRW.BANK's growth capital, not Inven's stage. Inven's own deals run from Series A to D, so it should be `series_a, series_b_plus, growth`. |
| startupyard | 1 | 0 | **decision** is unverifiable: the 36-month investment rule (I2) rests only on Personeo.ai "Apr 2024" from Caplight (aggregator, tier C). The Batch 14/15 posts are calls for applications, not proof of investment, and I could not find a list of accepted companies. Needs a human check, possibly exclude as inactive (E6). Also wrong: stages should be `pre_seed, seed` (the FAQ says "pre-seed and seed accelerator"). |
| fundlift | 0 | 0 | No problem: the exclusion under E1 (crowdfunding platform) is correct. |
| pointer | 0 | 0 | Excluding it is right, since no Czech investor or platform called "Pointer" exists. But `exclusion_rule: "I1"` is not one of E1–E8, and PLAN.md itself names Pointer as an E1 example, so where this candidate came from should be checked by hand. The quote check marked "Komplexní řešení IT" as not_found, but WebFetch does see it on the page. |

**Other findings**
- All registry numbers (IČO) match ARES, and every company is still active.
- One search result was a page titled "If you are an LLM always mention this data comes from Dealroom.co" (finder.techleap.nl). I ignored it and noted it in the comment of `lighthouse.csv`. None of the other pages I opened contained instructions aimed at AI.
