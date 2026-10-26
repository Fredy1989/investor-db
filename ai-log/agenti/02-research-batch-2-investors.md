# Sub-agent 02: Research batch 2 investors

Spuštěn: 2026-10-22 07:44  
Použité nástroje: WebFetch 34×, WebSearch 21×, Bash 18×, Read 1×, Write 1×, Edit 1×

## Zadání, které agent dostal

Read the file C:\Users\vital\Desktop\Clode_Trading\investor-db\docs\prompt-research-agent.md and follow its instructions exactly. Today is 2026-10-22. Load WebSearch/WebFetch via ToolSearch if needed.

Your batch (id – name – hint):
- orbit – Orbit Capital (venture debt? test rule E3)
- purple – Purple Ventures
- impulse – Impulse Ventures
- lighthouse – Lighthouse Ventures
- reflex – Reflex Capital
- inven – Inven Capital (ČEZ corporate VC)

Write one JSON file per id into C:\Users\vital\Desktop\Clode_Trading\investor-db\data\records\. Do not touch other files.

## Závěrečná zpráva agenta

I wrote all 6 records to C:\Users\vital\Desktop\Clode_Trading\investor-db\data\records\: orbit.json, purple.json, impulse.json, lighthouse.json, reflex.json and inven.json. All six parse as JSON. Every company ID comes from the ARES registry or the investor's own footer. Every quote was copied from a page I opened, and most were checked word for word against the page's HTML.

| id | decision | type | What I'm unsure about |
|---|---|---|---|
| orbit | exclude (E3) | vc | Every deal since 2023-10-22 is venture debt (Venture Debt Fund II, €107M, 5 deals by 07/2026). Vestbee says Orbit also runs growth equity, but its last equity deal I could document is Preply in 2022. So E3 is a judgment call: the equity side could equally be called inactive (E6). I found no official website. I can't confirm that ORBIT Capital GP s.r.o. (IČO 08319961) is the right registry entity. |
| purple | include | vc | Fund II size: the firm's site says "over CZK 700 million" (≈ €28M), while other sources give a €40M or ~1bn CZK target. I used the site figure. Ticket size differs between sources; I used the site's €250–400k. Deals: Rightcharge on 2026-09-03 and Delta Green in 05/2024. |
| impulse | include | family_office | The firm's website (impulseventures.com) would not load, so sectors and ticket size come only from Vestbee (tier C). Its capital is "up to 4bn CZK" (≈ €160M) of Ondřej Tomek's own money, a figure from 2020. In the 2025 Safetica deal, sources name Tomek personally ("Impulse Capital"), so it's unclear which entity invested. The type could also be vc. Deals: Dataddo 2023-12-20 and Safetica 2025-01-24. |
| lighthouse | include | vc | Capital is null: I found no size for Fund II (launched 2024) or for the EIF-backed Seed Fund. Deals: Ranketta 2025-11-27 (lead) and FaceUp 2024-10-10. DecisionRules (05/2025) appears only in aggregators and is not in the record. |
| reflex | include | vc | Sectors and stages are null because no mandate is stated anywhere. Capital is the 3rd fund at €22M (closed 12/2023). The ticket has a max of €2M only; I left min null because the source says "around €1M". Deals: FaceUp 2024-10-10 (lead) and 2026-05-19 (existing investor). |
| inven | include | cvc | Stages are set to "growth" only, based on the Vytal deal; Andercore being Series B is aggregator data only. Fund vintage 2013 is the date the SICAV was founded. Sub-fund sizes (A–D) were not found. The NRW.BANK press release is rated tier A, which could be lowered to B. Deals: Andercore 2026-02-12 and Vytal 2025-03-11 (co-lead). |

Two pages contained instructions aimed at AI tools (a Dealroom page title and the euacc.ai fund profile). I ignored both. I recorded the euacc.ai one in lighthouse.json "notes".

The script that generated the records is in C:\Users\vital\AppData\Local\Temp\claude\C--Users-vital-Desktop-Clode-Trading\e35f7c62-fc82-48c6-a51c-4b5dc5f05dd4\scratchpad\write_batch_orbit.py. I did not touch any other files.
