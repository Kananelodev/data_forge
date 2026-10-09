# The Rules of the Forge

## The idea in one breath
You're a smith. Raw data is ore. Every fundamental of data engineering is a
technique you have to *prove* you can do before the game believes you. Prove
enough, and you rise from **Cinder** to **Irreplaceable**.

## How a quest gets forged
A quest is complete only when **both** halves are done:

| Half | Where | What counts |
|---|---|---|
| 🛠️ **Gate** | `gates/test_qXX_*.py` | Every test in the file passes against your code in `solutions/qXX_*.py` |
| 📝 **Journal** | `journal/qXX.md` | A real entry in your own words (template line removed, enough substance to be honest) |

Only one half done? The quest shows as 🔨 half-done. That's deliberate — passing
tests without being able to explain them is exactly the gap interviewers find.

## What happens when you push
GitHub Actions runs `python -m forge.update`, which:
1. **Strikes the gates** — runs every gate test.
2. **Referees** — works out which quests are forged, your XP and rank.
3. **Announces** — compares with your last save and writes events
   (quest forged, region unlocked, rank up, streak).
4. **Redraws** — rewrites the board in `README.md` and the map in
   `assets/forge_map.svg`, then commits them back with the headline event as the
   commit message.

So your repo's front page *is* the game. Push a win and watch the map light up.

Run it locally any time with `make play` — same engine, no push needed.

## Ranks
| XP | Rank | |
|---|---|---|
| 0 | Cinder | the forge is cold |
| 150 | Striker | you can keep a fire lit |
| 400 | Journeyman Smith | the basics bend to your hammer |
| 900 | Bladesmith | you shape data that holds an edge |
| 1700 | Master Smith | production-ready pipelines |
| 2600 | Forgemaster | you teach the fire what to do |
| 3500 | **Irreplaceable** | every quest forged |

## Streak & forge heat
Your journal `date:` lines build a streak of consecutive days. The longer the
streak, the hotter the forge (up to 5 🔥) and the bigger the glow on the map.
Miss a day and it cools — it never resets your XP, just the heat.

## Regions
The seven regions follow the real data-engineering lifecycle:
**Foundry Floor** (storage) → **Query Crucible** (SQL) → **Ore Mines** (ingestion)
→ **Shaping Anvil** (modelling) → **Long Furnace** (reliable pipelines)
→ **Passport Office** (governance & POPIA) → **Cloud Citadel** (AWS).

Quests marked ⚒️ are on the map but their gate isn't forged yet. We forge each
gate together in a mentor session when you reach it — designing the test *after*
you understand the concept is part of the learning.

## House rules
- **No copy-paste solutions.** Look things up; type it yourself.
- **Never edit a gate to make it pass.** Gates are the referee. If you think a
  gate is wrong, raise it in a mentor session and argue your case — that's a
  great exercise in itself.
- **The engine (`forge/`) isn't part of the challenge,** but reading it is good
  Python practice.
