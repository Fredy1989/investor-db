# Sub-agent 05: Research batch 5 investors

Spuštěn: 2026-10-22 07:44  
Použité nástroje: WebSearch 26×, WebFetch 24×, Bash 20×, Read 4×, Write 1×

## Zadání, které agent dostal

Read the file C:\Users\vital\Desktop\Clode_Trading\investor-db\docs\prompt-research-agent.md and follow its instructions exactly. Today is 2026-10-22. Load WebSearch/WebFetch via ToolSearch if needed.

Your batch (id – name – hint). Several of these are deliberate edge cases to test the exclusion rules – decide strictly by the rules and document evidence:
- nrf – Národní rozvojový fond (state-backed; fund of funds or direct investor?)
- startupyard – StartupYard (accelerator; does it have its own investment vehicle taking equity? rule E2)
- fundlift – Fundlift (crowdfunding platform, rule E1)
- pointer – Pointer (crowdfunding / investment platform, rule E1)
- genesis – Genesis Capital / Genesis Ventures (PE with a VC arm – decide type)

Write one JSON file per id into C:\Users\vital\Desktop\Clode_Trading\investor-db\data\records\. Do not touch other files.

## Závěrečná zpráva agenta

I wrote all 5 records. Every quote except the ones from pointer.cz matched, word for word, against the page text I fetched with curl (and ARES JSON for the registry quotes). Each file is in `C:\Users\vital\Desktop\Clode_Trading\investor-db\data\records\` (nrf.json, startupyard.json, fundlift.json, pointer.json, genesis.json). The records folder already held other agents' files; I left those untouched.

| id | decision | type | what I'm unsure of |
|---|---|---|---|
| nrf | inactive (E6) | public_vc (rough) | IČO not found: nrf.cz didn't respond and the ARES name search returned an error. |
| startupyard | include | vc | Thin I2 evidence (see below). |
| fundlift | exclude (E1) | – | Whether the platform is still running in 2025–2026 is not shown. |
| pointer | exclude ("I1") | – | Not identified at all; "I1" is outside the E1–E8 list. |
| genesis | include | pe | No company website (it didn't respond), so tier A is ARES only. |

**Decisions on the edge cases:**

- **nrf:** It was neither a fund of funds nor a direct investor. It was a SICAV under Národní rozvojová banka meant for public infrastructure, and it never backed a single project (ČT24, Seznam Zprávy, Novinky). At its own request ČNB withdrew its licence, effective 2024-05-03. The state fund that does invest in companies is Národní rozvojová investiční (NRI, runs IPO fond 2025+). That is a different entity and should be its own candidate.
- **startupyard:** E2 does not apply. ARES shows a separate company per batch (Batch 14 s.r.o. founded 2023-12-07, Batch 15 s.r.o. founded 2024-11-14). Per its FAQ it invests through a convertible note worth €45k in kind plus an optional €25k cash, targeting about 5% equity. Only one named deal falls after 2023-10-22: Personeo.ai, April 2024, from the Caplight aggregator (tier C). The Batch 14 (April 2024) and Batch 15 (September 2025) announcements don't name any companies, and StartupYard's own profile posts never say it invested. The deal date is recorded as 2024-04-01 because the source gives only "Apr 2024".
- **fundlift:** Fundlift, s.r.o. (IČO 03876292) is an equity crowdfunding platform run by Roklen. No investments of its own were found.
- **pointer:** No Czech crowdfunding or investment platform called Pointer could be found. The ARES matches (PoInter, s.r.o., IČO 25120263, and POINTER a.s.) are IT/engineering firms, and pointer.cz is an IT services site. E1 couldn't be proven, so I recorded it as failing I1. The pointer.cz quote came from WebFetch only, because the site blocks curl (HTTP 466). Someone should check what platform was meant.
- **genesis:** Genesis Capital Equity s.r.o. (IČO 25795856) is a mid-market PE group. No Prague "Genesis Ventures" VC arm exists in any source I found; the search hits were unrelated Greek, Chilean, Spanish and Japanese funds. Its only non-buyout fund is the GGEF I growth fund (EUR 40m). AmCham (June 2026) says the GGEF I team will now operate independently of Genesis, so it may be worth a separate record. Evidence for Genesis itself:
  - Deals: Slevomat (2025-11-19, from the newest fund GPEF V) and GAF (2024-03-13, from GPEF IV).
  - Ticket: EUR 10–45m.
  - Capital: GPEF V at EUR 286m as of June 2026; reported sizes differ by date (225m at launch, 270m in November 2025).
  - Older funds are listed in the record.
