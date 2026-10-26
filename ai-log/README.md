# ai-log

Export konverzace s Claude Code (session menu → Export, ekvivalent příkazu `/export`), převedený na čitelný text
skriptem [src/export_ailog.py](../src/export_ailog.py).

- [konverzace-claude-code.md](konverzace-claude-code.md): celá konverzace (uživatel + Claude), volání nástrojů jako jednořádkový popis
- [agenti/](agenti/): 25 sub-agentů (rešerše, ověřování, slepé ověřování); u každého zadání, použité nástroje a závěrečná zpráva

Vynecháno: systémové připomínky a hooky (soukromé poznámky mimo úkol), obsah stažených stránek a mezikroky agentů,
jedna věta o jiném projektu uživatele. Doslovné pokyny agentům jsou i v [docs/](../docs/).
