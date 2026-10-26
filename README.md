# Spolehlivá databáze investorů

Řešení praktické úlohy (zadání A) k pozici Junior AI Developer.

Cílem bylo navrhnout, jak sestavit spolehlivou databázi investorů do firem, a ověřit to na menším vzorku.
Pilot jsem udělal na **investorech v Česku**. Výsledkem je **43 ověřených investorů všech typů ze zadání**.
U každého údaje je odkaz na veřejný zdroj, ze kterého pochází.

---

## Výsledek v kostce

| oblast | výsledek |
|---|---|
| **Databáze** | 43 investorů: 25 VC fondů, 5 investičních skupin podnikatelů, 4 korporátní fondy, 3 private equity, 3 andělé, 2 family office, 1 andělský syndikát |
| **Vyřazeno** | 28 subjektů, které podle pravidel investory nejsou (crowdfunding, sítě, neaktivní fondy, prodejci investic…) |
| **Přesnost** | ruční kontrola dvou náhodných vzorků (12 investorů): **49 z 51 ověřitelných údajů odpovídá zdroji (96 %)**; na „čistém“ vzorku 91 %; nezávislá AI kontrola surových dat: 86–93 % |
| **Úplnost** | všech 30 investorů z oficiálního katalogu CzechInvest, kteří prošli pravidly, je v databázi. Katalog ale 13 z našich 43 investorů nezná, takže skutečnou úplnost lze odhadnout jen zdola |
| **Odhad pro celý svět** | 30–50 tis. investorů, náklady na první naplnění **≈ 85–125 tis. EUR** |

**Kde začít:**
- 📊 [**Databáze investorů (Excel)**](data/Databaze_investoru.xlsx): jeden řádek = jeden investor, klik na hodnotu otevře zdroj
- 📋 [**ODEVZDANI.md**](ODEVZDANI.md): odpovědi na všechny body zadání, včetně placených databází a jejich cen
- 📐 [**PLAN.md**](PLAN.md): kdo do databáze patří a kdo ne, jak se to ověřuje, kolik investorů lze získat
- 📈 [**RESULTS.md**](RESULTS.md): podrobné výsledky, měření přesnosti a odhad nákladů

### Ukázka databáze (10 ze 43 investorů)

Každá hodnota je odkaz na zdroj, ze kterého pochází. Celá databáze je v [Excelu](data/Databaze_investoru.xlsx) nebo strojově v [CSV](data/investors_cz_vc.csv).

