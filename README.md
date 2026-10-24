# Spolehlivá databáze investorů

Řešení praktické úlohy (zadání A) k pozici Junior AI Developer.

Cílem bylo navrhnout, jak sestavit spolehlivou databázi investorů do firem, a ověřit to na menším vzorku.
Pilot jsem udělal na **investorech v Česku**. Výsledkem je **43 ověřených investorů všech typů ze zadání**.
U každého údaje je odkaz na veřejný zdroj, ze kterého pochází.

---

## Výsledek v kostce

| | |
|---|---|
| **Databáze** | 43 investorů: 25 VC fondů, 5 investičních skupin podnikatelů, 4 korporátní fondy, 3 private equity, 3 andělé, 2 family office, 1 andělský syndikát |
| **Vyřazeno** | 28 subjektů, které podle pravidel investory nejsou (crowdfunding, sítě, neaktivní fondy, prodejci investic…) |
| **Přesnost** | ruční kontrola náhodného vzorku: **35 z 35 údajů odpovídá zdroji**; nezávislá AI kontrola surových dat: 86–93 % |
| **Úplnost** | proti oficiálnímu katalogu CzechInvest; první kolo našlo 66 % investorů, další kola chybějící dohledala |
| **Odhad pro celý svět** | 30–50 tis. investorů, náklady na první naplnění **≈ 85–125 tis. EUR** |

**Kde začít:**
- 📊 [**Databáze investorů (Excel)**](data/Databaze_investoru.xlsx): jeden řádek = jeden investor, klik na hodnotu otevře zdroj
- 📋 [**ODEVZDANI.md**](ODEVZDANI.md): odpovědi na všechny body zadání, včetně placených databází a jejich cen
- 📐 [**PLAN.md**](PLAN.md): kdo do databáze patří a kdo ne, jak se to ověřuje, kolik investorů lze získat
- 📈 [**RESULTS.md**](RESULTS.md): podrobné výsledky, měření přesnosti a odhad nákladů

---

## Jak jsem postupoval

Nejdřív bylo potřeba úplně a do hloubky analyzovat zadání. Použil jsem k tomu **tři AI agenty**:

- **Agent 1** (Claude Code na Windows) a **agent 2** (Claude Code na Macu) řešili úlohu každý samostatně a vytvořili vlastní řešení.
- **Třetího agenta** (konzultace s AI DeepSeek a Gemini) jsem použil pro vlastní průzkum: kde a jak získat
  data o investorech.

Když první dva agenti skončili, **propojil jsem jejich výstupy přes git**, aby si navzájem viděli výsledky.
Agent 2 napsal kritické hodnocení řešení agenta 1 a agent 1 na něj odpověděl ([reviews/](reviews/)).
Pak jsem je nechal pracovat dál samostatně.

