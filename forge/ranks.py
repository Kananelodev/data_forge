"""Rank progression — the smith's path.

Plain idea: the more quests you complete, the more XP you earn, and XP moves you
up a ladder of ranks. (Jargon: this is just a lookup table mapping a running
score to a tier label.)
"""
from __future__ import annotations

# (xp_floor, name, flavour). Keep ascending by xp_floor.
RANKS: list[tuple[int, str, str]] = [
    (0,    "Cinder",            "the forge is cold — strike the first spark"),
    (150,  "Striker",           "you can keep a fire lit"),
    (400,  "Journeyman Smith",  "the basics bend to your hammer"),
    (900,  "Bladesmith",        "you shape data that holds an edge"),
    (1700, "Master Smith",      "pipelines leave your forge production-ready"),
    (2600, "Forgemaster",       "you teach the fire what to do"),
    (3500, "Irreplaceable",     "every quest forged — judgment, not just tools"),
]


def rank_for(xp: int) -> dict:
    """Return the rank dict for a given XP total, with progress to the next rank."""
    current = RANKS[0]
    for floor, name, flavour in RANKS:
        if xp >= floor:
            current = (floor, name, flavour)
        else:
            break
    idx = [r[1] for r in RANKS].index(current[1])
    floor, name, flavour = current
    nxt = RANKS[idx + 1] if idx + 1 < len(RANKS) else None
    if nxt:
        span = nxt[0] - floor
        into = xp - floor
        pct = int(round(100 * into / span)) if span else 100
        to_next = nxt[0] - xp
    else:
        pct, to_next = 100, 0
    return {
        "index": idx,
        "name": name,
        "flavour": flavour,
        "floor": floor,
        "next_name": nxt[1] if nxt else None,
        "next_floor": nxt[0] if nxt else None,
        "pct_to_next": pct,
        "xp_to_next": to_next,
        "is_max": nxt is None,
    }
