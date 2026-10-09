"""The game engine: turn raw facts (which gates passed, which journals exist)
into game state (XP, rank, unlocked regions, events).

Plain idea: this is the referee. It looks at what you've actually done and
decides what you've earned — it never just takes your word for it.
"""
from __future__ import annotations

import json
import re
from datetime import date, timedelta
from pathlib import Path
from xml.etree import ElementTree as ET

from . import ranks

ROOT = Path(__file__).resolve().parents[1]
JOURNAL_DIR = ROOT / "journal"
STATE_FILE = ROOT / "state" / "progress.json"

# A journal entry counts as "real reflection" only if it has this much substance
# beyond the template. You can't earn a quest by leaving the template untouched.
_MIN_JOURNAL_CHARS = 220
_TEMPLATE_MARKER = "⟶ replace this"


# ---------------------------------------------------------------------------
# Inputs: what actually happened
# ---------------------------------------------------------------------------
def gate_results_from_junit(xml_path: Path) -> dict[str, bool]:
    """Parse a pytest junit XML into {gate_file_path: passed?}.

    A gate 'passed' means: it had at least one real (non-skipped) test and none
    of its tests failed or errored. Returns {} if the file is missing.
    """
    if not Path(xml_path).exists():
        return {}
    tree = ET.parse(xml_path)
    by_file: dict[str, dict] = {}
    for case in tree.iter("testcase"):
        f = case.get("file") or case.get("classname", "")
        rec = by_file.setdefault(f, {"ran": 0, "bad": 0})
        skipped = any(c.tag == "skipped" for c in case)
        failed = any(c.tag in ("failure", "error") for c in case)
        if not skipped:
            rec["ran"] += 1
        if failed:
            rec["bad"] += 1
    return {f: (r["ran"] > 0 and r["bad"] == 0) for f, r in by_file.items()}


def _journal_dates() -> list[date]:
    """Dates pulled from `date: YYYY-MM-DD` lines in journal entries."""
    out: list[date] = []
    for p in JOURNAL_DIR.glob("q*.md"):
        m = re.search(r"date:\s*(\d{4})-(\d{2})-(\d{2})", p.read_text())
        if m:
            out.append(date(int(m[1]), int(m[2]), int(m[3])))
    return sorted(set(out))


def _has_reflection(qid: str) -> bool:
    p = JOURNAL_DIR / f"{qid}.md"
    if not p.exists():
        return False
    text = p.read_text()
    if _TEMPLATE_MARKER in text:
        return False
    body = re.sub(r"\s+", " ", text).strip()
    return len(body) >= _MIN_JOURNAL_CHARS


def _streak(dates: list[date]) -> int:
    """Run of consecutive calendar days ending at the most recent active date."""
    if not dates:
        return 0
    run = 1
    for later, earlier in zip(reversed(dates), reversed(dates[:-1])):
        if (later - earlier) == timedelta(days=1):
            run += 1
        else:
            break
    return run


