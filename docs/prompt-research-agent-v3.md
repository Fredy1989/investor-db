# Pokyny pro rešeršního agenta, v3 (fáze 3: PE, family office, jednotliví andělé)

Fáze 1–2 ověřily pravidla jen na VC-like investorech. Fáze 3 je ověřuje na zbylých typech ze zadání.
Platí v2 ([prompt-research-agent-v2.md](prompt-research-agent-v2.md)) s těmito **změnami v3, které mají přednost**.

---

Přečti `C:\Users\vital\Desktop\Clode_Trading\investor-db\docs\prompt-research-agent-v2.md` (a přes něj v1 a PLAN.md §1–2, §7)
a postupuj podle nich s těmito změnami:

1. **Rozsah vzorku fáze 3:** investoři se sídlem / týmem v Česku typu `pe`, `family_office`, `angel`.
   PE buyouty a podíly ve zralých soukromých firmách **jsou v rozsahu** (pravidlo v2 bod 7 tady neplatí).
2. **Private equity (`pe`):** I2 = doložená investice (akvizice podílu, buyout, růstový kapitál) do soukromé firmy
   za posledních 36 měsíců. Tiket a kapitál bývají v desítkách až stovkách milionů EUR. Velikost fondu uveď s `basis`
   (`latest_fund_size` jen u uzavřeného fondu, cíl = `target_fund_size`).
3. **Family office (`family_office`):** musí **samo přímo** investovat do soukromých firem. Správa majetku, investice
   jen do fondů nebo jen do kotovaných akcií a nemovitostí = E5 / I4. Když jde o průmyslovou skupinu, která kupuje
   firmy do svého podnikání, je to E7. Když FO investuje přes holding, `registry` = ten holding.
4. **Jednotlivý anděl (`angel`, fyzická osoba):**
   - I1 = veřejný profesní profil (rozhovor, článek, profil v asociaci / na webu). `registry` = `null`
     (nebo IČO jeho investiční s.r.o., pokud přes ni prokazatelně investuje).
   - I3 = **aspoň 2 doložené investice** (tier A/B), z toho aspoň 1 po 2023-10-22.
   - Když osoba investuje hlavně jako partner fondu, který už v DB je, a ne vlastními penězi, dej `exclude` / `E8` s poznámkou.
5. **GDPR u fyzických osob (povinné):** ukládej **jen profesní údaje**, které osoba sama zveřejnila nebo které
   veřejně uvedla média v souvislosti s investováním: jméno, investiční zaměření, doložené investice a jejich zdroje.
   **Nikdy** neukládej soukromé kontakty, bydliště, datum narození, osobní majetek ani rodinné poměry. Kapitál anděla
   (osobní majetek) nezjišťuj; `capital` = `null` s poznámkou „neuvádí se – osobní údaj".
   Zařazuj jen osoby, které se jako investoři **samy veřejně prezentují**.
6. `"phase": 3` místo 2. Ukládej do `data/records_raw/<id>.json`, jiné soubory neměň.
