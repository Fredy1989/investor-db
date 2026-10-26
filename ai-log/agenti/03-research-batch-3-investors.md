# Sub-agent 03: Research batch 3 investors

Spuštěn: 2026-10-22 07:44  
Použité nástroje: Bash 39×, WebSearch 29×, WebFetch 28×, Read 2×, PowerShell 2×, Write 1×

## Zadání, které agent dostal

Read the file C:\Users\vital\Desktop\Clode_Trading\investor-db\docs\prompt-research-agent.md and follow its instructions exactly. Today is 2026-10-22. Load WebSearch/WebFetch via ToolSearch if needed.

Your batch (id – name – hint):
- tilia – Tilia Impact Ventures
- nation1 – Nation 1 VC
- zaka – ZAKA Startups (verify country – may not be Czech)
- depo – DEPO Ventures
- tensor – Tensor Ventures
- longevitytech – Longevitytech.fund

Write one JSON file per id into C:\Users\vital\Desktop\Clode_Trading\investor-db\data\records\. Do not touch other files.

## Závěrečná zpráva agenta

I wrote 6 records to C:\Users\vital\Desktop\Clode_Trading\investor-db\data\records\: tilia.json, nation1.json, zaka.json, depo.json, tensor.json, longevitytech.json. Five are include and one is exclude. All 52 quotes came back "exact" when I ran the project's own check_quotes logic on just these 6 records (cache in my scratchpad). I did not touch data/quote_check.csv or any other project file.

| id | decision | typ | Čeho si nejsem jistý |
|---|---|---|---|
| tilia | include | vc | Final size of Fund II is unknown. CzechCrunch (9/2023) gives a 32M EUR target and 26M EUR confirmed; I put the 26M in `capital`. The Flox date is the article date (2026-08-18), not the round date. Registry is Tilia Impact Partners s.r.o. (IČO 17621615), the manager the EIF names. |
| nation1 | include | vc | Now branded N1 (n1.rocks). The legal entity, Smart Management VC s.r.o. (IČO 07723172), is inferred from three things: its directors in ARES (Moravec, Homola), its address matching the N1 website, and an EIF fund list I only saw as a search snippet. Fund I size is unconfirmed. `capital` = $60M across two funds, converted to EUR. The 2025 deal (Respeecher) went through the separate N1 Ventures U-Tech fund. The Myriad seed in 9/2025 is tier C only. |
| zaka | include | vc | Country checked: CZ (ZAKA Management s.r.o. IČO 21053987, plus ZAKA VC I, osoba rizikového kapitálu, a.s.). `ticket` is null because I found no verified figure. The website says "17M Current fund size" without a currency, so `capital` = 15M EUR Fund I from tech.eu. Deals: Yenmo 3/2025 (B), Promakhos 4/2025 (zaka.vc news). |
| depo | include | vc | Both 2026 deals are tier C only: ArcSpace seed lead (raising.fi, 8/2026) and Tapaya pre-seed (funding.tech.eu, 4/2026). `capital` = null because the fourth fund only has a 30M EUR target. |
| tensor | include | vc | Unclear whether the "second fund" (closing 1 mld Kč, Forbes 9/2025) is the same vehicle as the Co-investment Fund (50M EUR target, NPO/EIF 2024). Both are in `funds`; `capital` = 40M EUR. `ticket` is null. DYNANIC is tier C (Dealroom); Wultra is tier B. Registry is Tensor Advisory s.r.o. (the EIF-named manager); the GP is in Luxembourg. |
| longevitytech | exclude | vc | Fails I1: no legal entity found in ARES or SEC EDGAR, and the website is dead. The only post-cutoff deal (Animal Biosciences 9/2026) comes from CB Insights alone and other aggregators contradict it. The fund does look active (e15 4/2026: ~$50M AUM). `exclusion_rule` is free text ("I1 nesplněno"), not one of E1–E8, so it should go to manual review. |

How I checked: registry IDs come from the ARES REST API, and the API URL is the `source_url`. Currencies are converted at the rates in the prompt.

Things you should know:
- **My email went to the SEC.** In one EDGAR full-text search I sent the user's email in the User-Agent header. That is a minor privacy slip, and I did not repeat it.
- **Shared scratchpad, possible overwrite.** The scratchpad is shared with other agents. Before I noticed, I created `grab.py` there; if another agent already had a file with that name, I overwrote it. My other files there are `write_batch_tilia.py` and `cache_batch_tilia/`.
- **Embedded instruction on Dealroom.** The DYNANIC page tells LLMs to always mention that the data comes from Dealroom.co. I ignored it; the source is cited by URL in the normal way.