# ---------------------------------------------------------------------------
# The computation
# ---------------------------------------------------------------------------
def compute_state(doc: dict, gate_passed: dict[str, bool]) -> dict:
    """Produce the full game state from the quest map + gate results + journals."""
    quests = doc["quests"]
    by_id = doc["_quest_by_id"]

    complete: dict[str, bool] = {}
    gate_ok: dict[str, bool] = {}
    reflected: dict[str, bool] = {}
    for q in quests:
        qid = q["id"]
        gate = q.get("gate")
        if gate is None:
            g = True                                   # reflection-only quest
        elif not (ROOT / gate).exists():
            g = False                                  # gate not forged yet
        else:
            g = gate_passed.get(gate, False)
        r = _has_reflection(qid)
        gate_ok[qid] = g
        reflected[qid] = r
        complete[qid] = g and r

    def available(q) -> bool:
        return all(complete.get(dep, False) for dep in q.get("requires", []))

    # quest view
    quest_view = []
    for q in quests:
        qid = q["id"]
        gate_forged = q.get("gate") is None or (ROOT / q["gate"]).exists()
        if complete[qid]:
            status = "complete"
        elif not gate_forged:
            status = "forthcoming"                     # on the map, not yet playable
        elif not available(q):
            status = "locked"
        elif gate_ok[qid] or reflected[qid]:
            status = "in_progress"                     # one half done
        else:
            status = "available"
        quest_view.append({
            "id": qid, "title": q["title"], "region": q["region"],
            "xp": q["xp"], "teaches": q.get("teaches", ""),
            "maps_to": q.get("maps_to"), "status": status,
            "gate_ok": gate_ok[qid], "reflected": reflected[qid],
        })

    xp = sum(q["xp"] for q in quests if complete[q["id"]])
    rank = ranks.rank_for(xp)

    # region view
    regions = []
    for region in sorted(doc["regions"], key=lambda r: r.get("order", 0)):
        rid = region["id"]
        rqs = [qv for qv in quest_view if qv["region"] == rid]
        done = sum(1 for qv in rqs if qv["status"] == "complete")
        unlocked = any(qv["status"] in ("available", "in_progress", "complete") for qv in rqs)
        regions.append({
            "id": rid, "name": region["name"], "order": region.get("order", 0),
            "blurb": region.get("blurb", ""), "total": len(rqs), "done": done,
            "state": "cleared" if (rqs and done == len(rqs)) else ("active" if unlocked else "locked"),
        })

    dates = _journal_dates()
    streak = _streak(dates)

    return {
        "xp": xp,
        "rank": rank,
        "regions": regions,
        "quests": quest_view,
        "counts": {
            "complete": sum(complete.values()),
            "total": len(quests),
            "playable": sum(1 for qv in quest_view if qv["status"] != "forthcoming"),
        },
        "streak": streak,
        "heat": min(5, streak),
        "days_active": len(dates),
        "generated_for": date.today().isoformat(),
    }


# ---------------------------------------------------------------------------
# Events: what changed since last push (this is what makes a push feel alive)
# ---------------------------------------------------------------------------
def load_prev() -> dict | None:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except json.JSONDecodeError:
            return None
    return None


def diff_events(prev: dict | None, cur: dict) -> list[str]:
    events: list[str] = []
    if prev is None:
        events.append("🔥 The forge is lit for the first time. Your journey begins.")
        return events

    prev_done = {q["id"] for q in prev.get("quests", []) if q["status"] == "complete"}
    cur_done = {q["id"] for q in cur["quests"] if q["status"] == "complete"}
    for qid in sorted(cur_done - prev_done):
        q = next(q for q in cur["quests"] if q["id"] == qid)
        events.append(f"✅ Quest forged: **{q['title']}** (+{q['xp']} XP)")

    prev_regions_cleared = {r["id"] for r in prev.get("regions", []) if r["state"] == "cleared"}
    cur_regions_active = {r["id"] for r in cur["regions"] if r["state"] in ("active", "cleared")}
    prev_regions_active = {r["id"] for r in prev.get("regions", []) if r["state"] in ("active", "cleared")}
    for rid in cur_regions_active - prev_regions_active:
        r = next(r for r in cur["regions"] if r["id"] == rid)
        events.append(f"🗺️ New region unlocked: **{r['name']}**")
    for r in cur["regions"]:
        if r["state"] == "cleared" and r["id"] not in prev_regions_cleared:
            events.append(f"🏆 Region cleared: **{r['name']}**")

    if cur["rank"]["index"] > prev.get("rank", {}).get("index", 0):
        events.append(f"⚒️  RANK UP → **{cur['rank']['name']}** — {cur['rank']['flavour']}")

    if cur["streak"] >= 3 and cur["streak"] > prev.get("streak", 0):
        events.append(f"🔥 {cur['streak']}-day streak! The forge runs hot.")

    if not events:
        events.append("🔨 Progress committed. The fire holds steady — keep striking.")
    return events


def save_state(cur: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(cur, indent=2))
