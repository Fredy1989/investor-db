# Sub-agent 01: Research batch 1 investors

Spuštěn: 2026-10-22 07:44  
Použité nástroje: WebFetch 40×, WebSearch 28×, Bash 7×, Read 1×

## Zadání, které agent dostal

Read the file C:\Users\vital\Desktop\Clode_Trading\investor-db\docs\prompt-research-agent.md and follow its instructions exactly. Today is 2026-10-22. Load WebSearch/WebFetch via ToolSearch if needed.

Your batch (id – name – hint):
- credo – Credo Ventures
- kaya – KAYA VC
- presto – Presto Ventures
- rockaway – Rockaway Ventures (Rockaway Capital)
- miton – Miton (invests own capital, no LPs)
- jtventures – J&T Ventures (CZ/SK; determine HQ country honestly)

Write one JSON file per id into C:\Users\vital\Desktop\Clode_Trading\investor-db\data\records\. Do not touch other files.

## Závěrečná zpráva agenta

I wrote all 6 records, and every file parses as valid JSON. They are in C:\Users\vital\Desktop\Clode_Trading\investor-db\data\records\ as credo.json, kaya.json, presto.json, rockaway.json, miton.json and jtventures.json. No other files were touched.

| id | decision | type | uncertain about |
|---|---|---|---|
| credo | include | vc | The ARES quote is only the company name (Credo Ventures a.s.); the IČO 28538137 appears only in the source URL. Sources disagree whether the $88M fund 5 (3/2026) was a single close or a first close. Evidence: Delta Green (10/2025) and Modeinspect (1/2026). |
| kaya | include | vc | **The legal entity is unclear.** I used KAYA Advisory s.r.o. (IČO 22585737), which sits at the Prague office address. The historic fund vehicle is ENERN Investments SICAV (IČO 01790765). Fund V is €70M at first close (Vestbee) versus $85M on the website; I used the website figure. The Riptides deal (co-lead, €3.3M) is dated 4/2025, but that date comes only from Seedtable; the event page has no year. |
| presto | include | vc | The €150M Presto Tech Horizons fund is a **target**; I found no confirmed close. The newest deal I could verify is 5/2025, an unnamed Hungarian startup. The founder Přemysl Rubeš was detained by police in 3/2026; Presto says it ended cooperation with him in 9/2025, which is a risk to fund activity. The presto.vc domain is parked; the live site is prestoventures.com. |
| rockaway | include | vc | No ticket size is published anywhere, so it is null. Sector mapping to the taxonomy is approximate. Evidence: Filuta AI (lead, 6/2025), Remix 20% stake (12/2025), Apptronik (2/2026). |
| miton | include | private_investor | Invests its own money with no LPs. There are many MITON entities, and the parent could not be determined from the registry; I chose MITON C a.s. (IČO 19324448). The type could arguably be vc instead. Ticket €300k–2M comes from Miton's cc.cz profile. Evidence: Bandits, €400k (11/2025). |
| jtventures | include | vc | **HQ is CZ**: the website lists only a Prague office (Sokolovská 700/113a), and the funds are Czech SICAVs in ARES. Seedtable calls Definic its first investment in Slovakia. jtventures.sk did not resolve. The registry field uses the fund J&T Ventures III SICAV a.s. (IČO 22175903); I did not verify a separate management company. Individual fund sizes are unknown; AUM is €120M. Evidence: Definic seed, lead, €2.5M (6/2026). |

**Shared caveat:** for ARES the quote is the company name, because the API returns JSON and the IČO is visible only in the URL. Deals that appear only in aggregators are listed in `notes` and left out of `investment_evidence`.
