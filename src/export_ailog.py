"""Převod exportu konverzace z Claude Code (zip ze session menu → Export) na čitelný text do ai-log/.

Export obsahuje strojový přepis (JSONL) hlavní konverzace a všech sub-agentů včetně technických metadat.
Do repa jde čitelná verze:
  ai-log/konverzace-claude-code.md   zprávy uživatele + odpovědi Clauda; volání nástrojů jako jednořádkový popis
  ai-log/agenti/NN-<popis>.md        pro každého sub-agenta: zadání, které dostal, a jeho závěrečná zpráva

Vynechává se: systémové připomínky a výstupy hooků (obsahují soukromé poznámky uživatele mimo tento úkol),
obsah výsledků nástrojů (stažené stránky, výpisy souborů), mezikroky agentů a interní metadata.

Použití: python src/export_ailog.py <rozbalený-export-dir>
"""
import json
import re
import sys
from pathlib import Path

from records import ROOT

OUT = ROOT / "ai-log"
TAG_BLOCK = re.compile(r"<(system-reminder|task-notification|local-command-\w+|command-\w+)[^>]*>.*?</\1>", re.S)
PASTE = re.compile(r"<pasted_content[^>]*>(.*?)</pasted_content[^>]*>", re.S)


# Věty mimo tento úkol, které se do veřejného repa nehodí (stav jiné aplikace uživatele).
REDACT = [re.compile(r"Mimo tento úkol: v INBOXu je i zpráva o WristRadaru\..*?(?:\n|$)")]


def clean(text: str) -> str:
    text = TAG_BLOCK.sub("", text)
    for pattern in REDACT:
        text = pattern.sub("*[vynecháno: poznámka k jinému projektu]*\n", text)
    text = PASTE.sub(lambda m: "\n> " + m.group(1).strip().replace("\n", "\n> ") + "\n", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def tool_line(block: dict) -> str:
    name, inp = block.get("name", ""), block.get("input") or {}
    short = name.split("__")[-1]
    what = (inp.get("description") or inp.get("file_path") or inp.get("url") or inp.get("query")
            or inp.get("pattern") or "")
    if short == "Agent":
        what = f"{inp.get('description', '')} (sub-agent)"
    return f"- 🔧 `{short}` {str(what)[:150]}".rstrip()


def text_of(content) -> str:
    if isinstance(content, str):
        return content
    return "\n".join(b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text")


def is_handback(text: str) -> bool:
    return "[Subagent hand-back]" in text or "Another Claude session sent a message" in text


def main_conversation(path: Path) -> str:
    out = ["# Konverzace s Claude Code — zadání A „Spolehlivá databáze investorů“\n",
           "Čitelný přepis exportu konverzace (session „Spoľahlivá databáza investorov“, 22.–26. 10. 2026).",
           "Zprávy uživatele a odpovědi Clauda jsou celé. Volání nástrojů jsou zkrácena na jeden řádek",
           "a výsledky nástrojů vynechány. Přepisy sub-agentů jsou ve složce [agenti/](agenti/).\n"]
    pending_tools = []
    for line in open(path, encoding="utf-8"):
        o = json.loads(line)
        if o.get("type") not in ("user", "assistant") or o.get("isSidechain"):
            continue
        msg = o.get("message") or {}
        content = msg.get("content")
        if o["type"] == "user":
            if isinstance(content, list) and any(b.get("type") == "tool_result" for b in content if isinstance(b, dict)):
                continue
            raw = text_of(content)
            if is_handback(raw):
                m = re.search(r"The report follows:\s*(.*?)\s*</agent-message>", raw, re.S)
                report = (m.group(1) if m else "").strip()
                if report:
                    if pending_tools:
                        out.append("\n".join(pending_tools)); pending_tools = []
                    out.append("### 📨 Zpráva sub-agenta\n\n" + "\n".join("> " + l.strip() for l in report.splitlines()))
                continue
            text = clean(raw)
            if not text:
                continue
            if pending_tools:
                out.append("\n".join(pending_tools)); pending_tools = []
            ts = (o.get("timestamp") or "")[:16].replace("T", " ")
            out.append(f"---\n\n## 👤 Uživatel ({ts})\n\n{text}")
        else:
            for b in content if isinstance(content, list) else []:
                if b.get("type") == "text" and b.get("text", "").strip():
                    if pending_tools:
                        out.append("\n".join(pending_tools)); pending_tools = []
                    out.append(f"**🤖 Claude:**\n\n{clean(b['text'])}")
                elif b.get("type") == "tool_use":
                    name = b.get("name", "")
                    if "update_plan" in name or "wrap_up" in name or name == "ToolSearch":
                        continue
                    pending_tools.append(tool_line(b))
    if pending_tools:
        out.append("\n".join(pending_tools))
    return "\n\n".join(out) + "\n"


def subagents(folder: Path) -> list[tuple[str, str]]:
    files = sorted(folder.glob("agent-*.jsonl"), key=lambda p: first_ts(p))
    result = []
    for i, p in enumerate(files, 1):
        meta = {}
        mp = p.with_suffix("").with_suffix(".meta.json")
        if mp.exists():
            meta = json.loads(mp.read_text(encoding="utf-8"))
        prompt, final, tools = "", "", {}
        for line in open(p, encoding="utf-8"):
            o = json.loads(line)
            msg = o.get("message") or {}
            content = msg.get("content")
            if o.get("type") == "user" and not prompt:
                prompt = clean(text_of(content))
            elif o.get("type") == "assistant":
                t = text_of(content).strip()
                if t:
                    final = t
                for b in content if isinstance(content, list) else []:
                    if b.get("type") != "tool_use":
                        continue
                    if b.get("name") == "SubagentHandback":  # závěrečná zpráva se předává tímto nástrojem
                        final = (b.get("input") or {}).get("message") or final
                    else:
                        tools[b.get("name", "")] = tools.get(b.get("name", ""), 0) + 1
        desc = meta.get("description") or meta.get("agentType") or p.stem
        slug = re.sub(r"[^a-z0-9]+", "-", desc.lower()).strip("-")[:50] or p.stem
        activity = ", ".join(f"{name} {n}×" for name, n in sorted(tools.items(), key=lambda kv: -kv[1])
                             if name != "ToolSearch")
        body = (f"# Sub-agent {i:02d}: {desc}\n\nSpuštěn: {first_ts(p)[:16].replace('T', ' ')}  \n"
                f"Použité nástroje: {activity}\n\n"
                f"## Zadání, které agent dostal\n\n{prompt}\n\n## Závěrečná zpráva agenta\n\n{final}\n")
        result.append((f"{i:02d}-{slug}.md", body))
    return result


def first_ts(p: Path) -> str:
    for line in open(p, encoding="utf-8"):
        ts = json.loads(line).get("timestamp")
        if ts:
            return ts
    return ""


def main() -> None:
    src = Path(sys.argv[1])
    transcript = next(p for p in src.rglob("*.jsonl") if "subagents" not in p.parts and p.name != "transcript.jsonl")
    OUT.mkdir(exist_ok=True)
    (OUT / "konverzace-claude-code.md").write_text(main_conversation(transcript), encoding="utf-8")
    agents_dir = OUT / "agenti"
    agents_dir.mkdir(exist_ok=True)
    folder = next(src.rglob("subagents"))
    for name, body in subagents(folder):
        (agents_dir / name).write_text(body, encoding="utf-8")
    print(f"hotovo: {OUT}")


if __name__ == "__main__":
    main()
