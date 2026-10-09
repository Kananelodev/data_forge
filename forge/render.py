"""Render game state into things you can SEE on GitHub:
  - the live board inside README.md (between the FORGE markers)
  - assets/forge_map.svg (the map that lights up as you progress)
"""
from __future__ import annotations

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
SVG_OUT = ROOT / "assets" / "forge_map.svg"

START, END = "<!-- FORGE:START -->", "<!-- FORGE:END -->"

STATUS_ICON = {
    "complete": "✅", "in_progress": "🔨", "available": "🟠",
    "locked": "🔒", "forthcoming": "⚒️",
}
REGION_ICON = {"cleared": "🏆", "active": "🔥", "locked": "🔒"}

FLAMES = [
    "   (cold)   ",
    "     .      ",
    "    (.)     ",
    "   ( ) )    ",
    "  ( (()) )  ",
    " ((( )() )) ",
]


def _bar(pct: int, width: int = 24) -> str:
    filled = round(width * pct / 100)
    return "█" * filled + "░" * (width - filled)


# ---------------------------------------------------------------------------
# README board
# ---------------------------------------------------------------------------
def render_board(state: dict, events: list[str]) -> str:
    r = state["rank"]
    lines: list[str] = []
    lines.append('<p align="center"><img src="assets/forge_map.svg" alt="Forge map" width="100%"/></p>')
    lines.append("")
    lines.append(f"### ⚒️ Rank: **{r['name']}** — _{r['flavour']}_")
    lines.append("")
    if r["is_max"]:
        lines.append(f"`{_bar(100)}` **{state['xp']} XP** — max rank reached")
    else:
        lines.append(f"`{_bar(r['pct_to_next'])}` **{state['xp']} XP** · "
                     f"{r['xp_to_next']} XP to **{r['next_name']}**")
    lines.append("")
    c = state["counts"]
    lines.append(f"**Quests:** {c['complete']}/{c['total']} forged · "
                 f"**Streak:** {state['streak']} day(s) · "
                 f"**Days at the anvil:** {state['days_active']} · "
                 f"**Forge heat:** {'🔥' * state['heat'] or '❄️'}")
    lines.append("")
    lines.append("#### 📣 Last push")
    for e in events:
        lines.append(f"- {e}")
    lines.append("")

    nxt = [q for q in state["quests"] if q["status"] in ("in_progress", "available")]
    lines.append("#### 🎯 Next on the anvil")
    if nxt:
        for q in nxt[:3]:
            half = ""
            if q["status"] == "in_progress":
                half = " — gate ✔ / journal ✘" if q["gate_ok"] else " — journal ✔ / gate ✘"
            lines.append(f"- {STATUS_ICON[q['status']]} **{q['id']} · {q['title']}** "
                         f"(+{q['xp']} XP){half}")
    else:
        lines.append("- Nothing playable right now — time for a mentor session to forge the next gate.")
    lines.append("")

    lines.append("#### 🗺️ The map")
    lines.append("")
    lines.append("| Region | State | Quests |")
    lines.append("|---|---|---|")
    for reg in state["regions"]:
        lines.append(f"| {reg['name']} | {REGION_ICON[reg['state']]} {reg['state']} | "
                     f"{reg['done']}/{reg['total']} |")
    lines.append("")

    lines.append("<details><summary>📜 Full quest log</summary>")
    lines.append("")
    lines.append("| | Quest | Region | XP | Teaches |")
    lines.append("|---|---|---|---|---|")
    region_name = {reg["id"]: reg["name"] for reg in state["regions"]}
    for q in state["quests"]:
        lines.append(f"| {STATUS_ICON[q['status']]} | **{q['id']}** {q['title']} | "
                     f"{region_name.get(q['region'], q['region'])} | {q['xp']} | {q['teaches']} |")
    lines.append("")
    lines.append("Legend: ✅ forged · 🔨 half-done · 🟠 available · 🔒 locked · ⚒️ gate not forged yet")
    lines.append("</details>")
    lines.append("")
    lines.append(f"<sub>Board regenerated automatically on push · {state['generated_for']}</sub>")
    return "\n".join(lines)


def write_readme(state: dict, events: list[str]) -> None:
    text = README.read_text()
    if START not in text or END not in text:
        raise SystemExit("README.md is missing the FORGE:START / FORGE:END markers.")
    head, rest = text.split(START, 1)
    _, tail = rest.split(END, 1)
    README.write_text(f"{head}{START}\n{render_board(state, events)}\n{END}{tail}")


# ---------------------------------------------------------------------------
# SVG forge map
# ---------------------------------------------------------------------------
_COL = {
    "bg": "#14110f", "panel": "#1f1a17", "text": "#f3e9dc", "muted": "#8a7f74",
    "locked": "#3a332e", "active": "#ff8c2a", "cleared": "#ffd166", "line": "#4a403a",
    "bar_bg": "#2b2420", "bar": "#ff8c2a",
}


