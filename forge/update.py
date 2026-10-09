"""One turn of the game. Run on every push (and locally via `make play`).

  1. strike the gates   -> run pytest over gates/, record results
  2. referee            -> compute XP / rank / regions from results + journals
  3. announce           -> diff against the last save to produce events
  4. render             -> rewrite the README board + forge map SVG
  5. save               -> write state/progress.json (the save file)
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from . import engine, quests, render

ROOT = Path(__file__).resolve().parents[1]
JUNIT = ROOT / "state" / "gates.xml"


def strike_gates() -> None:
    JUNIT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [sys.executable, "-m", "pytest", "gates", "-q", "-p", "no:cacheprovider",
         f"--junitxml={JUNIT}", "-o", "junit_family=xunit1"],
        cwd=ROOT, check=False,
    )


def main() -> None:
    print("⚒️  Striking the gates...\n")
    strike_gates()

    doc = quests.load()
    gate_passed = engine.gate_results_from_junit(JUNIT)
    cur = engine.compute_state(doc, gate_passed)
    prev = engine.load_prev()
    events = engine.diff_events(prev, cur)

    render.write_readme(cur, events)
    render.write_svg(cur)
    engine.save_state(cur)

    r = cur["rank"]
    print("\n" + "=" * 60)
    print(f"  RANK   {r['name']}  ({cur['xp']} XP)")
    print(f"  QUESTS {cur['counts']['complete']}/{cur['counts']['total']}   STREAK {cur['streak']}d")
    print("=" * 60)
    for e in events:
        print("  " + e.replace("**", ""))
    print()

    # Hand events to the GitHub Action (commit message + job summary)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a") as fh:
            fh.write(f"## ⚒️ {r['name']} — {cur['xp']} XP\n\n")
            fh.writelines(f"- {e}\n" for e in events)
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        headline = events[0].replace("**", "")[:70]
        with open(out, "a") as fh:
            fh.write(f"headline={headline}\n")


if __name__ == "__main__":
    main()
