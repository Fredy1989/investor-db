# Sub-agent 04: Research batch 4 investors

Spuštěn: 2026-10-22 07:44  
Použité nástroje: WebFetch 33×, WebSearch 21×, Write 6×, Bash 5×, Read 1×

## Zadání, které agent dostal

Read the file C:\Users\vital\Desktop\Clode_Trading\investor-db\docs\prompt-research-agent.md and follow its instructions exactly. Today is 2026-10-22. Load WebSearch/WebFetch via ToolSearch if needed.

Your batch (id – name – hint):
- springtide – Springtide Ventures
- palefire – Pale Fire Capital
- ysoft – Y Soft Ventures (corporate VC; check activity in last 36 months – rule E6)
- czechfounders – Czech Founders VC
- iplab – Czech IP Lab Ventures (technology-transfer fund with EIF commitment; check whether it already invested)
- aspire11 – Aspire11 (Prague, reportedly EUR 500M fund, part fund-of-funds; decide type / I3)

Write one JSON file per id into C:\Users\vital\Desktop\Clode_Trading\investor-db\data\records\. Do not touch other files.

## Závěrečná zpráva agenta

I wrote all 6 records to C:\Users\vital\Desktop\Clode_Trading\investor-db\data\records\ (springtide.json, palefire.json, ysoft.json, czechfounders.json, iplab.json, aspire11.json). Five are included and IP Lab is excluded under I2. Every file loads as valid JSON. I touched no other files; the other records now in the folder come from parallel agents.

| id | decision | type | Uncertain about |
|---|---|---|---|
| springtide | include | cvc | Ticket of 3–10M USD comes from e15 (2021). Only one deal falls in the 36-month window: ThreatMark, 8M USD convertible note, 2025-01-07. springtide.vc is a parked domain for sale. cvc vs vc/family_office is a judgement call: it is a 100% subsidiary of KKCG Technologies. Aggregators mix it up with the US SpringTide Ventures (Boston). |
| palefire | include | pe | The only private deal since 2023-10 is the Zwift stake taken in the ROUVY sale (2026-04-30), which is effectively a share swap. Most recent activity is listed shares (Edenred, Dole, Lightspeed). The EUR 2B AUM includes public holdings. Ticket ("hundreds of millions to over a billion CZK") is left null. pe vs family_office is debatable. |
| ysoft | include | cvc | E6 does not apply: it co-invested in RoboTwin's EUR 1.25M round (announced 2025-07-02). Ticket and capital come only from a 2014 article, so the numeric fields are null. Registry was confirmed only on mesec.cz (tier C). |
| czechfounders | include | vc | Latest deal I verified is Edmund (2025-02-12). PitchBook lists 2026 deals that I did not verify. Fund size of EUR 10M dates from 2022. Sectors set to null (website lists none). Legal name from ARES: "Czech Founders Ventures s.r.o., osoba rizikového kapitálu", IČO 17051835. |
| iplab | exclude (I2) | vc | EIF committed about EUR 27M to IP Lab Ventures Fund I (09/2026), but I found no portfolio investment yet. Target size differs across sources (>50M EUR / up to 40M EUR / 1.2 bn CZK). The legal entity is unresolved: ARES has IP Lab Advisor/Holding/Services s.r.o., but no source links them to the fund. Worth re-checking later. |
| aspire11 | include | vc | Counts as I3: 300 of the EUR 500M go to direct growth investments and only 100M to the fund-of-funds. Deals: Revolut (2025-12) and Vinted, EUR 20M (2026-06); sources don't say whether these were primary or secondary shares. Record is Aspire 11 Capital Partners, s.r.o. (IČO 23602597), but its role as manager vs adviser is not verified. The fund-of-funds is formally run by Partners investiční společnost. The EUR 500M is the declared size, not necessarily committed capital. |

Notes:
- Where no fixed register page was available, the registry fields use the ARES REST JSON URLs (ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/<IČO>).
- In iplab.json, exclusion_rule is "I2" (an inclusion rule that isn't met) rather than an E-code, because no E-code fits.
- Many quotes were taken from WebFetch output, which a small model extracts and can slightly alter; a few may fail the automatic quote check, especially palefire's Zwift fragment and the threatmark.com sentence.