def render_svg(state: dict) -> str:
    W, H = 960, 330
    regions = state["regions"]
    n = max(1, len(regions))
    x0, x1, y = 90, W - 90, 210
    step = (x1 - x0) / max(1, n - 1)

    parts: list[str] = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
                 f'font-family="ui-monospace, SFMono-Regular, Menlo, monospace">')
    parts.append(f'<rect width="{W}" height="{H}" rx="18" fill="{_COL["bg"]}"/>')
    parts.append("""<defs>
  <radialGradient id="glow" cx="50%" cy="50%" r="50%">
    <stop offset="0%" stop-color="#ffb347" stop-opacity="0.9"/>
    <stop offset="100%" stop-color="#ff5e00" stop-opacity="0"/>
  </radialGradient>
</defs>""")

    # title + rank
    r = state["rank"]
    parts.append(f'<text x="40" y="58" fill="{_COL["active"]}" font-size="30" font-weight="700" '
                 f'letter-spacing="6">DATA FORGE</text>')
    parts.append(f'<text x="40" y="86" fill="{_COL["muted"]}" font-size="14">'
                 f'Kananelo Mofokeng · data engineering, forged by hand</text>')
    parts.append(f'<text x="{W-40}" y="52" text-anchor="end" fill="{_COL["text"]}" font-size="20" '
                 f'font-weight="700">{escape(r["name"])}</text>')
    parts.append(f'<text x="{W-40}" y="74" text-anchor="end" fill="{_COL["muted"]}" font-size="13">'
                 f'{state["xp"]} XP · {state["counts"]["complete"]}/{state["counts"]["total"]} quests</text>')

    # xp bar
    bx, bw, by = W - 300, 260, 88
    pct = 100 if r["is_max"] else r["pct_to_next"]
    parts.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="10" rx="5" fill="{_COL["bar_bg"]}"/>')
    parts.append(f'<rect x="{bx}" y="{by}" width="{bw*pct/100:.1f}" height="10" rx="5" fill="{_COL["bar"]}">'
                 f'<animate attributeName="opacity" values="0.75;1;0.75" dur="2.4s" repeatCount="indefinite"/></rect>')
    label = "MAX RANK" if r["is_max"] else f'{r["xp_to_next"]} XP → {escape(r["next_name"])}'
    parts.append(f'<text x="{bx+bw}" y="{by+26}" text-anchor="end" fill="{_COL["muted"]}" font-size="11">{label}</text>')

    # path
    parts.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{_COL["line"]}" '
                 f'stroke-width="4" stroke-dasharray="2 10" stroke-linecap="round"/>')

    # find frontier (first non-cleared active region) for the flame
    frontier = next((i for i, reg in enumerate(regions) if reg["state"] == "active"), None)

    for i, reg in enumerate(regions):
        cx = x0 + i * step
        st = reg["state"]
        fill = {"locked": _COL["locked"], "active": _COL["active"], "cleared": _COL["cleared"]}[st]
        if i == frontier and state["heat"] > 0:
            rad = 34 + 6 * state["heat"]
            parts.append(f'<circle cx="{cx:.1f}" cy="{y}" r="{rad}" fill="url(#glow)">'
                         f'<animate attributeName="r" values="{rad-6};{rad+4};{rad-6}" dur="1.8s" '
                         f'repeatCount="indefinite"/></circle>')
        parts.append(f'<circle cx="{cx:.1f}" cy="{y}" r="26" fill="{_COL["panel"]}" stroke="{fill}" stroke-width="4"/>')
        glyph = {"locked": "◌", "active": "▲", "cleared": "★"}[st]
        parts.append(f'<text x="{cx:.1f}" y="{y+7}" text-anchor="middle" font-size="20" '
                     f'fill="{fill}">{glyph}</text>')
        tcol = _COL["text"] if st != "locked" else _COL["muted"]
        parts.append(f'<text x="{cx:.1f}" y="{y+52}" text-anchor="middle" font-size="12" '
                     f'fill="{tcol}" font-weight="600">{escape(reg["name"])}</text>')
        parts.append(f'<text x="{cx:.1f}" y="{y+70}" text-anchor="middle" font-size="11" '
                     f'fill="{_COL["muted"]}">{reg["done"]}/{reg["total"]}</text>')

    # heat meter
    heat = state["heat"]
    parts.append(f'<text x="40" y="{H-26}" fill="{_COL["muted"]}" font-size="12">forge heat</text>')
    for k in range(5):
        on = k < heat
        parts.append(f'<rect x="{120 + k*18}" y="{H-37}" width="12" height="12" rx="3" '
                     f'fill="{_COL["active"] if on else _COL["locked"]}"/>')
    parts.append(f'<text x="{W-40}" y="{H-26}" text-anchor="end" fill="{_COL["muted"]}" font-size="12">'
                 f'streak {state["streak"]}d · {state["days_active"]} days at the anvil</text>')

    parts.append("</svg>")
    return "\n".join(parts)


def write_svg(state: dict) -> None:
    SVG_OUT.parent.mkdir(parents=True, exist_ok=True)
    SVG_OUT.write_text(render_svg(state))