| investor | typ | sektor | fáze | typická investice | celkový kapitál | poslední doložená investice |
|---|---|---|---|---|---|---|
| [Credo Ventures](https://www.credoventures.com) | VC fond | [bez omezení oboru](https://tech.eu/2026/03/23/credo-ventures-raises-88m-fund-5-to-double-down-on-pre-seed-in-cee-and-its-global-diaspora/) | [pre-seed, seed](https://www.credoventures.com) | [890 tis. EUR – 4,5 mil. EUR](https://www.credoventures.com) | [75,9 mil. EUR (poslední fond)](https://thenextweb.com/news/credo-ventures-88m-fund) | [Modeinspect (15. 1. 2026)](https://www.lupa.cz/n/credo-ventures/) |
| [KAYA VC](https://www.kaya.vc) | VC fond | [bez omezení oboru](https://www.kaya.vc) | [pre-seed, seed, série A](https://vestbee.com/blog/articles/kaya-secures-70-m) | [1 mil. EUR – 3 mil. EUR](https://vestbee.com/blog/articles/kaya-secures-70-m) | [75,7 mil. EUR (poslední fond)](https://www.kaya.vc) | [Riptides (23. 4. 2025)](https://www.vestbee.com/blog/articles/riptides-secures-3-3-m) |
| [Rockaway Ventures](https://www.rockawayventures.com) | VC fond | [e-commerce, spotřebitelé, mobilita, B2B software, obrana, energetika a klima](https://www.rockawayventures.com) | [seed, série A](https://www.rockawayventures.com) | [500 tis. EUR – 2 mil. EUR](https://www.vestbee.com/insights/articles/vc-of-the-month-rockaway-ventures) | [55 mil. EUR (poslední fond)](https://vestbee.com/insights/articles/rockaway-ventures-closes-55-m-fund) | [Apptronik (13. 2. 2026)](https://www.lupa.cz/n/rockaway-group/) |
| [Inven Capital](https://www.invencapital.cz/) | korporátní VC | [energetika a klima](https://www.invencapital.cz/) | [série A, série B+, růstová fáze](https://www.invencapital.cz/) | [2 mil. EUR – 30 mil. EUR](https://www.invencapital.cz/) | [500 mil. EUR (spravovaná aktiva)](https://www.invencapital.cz/) | [Andercore (12. 2. 2026)](https://www.deutsche-startups.de/2026/02/12/andercore-sammelt-40-millionen-ein-blockbrain-erhaelt-175-millionen-twentyfour-bekommt-118-millionen/) |
| [Seed Starter ČS](https://czechstartups.gov.cz/?investori=seed-starter) | korporátní VC | [fintech](https://www.seedstarter.cz/cs/uvod) | [seed](https://www.finance.cz/541902-seed-starter-cs) | [200 tis. EUR – 1 mil. EUR](https://www.seedstarter.cz/cs/uvod) | neuvedeno | [Definic (dříve Nordics), Košice (12. 6. 2026)](https://cc.cz/nakup-it-sluzeb-v-korporacich-je-casto-nefunkcni-hlasi-do-jejich-reseni-investuje-i-ceska-sporitelna/) |
| [Genesis Capital](https://www.genesiscapital.cz) | private equity | [bez omezení oboru](https://www.amcham.cz/member-news/genesis-announces-strong-year-investment) | [růstová fáze, buyout](https://www.unquote.com/cee/official-record/3027049/genesis-holds-eur-150m-final-close-for-gpef-iv) | [10 mil. EUR – 45 mil. EUR](https://www.amcham.cz/member-news/genesis-announces-strong-year-investment) | [286 mil. EUR (poslední fond)](https://www.amcham.cz/member-news/genesis-announces-strong-year-investment) | [Fyzioterapie s úsměvem (8. 4. 2026)](https://chambers.com/articles/j%C5%A1k-advises-genesis-capital-on-another-significant-investment) |
| [Jet Investment (PE + VC fond Jet Venture 1)](https://www.jetinvestment.cz/private-equity) | private equity | [průmysl, energetika a klima, zdraví, spotřebitelé](https://forbes.cz/znovu-a-jeste-lepe-faituv-jet-investment-pokracuje-v-jizde-otevira-dalsi-fond/) | [buyout](https://cc.cz/novy-fond-jet-4-chce-ozivit-stredoevropsky-prumysl-investorum-nabizi-primy-vstup-od-10-milionu/) | [10 mil. EUR – 60 mil. EUR](https://cc.cz/novy-fond-jet-4-chce-ozivit-stredoevropsky-prumysl-investorum-nabizi-primy-vstup-od-10-milionu/) | [300 mil. EUR (cíl fondu)](https://forbes.cz/znovu-a-jeste-lepe-faituv-jet-investment-pokracuje-v-jizde-otevira-dalsi-fond/) | [GigaScan Technologies (Göteborg) (17. 9. 2026)](https://cc.cz/brnenska-startupova-ofenziva-miliardar-igor-fait-a-spol-investovali-behem-mesice-pres-150-milionu/) |
| [TCF Capital](https://tcfcap.com) | soukromý investor | [spotřebitelé, e-commerce, průmysl](https://www.newstream.cz/leaders/cupr-investoval-desitky-milionu-do-inovatora-v-oblasti-vzduchotechniky) | [růstová fáze, buyout](https://tcfcap.com/) | [30 mil. EUR – 50 mil. EUR](https://cc.cz/tomas-cupr-spousti-investicni-skupinu-jeji-hodnota-diky-rohliku-prekracuje-17-miliard-a-ma-rychle-rust/) | [720 mil. EUR (hodnota portfolia)](https://www.newstream.cz/leaders/cupr-investoval-desitky-milionu-do-inovatora-v-oblasti-vzduchotechniky) | [Töpfer Babywelt GmbH (DE) (12. 5. 2025)](https://forbes.cz/po-pilulce-a-macromu-jde-o-dalsi-akvizici-cupr-s-tpag-odkoupili-topfer-babywelt-nemeckeho-vyrobce-kojenecke-vyzivy/) |
| [QQ Capital](https://www.qq.capital/) | family office | [B2B software](https://www.qq.capital/) | [seed, série A, série B+, růstová fáze](https://www.qq.capital/) | neuvedeno | neuvedeno | [Navigara (6. 3. 2026)](https://pulse2.com/navigara-2-5-million-raised-for-engineering-performance-measurement-platform/amp/) |
| [Lumus Investment](https://www.lumusinvestment.com/) | andělský syndikát | [bez omezení oboru](https://cc.cz/jak-prilakat-k-investovani-do-startupu-vice-zen-ctyri-slovenky-sdruzuji-uz-250-andelskych-investorek-z-celeho-regionu/) | [pre-seed, seed](https://cc.cz/jak-prilakat-k-investovani-do-startupu-vice-zen-ctyri-slovenky-sdruzuji-uz-250-andelskych-investorek-z-celeho-regionu/) | neuvedeno | neuvedeno | [Kardi AI (28. 4. 2025)](https://tech.eu/2025/04/28/czech-medtech-kardi-ai-raises-1-1m-to-expand-heart-monitoring-tech/) |


---

## Jak jsem postupoval

Nejdřív bylo potřeba úplně a do hloubky analyzovat zadání. Použil jsem k tomu **tři AI agenty**:

- **Agent 1** (Claude Code na Windows) a **agent 2** (Claude Code na Macu) řešili úlohu každý samostatně a vytvořili vlastní řešení.
  **Odevzdané řešení je řešení agenta 1.** Agent 2 sloužil jako nezávislá kontrola: jeho kritika je v [reviews/](reviews/)
  a zjištění jsou zapracovaná (viz „Kde se AI mýlila").
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

Nakonec jsem **ručně zkontroloval dva náhodné vzorky** po 6 investorech (každý údaj proti zdroji). Ve druhém jsem
našel 3 chyby, které AI kontrola přehlédla, a jsou opravené.

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
5. **Člověk:** ruční kontrola dvou náhodných vzorků po 6 investorech.
   - Vzorek 1 (prošel i review agenta 2): 29 z 30 sedí, 0 chyb.
   - Vzorek 2 (bez kontroly navíc): 20 sedí, 2 nesedí, 1 údaj chyběl. **Člověk tu našel 3 chyby, které AI ověřovatel přehlédl.**
   - Proto lidskou kontrolu vzorku nejde při rozšíření vynechat.

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

## Odhad nákladů na rozšíření na celý svět

**Kolik investorů jde z veřejných zdrojů získat:** přibližně **30–50 tisíc** po celém světě, z toho jádro
(VC fondy, private equity, korporátní fondy) 12–16 tisíc. Odhad vychází z veřejných statistik: NVCA, Preqin,
Deloitte, Global Corporate Venturing a EBAN (podrobně v [PLAN.md §5](PLAN.md)).

**Z čeho vychází cena:** z toho, co pilot skutečně spotřeboval.
- Ověřit jednoho kandidáta stojí AI práci za **$0,55–0,95**. Je v tom rešerše, nezávislé ověření a ~8 vyhledávání
  na webu za $10 / 1 000 dotazů podle ceníku Anthropic. U private equity, family office a andělů je to asi 1,6× dráž,
  protože o nich je méně veřejných informací.
- Pravidly projde **zhruba polovina kandidátů**. Na 30–50 tisíc investorů je tedy potřeba prověřit 60–100 tisíc kandidátů.
- Člověk kontroluje **náhodný vzorek a sporné případy**. Všechno lidsky kontrolovat není potřeba, ale vzorek ano:
  na čistém vzorku člověk našel 3 chyby, které AI ověřovatel přehlédl (věcná shoda 86 %).

| položka | jádro (VC, PE, korporátní fondy) | celý rozsah vč. family office a andělů |
|---|---|---|
| počet kandidátů k prověření | ~30 tisíc | ~100 tisíc |
| práce AI + vyhledávání | 15–25 tis. EUR | 49–85 tis. EUR |
| lidská kontrola vzorku a sporných případů | ~9 tis. EUR | ~24 tis. EUR |
| vývoj (fronta úloh, napojení registrů, hlídání chyb) | 10–15 tis. EUR | 10–15 tis. EUR |
| **první naplnění databáze celkem** | **≈ 35–50 tis. EUR** | **≈ 85–125 tis. EUR** |
| průběžná aktualizace (nové fondy, neaktivní investoři) | ≈ 40 % prvního naplnění ročně | |
| doba zpracování (20 agentů souběžně) | ~3 dny | ~10 dní |

**Placené databáze jako alternativa:** celou databázi Apify (~10 tisíc investičních firem) lze koupit za ~$420.
Ušetřila by ale jen hledání kandidátů, ne ověření, protože údaje v ní nemají doložený zdroj. PitchBook nebo Preqin
stojí $12–80 tisíc ročně a jejich data nesmí být zveřejněna. Smysl dávají jen jako levný seznam kandidátů.

**Co cenu sníží nejvíc:**
- začít strojově čitelnými registry (americká SEC, evropský registr ESMA, národní regulátoři jako ČNB),
- levný model na předfiltrování zjevných nesmyslů,
- lidskou kontrolu nasadit jen tam, kde se AI neshodne.

**Rizika odhadu:** v zemích mimo latinku (Čína, Japonsko, Blízký východ) bude přesnost nižší a kontrola dražší.
Některé weby blokují stahování. Andělé jsou fyzické osoby, takže jejich sběr potřebuje právní posouzení (GDPR).
Podrobný výpočet je v [RESULTS.md §5](RESULTS.md).

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

- Ručně je zkontrolováno 12 ze 43 investorů (dva náhodné vzorky). Zbytek ověřila AI, u které ruční kontrola ukázala zhruba 1 přehlédnutou chybu na 10 údajů.
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