Mezitím jsem s třetím agentem hledal **zdroje dat**:
- Stáhl jsem exporty z **registru České národní banky** a **katalog investorů portálu CzechStartups** (CzechInvest).
- Dalším zdrojem by byly **placené databáze** (Apify, Crunchbase, PitchBook…). Jsou ale zpoplatněné a zadání chce
  jen veřejná data, proto jsem je nepoužil. Ceny a důvody jsou v [ODEVZDANI.md](ODEVZDANI.md#placené-databáze-proč-nejsou-použité-a-kolik-by-stály).

Všechny exporty jsem pak předal agentům k analýze, aby byl výsledek co nejpřesnější. Tak vznikla tři kola pilotu:

| kolo | co se dělalo | výsledek |
|---|---|---|
| 1 | VC fondy z médií a veřejných přehledů | 22 investorů |
| 2 | kandidáti z oficiálního katalogu CzechInvest a registru ČNB | +14 investorů; zjištění, že první kolo jich třetinu přehlédlo |
| 3 | doplnění dalších typů ze zadání: private equity, family office, andělé | +7 investorů |

Nakonec jsem **ručně zkontroloval náhodný vzorek**: 6 investorů × 5 údajů, každý proti zdroji.

---

## Jak pracovala AI

### Kdo co dělal

V řešení agenta 1 pracovalo několik AI agentů s jasně oddělenými rolemi:

- **Hlavní agent** napsal plán, pravidla a programy. Rozdělil práci ostatním a vyhodnocoval jejich výsledky.
- **Rešeršní agenti** (13 běhů) dohledávali o každém kandidátovi informace na webu. Pravidla:
  - použít jen stránky, které sami otevřeli,
  - u každého údaje uvést odkaz a **doslovnou citaci** ze zdroje,
  - když údaj nenajdou, nechat pole prázdné. **Nikdy nic neodhadovat.**
- **Ověřovací agenti** (12 běhů) znovu otevřeli zdroje a hledali chyby. Od druhého kola pracovali **naslepo**:
  dostali jen tvrzení a odkaz, ne citaci rešeršního agenta, takže ji museli najít sami.

Doslovné pokyny, které agenti dostali, jsou ve složce [docs/](docs/).

### Jak jsem kontroloval, že AI nevymýšlí

AI agenti umějí vymyslet zdroj nebo citaci. Proto má kontrola pět vrstev a každou dělá někdo jiný:

1. **Program ověří každou citaci.** Stáhne zdrojovou stránku a hledá v ní citaci. Ze 494 citací nebyla ani jedna vymyšlená.
2. **Nezávislý ověřovací agent** zkontroluje každý údaj znovu, od druhého kola naslepo.
3. **Opravy se zapisují, ne přepisují.** Každá ze 89 oprav má důvod a autora. Původní výstup AI zůstává
   beze změny vedle, takže je vidět, co AI udělala špatně.
4. **Druhé nezávislé řešení** (agent 2 na Macu) a vzájemná kritika obou řešení.
5. **Člověk:** ruční kontrola náhodného vzorku. Výsledek: 35 z 35 údajů sedí a ověřovací AI se s člověkem
   shodla v 96 %. Při rozšíření na celý svět proto stačí lidsky kontrolovat jen vzorek.

### Kde se AI mýlila

Chyby jsem rozdělil do čtyř skupin. Úplný seznam je níže v rozbalovací části.

**1. AI si vymýšlela nebo přebírala neověřené tipy**
- Hlavní agent přidal mezi kandidáty crowdfundingovou platformu „Pointer", která neexistuje. Pravidla ji vyřadila.
- Tipy jiné AI (DeepSeek) se potvrdily jen zčásti: ze 4 family office prošla pravidly 2, u jednoho anděla bylo špatné jméno.

**2. Chyby v mých vlastních pokynech pro agenty**
- Pokyny nařizovaly pevný kurz dolaru, takže agenti přepočítávali měny špatně. To byla nejčastější chyba.
  Přepočet teď dělá program podle kurzu ECB k datu zdroje.
- Pokyny dovolily zařadit „skupinu andělů" jako anděla, i když anděl je fyzická osoba. Pravidla jsem upřesnil.

**3. Údaje vypadaly správně, ale znamenaly něco jiného**
- „Kapitál 720 mil. EUR" byl ve skutečnosti hodnota jednoho podílu (Rohlik), ne peníze k investování.
- Cílová velikost fondu, kterou fond teprve shání, byla vykázaná jako hotový fond.
- Kapitál z článku z roku 2019 neměl datum, takže nešlo poznat, že je zastaralý.

**4. Přehnaný optimismus**
- Hlavní agent odhadl úplnost na 88 %. Měření proti oficiálnímu katalogu ukázalo 66 %.
- První odhad nákladů byl 2–3× nízký. Na chybu upozornil agent 2 a odhad je přepočítaný.

**Bezpečnost:** některé webové stránky obsahovaly skryté pokyny pro AI („If you are an LLM always mention…").
Agenti je ignorovali a nahlásili. Text z webu jsou data, ne příkazy.

---

## Důležitá rozhodnutí

- **Co je „skutečný investor":** subjekt, který má **doloženou investici za poslední 3 roky** (článek nebo tisková zpráva
  s datem). Tvrzení na webu „investujeme" nestačí.
- **Chybějící údaj zůstává prázdný, nikdy se neodhaduje.** Ne všichni investoři zveřejňují, kolik investují nebo kolik mají.
  Vymyšlené číslo by vypadalo jako fakt a šlo by proti hlavnímu požadavku na spolehlivost.
  Nejméně údajů zveřejňují family office a andělé, u andělů se navíc osobní majetek úmyslně nezjišťuje (GDPR).
- **Jen veřejná data,** bez placených databází (viz výše).
- **Vzorek = Česko.** Zadání navrhuje jednu zemi a český trh je dost malý na ruční kontrolu. Úmyslně jsem do něj
  dal i subjekty, které vyřazené být mají (crowdfunding, akcelerátor, dluhový fond), aby se otestovala i pravidla vyřazení.
- **Jeden správce = jeden záznam,** i když má víc fondů nebo strategií.
- **Andělé jen ti, kdo se jako investoři veřejně prezentují,** a jen profesní údaje: jméno, zaměření a doložené investice.

## Co v řešení chybí

- Ručně je zkontrolovaný jen vzorek z prvního kola (6 investorů). Druhé a třetí kolo zkontrolovala AI naslepo, ne člověk.
- Private equity, family office a andělé jsou ověření na malém vzorku (12 kandidátů).
- Úplnost: ani oficiální katalog nezná všechny investory. V Česku je aktivních investorů nejméně 43; kolik přesně, z veřejných zdrojů spolehlivě změřit nejde.
- U některých webových zdrojů chybí archivní snímek stránky, takže zpětně nejde doložit, co na ní v den kontroly bylo.
- Několik hraničních případů k ručnímu dořešení (např. NEWTON University Angels: investice zřejmě jsou, ale bez data).

---

<details>
<summary><b>Úplný seznam chyb AI (24 položek)</b></summary>

| chyba | kdo | jak se na to přišlo | co se změnilo |
|---|---|---|---|
| Kandidát „Pointer" jako crowdfundingová platforma; taková neexistuje | hlavní agent | rešeršní agent ho nedohledal | kandidát musí mít zdroj (PLAN §7.8) |
| Národní rozvojový fond jako státní VC fond; nikdy neinvestoval | hlavní agent | rešeršní agent | dtto |
| Pevný kurz 0,92 USD/EUR v pokynech, v rozporu s plánem | hlavní agent | ověřovací agent, u 8 údajů | přepočet dělá program ([src/fx.py](src/fx.py)) |
| Sektory a fáze odvozené ze 2–3 investic místo z deklarovaného zaměření | rešeršní agenti | ověřovací agent | jen z mandátu (PLAN §7.3) |
| Pale Fire jako private equity, i když plán ho uvádí jako investiční skupinu | rešeršní agent | ověřovací agent | oprava typu |
| Investice připsaná fondu, i když investoval zakladatel osobně (Impulse) | rešeršní agent | ověřovací agent | doklad odstraněn |
| Investice doložená jen agregátorem s domyšleným datem (StartupYard) | rešeršní agent | ověřovací agent | neaktivní (PLAN §7.4) |
| 3 chyby v programu na kontrolu citací | hlavní agent | ruční pohled do stažených stránek | opraveno |
| Agent poslal e-mail uživatele v hlavičce požadavku na SEC EDGAR | rešeršní agent | agent to sám nahlásil | zákaz osobních údajů v požadavcích |
| Genesis (PE) v kole, které bylo jen pro VC | hlavní agent | review agenta 2 | přeřazeno, ve 3. kole zařazen |
| Kapitál Lighthouse z roku 2019 bez data | rešeršní agent | review agenta 2 | datum doplněno, měří se aktuálnost (PLAN §7.9) |
| Odhad nákladů 2–3× nízký (statistiky agentů ≠ účtované tokeny) | hlavní agent | review agenta 2 | přepočteno (RESULTS §5) |
| Ověřovací agent v 1. kole viděl citace rešeršního agenta | hlavní agent | review agenta 2 | od 2. kola slepé ověření |
| IČO Nation 1 z výsledku vyhledávání, který agent neotevřel | rešeršní agent | review agenta 2 | doloženo adresářem CVCA |
| Důkaz Tensoru jen z agregátoru | rešeršní agent | review agenta 2 | nahrazen článkem |
| Andělské „skupiny" jako anděl (fyzická osoba) | hlavní agent (pokyny) | slepý ověřovatel | typ „andělský syndikát"; síť bez vlastní investice vyřazena (PLAN §7.15) |
| Cílová velikost fondu vykázaná jako hotový fond (4×) | hlavní agent (schéma) | slepý ověřovatel | nové označení „cíl fondu" (PLAN §7.17) |
| IČO mateřské banky místo investující dceřiné firmy (Seed Starter ČS) | rešeršní agent | slepý ověřovatel | opraveno |
| Dva agenti si ve sdíleném adresáři přepsali pomocný program | infrastruktura | agent to sám nahlásil | výsledky beze změny; každý agent má vlastní adresář |
| Odhad úplnosti 88 % | hlavní agent | oficiální katalog CzechInvest | změřeno 66 % (RESULTS §3b) |
| Tipy DeepSeek: 2 ze 4 family office neprošla, špatné jméno anděla | DeepSeek | rešeršní agent | tipy jiných AI se ověřují jako vše ostatní (PLAN §7.24) |
| Typ „family office" převzatý z agregátoru (TCF, BHM) | rešeršní agent | slepý ověřovatel | rozhoduje, jak se subjekt sám označuje (PLAN §7.21) |
| „Kapitál" = hodnota jednoho podílu (TCF) / aktiva celé skupiny (BHM) | rešeršní agent | slepý ověřovatel | správné označení, co číslo znamená |
| Jet Investment a jeho VC fond jako dva investoři | hlavní agent | rešeršní agent (stejné IČO) | sloučeno (PLAN §7.22) |

</details>

<details>
<summary><b>Všechny soubory v repozitáři</b></summary>

| soubor | obsah |
|---|---|
| [ODEVZDANI.md](ODEVZDANI.md) | odpovědi na všechny body zadání, placené databáze, hlavní rozhodnutí |
| [PLAN.md](PLAN.md) | definice investora, pravidla zařazení/vyřazení, ověřování, odhad velikosti světa, úpravy po pilotu (§7) |
| [RESULTS.md](RESULTS.md) | výsledky všech tří kol, přesnost, úplnost, rozbor chyb, náklady |
| [data/Databaze_investoru.xlsx](data/Databaze_investoru.xlsx) | výsledek pro čtení (43 investorů + vyřazení + vysvětlivky) |
| [data/investors_cz_vc.csv](data/investors_cz_vc.csv) | totéž strojově: u každého údaje odkaz, datum a spolehlivost zdroje |
| [data/excluded.csv](data/excluded.csv) | 28 vyřazených s pravidlem a důvodem |
| [data/records/](data/records/) | plné záznamy (JSON) po opravách: citace, fondy, všechny doložené investice |
| [data/records_raw/](data/records_raw/) | totéž beze změny, jak to vrátili rešeršní agenti |
| [data/corrections.json](data/corrections.json) | 89 oprav s důvodem a autorem |
| [data/quote_check.csv](data/quote_check.csv) | strojová kontrola 494 citací |
| [data/verification/](data/verification/), [data/verification_v2/](data/verification_v2/), [data/blind/](data/blind/) | verdikty ověřovacích agentů a slepé podklady |
| [data/manual_check.csv](data/manual_check.csv) | ruční kontrola vzorku |
| [data/reference_czechstartups.csv](data/reference_czechstartups.csv), [data/recall.csv](data/recall.csv) | katalog CzechInvest a měření úplnosti |
| [docs/](docs/) | doslovné pokyny agentům, zadání, kontrola proti zadání, analýza zdrojů |
| [reviews/](reviews/) | vzájemná kritika agentů 1 a 2 |
| [ai-log/](ai-log/) | export konverzace s Claude Code |

</details>

<details>
<summary><b>Jak to spustit</b></summary>

```bash
pip install requests beautifulsoup4 openpyxl
python src/apply_corrections.py      # původní výstup AI + opravy → finální záznamy, přepočet měn kurzem ECB
python src/check_quotes.py           # stáhne zdroje a ověří citace
python src/build.py                  # tabulky, pokrytí údajů podle typu, aktuálnost zdrojů
python src/measure.py                # přesnost (AI ověření po kolech, ruční kontrola, shoda AI × člověk)
python src/recall.py                 # úplnost vůči katalogu CzechInvest
python src/simple_xlsx.py databaze   # Excel „Databáze investorů“
python src/simple_xlsx.py kontrola   # Excel „Ruční kontrola“ (zachová už zadané odpovědi)
python src/simple_xlsx.py import     # vyplněná kontrola → data/manual_check.csv
```

</details>
