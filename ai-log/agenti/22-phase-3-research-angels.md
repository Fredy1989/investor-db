# Sub-agent 22: Phase 3 research angels

Spuštěn: 2026-10-23 07:58  
Použité nástroje: WebFetch 35×, WebSearch 21×, Bash 15×, Read 1×, Write 1×

## Zadání, které agent dostal

Read C:\Users\vital\Desktop\Clode_Trading\investor-db\docs\prompt-research-agent-v3.md and follow it exactly (it tells you to read the v2 and v1 prompts and PLAN.md; v3 rules take precedence over v2, v2 over v1). Today is 2026-10-23; the 36-month activity window starts 2023-10-22. Load WebSearch/WebFetch via ToolSearch if needed. Candidate context: data/candidates_phase3.csv. Use your own uniquely named working directory for any scripts (e.g. scratchpad/phase3_angels/), never a shared filename.

These are natural persons: follow the GDPR rule (v3 point 5) strictly – store only professional, publicly self-presented investment information (name, investment focus, documented investments with sources). Never store private contacts, address, date of birth, personal wealth or family details; capital = null with note "neuvádí se – osobní údaj".

Your batch – individual angels (id – name):
- hlavenka – Jiří Hlavenka
- obluk – Karel Obluk (also partner of Evolution Equity – check whether he invests personally)
- dendis – Miloš Dendis
- najvarek – Jan Najvárek
- rostock – Michal Rostock

Write one JSON per id into data/records_raw/<id>.json with "phase": 3. Do not touch other files. Return a short table: id, decision, type, what you are unsure about.

## Závěrečná zpráva agenta

I wrote all 5 records to `C:\Users\vital\Desktop\Clode_Trading\investor-db\data\records_raw\<id>.json` with `"phase": 3`; three are `include` and two are `exclude`. All five are type `angel` and `country` CZ.

GDPR (v3 point 5) applied to all five: only professional investment data is stored. `capital` is null with "neuvádí se – osobní údaj", and `hq_city` is null for every person. No other files were touched. The writer script is at `C:\Users\vital\AppData\Local\Temp\claude\C--Users-vital-Desktop-Clode-Trading\e35f7c62-fc82-48c6-a51c-4b5dc5f05dd4\scratchpad\phase3_angels\write_phase3_angels.py`.

| id | decision | type | what I am unsure about |
|---|---|---|---|
| hlavenka | include | angel | Two deals name him personally, both tier B and after the cutoff: Elredo (cc.cz 2026-10-01) and FaceUp (cc.cz 2026-05-19). Two more went through Jinej fond (with Jan Sláma): TasteTown (2025-04-15) and HTG Medical (2026-07-14). It is unclear whether the Jinej fond deals count as his own; he passes I3 without them. Jinej fond's legal entity and IČO are not found, so `registry` is null. Sectors are null because no mandate is declared. The ticket figure is from 2020 and applies to Jinej fond. |
| obluk | exclude (I3) | angel | He calls his own angel investing occasional and small ("občas se drobně podílím", cc.cz 2024-10-17). I found no named, dated personal deal in a tier A/B source. Crunchbase lists Localazy but that is only an aggregator. I did not use E8 because Evolution Equity Partners is not in the DB and has no Czech team, so v3 point 4 does not formally apply. Please review that call. |
| dendis | include | angel | He invests through his vehicle "Dendis Capital": Carebot (Lupa 2026-01-08, €400k) and HTG Medical (Lupa 2026-07-14, existing investor; Vestbee confirms). The sector is health, from a JIC interview republished on businessinfo.cz on 2026-01-07. `registry` is null because I could not tell which legal entity invests. ARES shows three candidates: Dendis Capital Holding a.s. 21180237, Dendis Capital nadační fond 19786514 and DENDIS INVESTMENTS s.r.o. 21395594. Open question: should this be an `angel` record or a `family_office`/`private_investor` record for Dendis Capital? I left out the ownership detail Lupa gives because it is family data. |
| najvarek | exclude (I3) | angel | The only source I could open is the Lupa list of Garage Angels members, with no deal named. His ARTIN spin-offs are founder activity, not angel investing. g-angels.cz would not open (301 redirect loop), so I also could not confirm he presents himself publicly as an investor. |
| rostock | include | angel | The real name in all sources is **Michael Rostock-Poplar**, not "Michal Rostock". Please confirm it is the same person. His two deals: UltimateSuite with Tensor Ventures (cc.cz, round 12/2021) and the DecisionRules seed as an angel (cc.cz and ain.ua, both 2025-05-06). That meets I3. Sectors and stages are null. CBAA membership is not confirmed. |

Other findings:
- **Lupa VR Life article (2026-02-23):** its line "Mezi invetsory patří…" lists Garage Angels members generally. It is not evidence that any of these people invested in that round, so I only used it as a profile source.
- **Dishboard:** the Hlavenka deal reported by cc.cz on 2023-10-16 falls 6 days before the window, so it does not count.
- **Extra field:** the excluded records carry a `profile_evidence` array with quotes backing I1. This field is not in the v1 schema.
- **Quote wording:** some quotes came through the WebFetch summariser and are short fragments. They should still pass the machine check, but they have not been re-checked against the raw page text.
