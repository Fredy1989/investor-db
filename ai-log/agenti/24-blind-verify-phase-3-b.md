# Sub-agent 24: Blind verify phase 3 B

Spuštěn: 2026-10-23 08:09  
Použité nástroje: WebFetch 17×, WebSearch 15×, Bash 11×, Grep 2×, Read 1×, Write 1×, Edit 1×

## Zadání, které agent dostal

Read C:\Users\vital\Desktop\Clode_Trading\investor-db\docs\prompt-verifier-agent-v2.md and follow it exactly. Also read docs/prompt-research-agent-v3.md section "změny v3" – for this batch PE, family offices and individual angels ARE in scope (PE buyouts count; angels are natural persons, need ≥2 documented investments with ≥1 after 2023-10-22; angel capital is intentionally null for GDPR reasons – treat that as null_ok). Today is 2026-10-23. Load WebSearch/WebFetch via ToolSearch if needed. You are a BLIND verifier: read only data/blind/<id>.json, PLAN.md and the prompt files; do not open data/records_raw, data/records or data/quote_check.csv. Use your own uniquely named scratch directory (e.g. scratchpad/verify3_b/) for any scripts. For natural persons, do not collect or write any private personal data.

Your ids: arx, bhm, dendis, najvarek

## Závěrečná zpráva agenta

I checked all four records blind and wrote one CSV per record, with one row for each claim. Of the 32 claims, 2 are `wrong` and 2 are `null_missed`, all in bhm and dendis. arx and najvarek have no errors.

| id | wrong | null_missed | Most serious problem |
|---|---|---|---|
| arx | 0 | 0 | None. Two minor points: `consumer` in sectors is only a loose reading of "lifestyle services", and `growth` in stages is weakly supported. |
| bhm | 2 | 0 | `investor_type` is `family_office`, but BHM calls itself an "investiční skupina" (investment group) on its own website and in the deal press release. Only the aggregator Altss calls it a family office. Under PLAN §1 the right type is `private_investor`. |
| dendis | 1 | 2 | The cited HTG Medical deal was made by the vehicle Dendis Capital nadační fond, not by Miloš Dendis by name. So `registry` is `null_missed`: it should be 19786514, confirmed in ARES. The type should be `family_office`, or `angel` with that vehicle as the registry (v3 rule 4). |
| najvarek | 0 | 0 | None. The exclusion under I3 holds: five searches found only a Garage Angels investor profile and no documented tier A/B investment. |

**arx**
- The Medicofit majority buyout on 2026-08-26 is documented, and the ARES record and the Prague headquarters match.
- Capital of EUR 100m with basis `target_fund_size` is correct. The first close was EUR 78m and the hard cap is EUR 125m. I found no final close.
- Ticket `null_ok`: the page gives only target company valuations of EUR 10–50m, not an equity ticket.

**bhm**
- **Stages (wrong):** the stages field is derived from the evidence, and Rein Medical was a full acquisition, so only `buyout` is supported, not `growth`.
- **Decision:** `include` is defensible because BHM repeatedly buys companies (Medifa, Brandon Medical, Schaerer Medical) and also sells them. But the evidence deal is an add-on bought through its portfolio company Reinsberg Group, so there is some risk under rule E7.
- **Capital:** the EUR 1.1bn on the homepage is labelled "AKTIVA", meaning total group assets including real estate, not money available to invest.

**dendis**
- **Investor type (wrong):** the website field is also missing; it should be https://dendiscapital.com/.
- **Stages (`null_missed`):** this is minor. dendiscapital.com and the HTG round point to `pre_seed` and `seed`.
- **Decision:** `include` is fine. There is a public investor profile, and dendiscapital.com lists 8 portfolio companies. HTG Medical alone has a 2025 and a 2026 round.
- **Capital:** left null for GDPR, so it is `null_ok`.

**Access notes**
- The businessinfo.cz page returned 403 to WebFetch, so I fetched it with curl, which worked.
- g-angels.cz is stuck in a redirect loop, so the najvarek rows have no verbatim quotes.

I did not open records_raw, records or quote_check.csv, and I stored no private personal data for the natural persons. My helper script is `C:\Users\vital\AppData\Local\Temp\claude\C--Users-vital-Desktop-Clode-Trading\e35f7c62-fc82-48c6-a51c-4b5dc5f05dd4\scratchpad\verify3_b\write_csv.py`.

Files are in C:\Users\vital\Desktop\Clode_Trading\investor-db\data\verification_v2:
- arx.csv
- bhm.csv
- dendis.csv
- najvarek.csv
