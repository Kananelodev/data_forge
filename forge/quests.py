"""Load and validate the quest map from quests/quests.yml."""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
QUESTS_FILE = ROOT / "quests" / "quests.yml"


def load(path: Path | None = None) -> dict:
    """Parse quests.yml into {'regions': [...], 'quests': [...]}.

    Each quest gets sensible defaults so later ones can be listed before their
    gate exists ('forthcoming' quests).
    """
    doc = yaml.safe_load((path or QUESTS_FILE).read_text()) or {}
    doc.setdefault("regions", [])
    doc.setdefault("quests", [])
    for q in doc["quests"]:
        q.setdefault("requires", [])
        q.setdefault("gate", None)      # path like "gates/test_q01_storage.py", or None
        q.setdefault("xp", 100)
        q.setdefault("maps_to", None)
    # index helpers
    doc["_region_order"] = {r["id"]: r.get("order", i) for i, r in enumerate(doc["regions"])}
    doc["_quest_by_id"] = {q["id"]: q for q in doc["quests"]}
    return doc
