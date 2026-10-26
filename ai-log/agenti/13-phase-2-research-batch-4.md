# Sub-agent 13: Phase 2 research batch 4

Spuštěn: 2026-10-22 17:06  
Použité nástroje: Bash 34×, WebFetch 22×, WebSearch 15×, Read 4×, Grep 1×, Write 1×

## Zadání, které agent dostal

Read C:\Users\vital\Desktop\Clode_Trading\investor-db\docs\prompt-research-agent-v2.md and follow it exactly (it tells you to read the v1 prompt and PLAN.md too; v2 rules take precedence). Today is 2026-10-22. Load WebSearch/WebFetch via ToolSearch if needed. Candidate context is in data/candidates_phase2.csv.

Your batch (id – name):
- 3ts – 3TS Capital Partners (check where the team/manager is based)
- maccelerator – mAccelerator.vc (mBank; check where the team/manager is based)
- jetventure – Jet Venture 1 (VC arm of Jet Investment; fund in ČNB register)
- jsk – JSK Investments (Venture Capital Fund I; in ČNB register)
- czegg – CZEGG Ventures (podfond of STARTEEPO SICAV a.s.; in ČNB register)
- directpro – Direct PRO Ventures (podfond of Direct PRO SICAV; in ČNB register)

Write one JSON per id into data/records_raw/<id>.json with "phase": 2. Do not touch other files. Return a short table: id, decision, type, what you are unsure about.

## Závěrečná zpráva agenta

I wrote all six records to `C:\Users\vital\Desktop\Clode_Trading\investor-db\data\records_raw\` (`3ts.json`, `maccelerator.json`, `jetventure.json`, `jsk.json`, `czegg.json`, `directpro.json`), each with `"phase": 2`. No other files were touched. Two are included, two are out of scope (no Czech team) and two are excluded.

Before writing, I compared every quote against the text of the page I actually downloaded, and all of them matched. Registry numbers come from the ARES records I opened. Amounts are kept in the source currency in `original`, and no currencies were converted.

| id | decision | type | what I am unsure about |
|---|---|---|---|
| 3ts | out_of_scope | vc | **Team location:** one undated job-portal profile (tier C) lists offices in Vienna, Warsaw, Bucharest, Budapest, Bratislava and the US, with no Prague. `country=AT` is my guess from Vienna being listed first; headquarters is not confirmed and their team page returns 404. The firm itself is active (it led Patronus, €11M, 2026-05-04, via TCEE Fund IV). I did not check the manager's registry entry. |
| maccelerator | out_of_scope | cvc | **Team location:** the Warsaw base is supported only by an aggregator (Altss). The fund belongs to Poland's mBank and Czechia is only a target market. maccelerator.vc is now a hosting company's "under construction" page, and I found no deal after 2019, so E6 would also apply. I did not open a Polish registry entry. |
| jetventure | include | vc | **Manager:** the registry field holds Jet Investment, a.s. (IČO 03890333). I did not confirm in the ČNB register that it formally manages Jet Venture 1 SICAV (IČO 22030417). The deal evidence is four deals (GigaScan, Phantasma Labs, Hermetiq, AppNava) from one CzechCrunch article of 2026-09-17, so each deal carries the article date. The stage values `series_a`/`series_b_plus` are my reading of "pozdějších fázích" (later stages). The link to "Jet Venture 1 fond fondů OPF" (IČO 75165228) is unclear. |
| jsk | include | vc | **Type:** `vc` or `family_office` — it is a dedicated VC sub-fund with its own team and outside investors, but the money originally comes from the Kijonkovi family. The €20M is the target size of the VC sub-fund, and the quote covers only the "€10M internal capital" line because the page puts the figures on separate lines. The deals are MintNeuro (2026-10-10) and Andromeda Surgical (2026-09-15); both sources say the fund invested, not Kijonková personally. |
| czegg | exclude (E5) | pe | **Rule:** E5 versus I2 or out_of_scope. The only mandate source is a 2020 Forbes article: established family manufacturers that must list on the Prague exchange, 25–50M CZK per issuer. STARTEEPO's site today shows IPO advisory and trades in listed shares only. Only one of the four PDFs on the site downloaded (an SFDR disclosure), so I could not read the fund statute. I found no startup deals. |
| directpro | exclude (I2) | cvc | **Rule and type:** the sub-fund has existed in ARES since 2025-11-11, but I found no strategy, website or deal. The parent fund Direct PRO is a vehicle for funding the Direct group (that reads more like E7). `cvc` is a guess. Rechecking later or reading its ČNB filing is advisable. |

**Other notes:**
- **AI instruction in search results:** a Dealroom page title in the results contained an instruction aimed at LLMs. I ignored it, never opened Dealroom, and recorded this in the `maccelerator` notes as rule 11 requires.
- **Extra JSON fields:** I added three fields the schema doesn't define, in case the build or validation step rejects them: `country_evidence` (3ts, maccelerator), `mandate_evidence` (czegg), and `original` / `domicile` / `registry` inside `funds[]`.
- **Overlap with an existing record:** Phantasma Labs was co-funded by Lighthouse Seed Fund II, which already has a record (`lighthouse`). This is noted in the `jetventure` notes.

