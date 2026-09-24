# Project Management

Evidence of the process behind Pac-Man (42 project *Pacman v1.5*), team of two.

---

## 1. Team organization

| | Developer A (``) | Developer B (``) |
|---|---|---|
| Scope | engine: config, maze adapter, movement, ghost AI, game rules, tests | presentation: window, rendering, scenes, HUD, highscore screen |
| Commits | 101 | 48 (+1 merge PR) |
| Main files | `game.py` (40), `shared_types.py` (13), `core/world.py` (11), `core/ghosts.py` (10), `core/player.py` (8), `parsing.py` (7) | `visuals/visualiser.py` (20), `entity_view.py` (13), `event_handler.py` (10), `maze_view.py` (9), `victory_view.py` (8) |
| Branch | `lolkek` | `yaro` |

Shared: `src/main.py` (12 / 11 commits) and `src/shared_types.py`, the contract file.
The config parser was started by B on 09-11 and later maintained by A.

**Integration.** Personal branches merge into `testall` / `test`, then into `main`.
Merges were done manually and once through a pull request (`Merge pull request #2`).

**How decisions were made.** Anything crossing the boundary (type names, snapshot
fields, who triggers level transitions) was agreed before implementation and recorded in
`src/shared_types.py`. Disagreements were settled by measurement rather than opinion —
see the greedy-vs-BFS experiment in §3.

**How issues were handled.** Each defect was reproduced with a scripted scenario outside
the game window, fixed, then re-checked with the same script; the scripts became the test
cases listed in §5.

**Use of AI.** An AI assistant (Claude Code) was used for review and explanation:
exploring the third-party maze package, reasoning about algorithms, hunting bugs by
running scenario scripts against a reference implementation, and drafting this document.
Game code was written by the developers; the assistant committed no source code.

---

## 2. Timeline and progress tracking

| Sprint | Dates | Commits | Goal | Result |
|---|---|---|---|---|
| 0. Foundation | 09-08 | 1 | repository, skeleton | ✅ |
| 1. Config & maze | 09-11 → 09-12 | 14 | JSON-with-comments parser, A-Maze-ing adapter | ✅ |
| 2. Vertical slice | 09-13 → 09-16 | 33 | tile movement, ghost skeleton, `Game`, first window | ✅ |
| 3. Full level | 09-17 → 09-19 | 64 | 4 ghosts, pacgums, scoring, level progression | ✅ |
| 4. Meta-game | 09-21 → 09-23 | 38 | lives, pause, countdown, cheats, highscores, difficulty | ✅ |
| 5. Packaging | — | 0 | PyInstaller, itch.io | ✅ |
| 6. Docs & defense | 09-23 | — | README, project management | ✅ |

No commits on 09-09, 09-10, 09-20. Busiest day: 09-17 with 42 commits.

```
              08 11 12 13 14 15 16 17 18 19 21 22 23
Parser         .  ## #  .  .  .  .  .  .  .  .  #  .
Maze adapter   .  .  ## .  .  .  .  .  .  .  .  .  .
Player         .  .  #  ## .  .  .  .  .  .  .  .  .
Ghosts         .  .  .  .  #  #  ## ## .  .  #  .  .
Game rules     .  .  .  .  #  ## #  ## ## #  ## ## #
Rendering      .  .  .  .  #  ## #  ## ## .  #  #  .
Highscores     .  .  .  .  .  .  .  .  .  .  .  ## ##
Tests          .  .  .  #  .  .  .  #  ## #  #  ## ##
```

**Plan vs actual.** Sprints 1–3 matched the estimate; the parser landed a day early and
the adapter a day late. Sprint 4 took three days instead of two. The planned robustness
phase is only partly done, and packaging has not started — the two items that put the
deadline at risk (§4).

---

## 3. Analysis and key choices

**Tile grid `(2W+1)×(2H+1)`.** The package returns `W×H` cells with wall bitmasks.
The adapter expands each cell into a floor tile at `(2x+1, 2y+1)`, opening the shared
tile between two cells when the wall bit is clear. Neighbouring cells share one wall
tile. Collision checks then reduce to `grid[row][col] == "wall"`. Rejected: keeping the
bitmask grid, which would force bit logic into movement, path-finding and rendering.

**`Pos = (col, row)` with `grid[row][col]`.** Positions match pygame's `(x, y)`; the grid
stays a list of rows. This seam caused three separate bugs, so `tile_at(grid, pos)`
centralises the conversion and every related test uses a **non-square** maze, where a
swapped pair is immediately visible.

**One file touches the third-party package.** `core/maze_adapter.py` normalises the seed,
validates the returned structure (list of lists, expected size, values 0–15) and raises
`MazeError` otherwise. This was justified: the package README documents
`MazeGenerator(width=…, height=…)` while the real signature is `size=(w, h)`,
`seed=None` raises `TypeError`, and generation reseeds the **global** `random` module —
so ghosts use a private `random.Random()` instance.

**Time-based movement.** Entities keep the tile they left plus `progress ∈ [0, 1)`;
speed is tiles per second, every step is `progress += speed * dt`, and direction changes
only at tile centres with a buffered intent. `while progress >= 1` prevents a long frame
from teleporting anyone through a wall. Verified against a reference implementation over
75 000 simulated frames with zero divergence.

**Ghost path-finding: BFS, decided by measurement.** The arcade original picks the
neighbour minimising straight-line distance. Over 8 mazes × 60 random start/target pairs:

| Strategy | Reached target |
|---|---|
| Greedy (Manhattan distance) | 305 / 480 |
| BFS carrying the first step | **480 / 480** |

Greedy ghosts looped around the same four tiles when a wall separated them from pacman,
so a player could stand still and never be caught. BFS costs ~25 lines and runs only at
tile centres (~3 decisions per ghost per second).

**Ghost personalities differ in one method.** `Ghost` is abstract with a single abstract
method `chase_target`: Blinky targets pacman, Pinky 8 tiles ahead, Inky 8 tiles behind,
Clyde chases while far and retreats when close. Measured over 90 seconds of play the four
ghosts share only 6–26 % of visited tiles.

**Immutable snapshot between engine and renderer.** `Game.snapshot()` returns a frozen
dataclass with copied sets. Needed in practice: a countdown *view* was assigning
`game.status = "playing"` every frame, resurrecting the game from `dead`. Views now call
`end_countdown()`, which acts only when the status still is `countdown`.

**UI drives transitions.** The engine sets terminal statuses (`level_won`, `dead`,
`game_over`, `victory`); the UI plays its animation and calls `next_level()`,
`respawn()` or `end_countdown()`, each validating the current status first. Animation
durations are a presentation concern, so internal engine timers were rejected.

**Cheats are reversible toggles**, so a reviewer can enable invincibility, walk through
the levels, then disable it and test dying. **Highscores** are a plain JSON list of
`{nickname, score}`; saving appends, sorts descending and truncates to ten, which removes
the special cases a "better than the last one?" comparison kept getting wrong.
**Difficulty** (1–3) maps to `{0.5, 0.7, 0.9}` and multiplies ghost speed.
**Running out of time** ends the game rather than costing a life — this must be stated in
the root README.

---

## 4. Risk analysis

| Risk | Mitigation | Did it happen? |
|---|---|---|
| Third-party maze package is undocumented or its API differs | all contact in one adapter file, output validated, `MazeError` on failure | **Yes** — README signature wrong, `seed=None` crashes, global `random` reseeded |
| Reviewer edits the config during the defense | validation table with clamping and messages, no traceback | Partly — parser hardened, broken-config matrix not finished |
| Two work streams diverge and conflict | contract file agreed first, integration branch, frequent merges | **Yes** — heavy merge traffic on 09-17; resolved the same day |
| Boundary between logic and rendering erodes | engine exposes only a frozen snapshot | **Yes** — a view wrote into `game.status`; fixed with explicit methods |
| Ghost AI feels broken (stuck or instantly lethal) | measure before choosing; four distinct targets; speed via difficulty | **Yes** — greedy version got stuck, replaced with BFS |
| Coordinate convention confusion | single helper for grid access, non-square mazes in tests | **Yes** — three bugs, all caught by non-square tests |
| Packaging and itch.io left to the end | planned as its own phase | **Open risk** — not started, biggest remaining threat |
| Documentation written the night before | this folder maintained during the work | Partly — started 09-23 |
| One developer cannot explain the other's code | reviews, shared contract file, no unreviewed code | No |

---

## 5. Acceptance test plan

Automated tests live in `tests/` (pytest). Scenario scripts were used for behaviour that
needs many frames: chases on real mazes, collision timing, transitions between statuses.

| Feature | How it is tested | Status |
|---|---|---|
| Config: missing key, wrong type, out of range, unknown keys | unit tests + manual matrix of broken configs | ✅ |
| Config: not JSON, not UTF-8, directory instead of file | manual matrix | ✅ |
| Maze adapter: reproducible seed 42, size, borders, connectivity | scenario script over 72 mazes | ✅ |
| Adapter: generator failure, malformed output | unit-level checks with a stubbed package | ✅ |
| Pacman: walls, buffered turns, reversal, long frames | unit tests + 75 000-frame comparison | ✅ |
| Ghosts: path choice, dead ends, frightened, eaten, respawn | scenario scripts on 8 mazes | ✅ |
| Scoring: pacgum, super-pacgum, ghost | manual run + code review | ✅ |
| Lives, death, game over | scenario script | ✅ |
| Level progression and victory | scenario script | ✅ |
| Cheats: each toggles on and off | scenario script | ✅ |
| Pause | test present | ✅ |
| Full loop: menu → game → death → restart | manual play |  ✅  |

### Bugs found and fixed (selection)

| # | Defect | How it was found | Status |
|---|---|---|---|
| 1 | Non-UTF-8 config raised a traceback | broken-config matrix | fixed |
| 2 | Non-string `highscore_filename` raised `ValidationError` | broken-config matrix | fixed |
| 3 | Extra `generate()` call re-randomised the seeded maze — level 1 not reproducible | adapter scenario script | fixed |
| 4 | `seed=None` crashed inside the package | adapter scenario script | fixed |
| 5 | Start tile computed as `(row, col)` — pacman spawned inside a wall; `IndexError` on non-square mazes | non-square maze test | fixed |
| 6 | Pacgum placement transposed — 200 of 493 pacgums outside the grid | placement script | fixed |
| 7 | Pacman teleported one tile on start; reversal used `progress - 1` instead of `1 - progress` | reference comparison | fixed |
| 8 | Greedy ghosts circled forever (175 of 480 chases failed) | 480-chase measurement | fixed (BFS) |
| 9 | BFS bugs: inner loop nested in the candidate loop, one direction checked, wrong neighbour, `while queue` on the imported module | fork-in-the-maze test | fixed |
| 10 | `eaten` ghosts never returned to `chase`; timers compared with `== 0` | timer scenario | fixed |
| 11 | Circular import `world ↔ ghosts` — the project did not import at all | `import game` | fixed |
| 12 | Pacgum sets swapped on unpacking — 620 dots drawn with the animated super-gum sprite | visual flicker report | fixed |
| 13 | `game.update` called twice per frame + a view writing `status = "playing"` — two lives lost per collision | frame-by-frame trace | fixed |
| 14 | Pacgum and super-pacgum point values swapped | score check | fixed |
| 15 | Ghost speed 1 on level 1 but 8 on level 2 | speed comparison across levels | fixed |
| 16 | After switching cheats from list to dict, `"key" not in dict` was always false — pacman immortal, timer frozen | no-cheat baseline run | fixed |
| 17 | Highscore reader fed dicts to `model_validate_json` — table always empty; ascending sort kept the ten worst | highscore scenarios | fixed |
| 18 | `save` crashed with `IndexError` on an empty table | highscore scenarios | fixed |
| 19 | Highscore read/write have no `try/except`; missing or corrupt file crashes | highscore scenarios | **open** |
| 20 | Score is saved on victory only, not on game over | code review | **open** |

---

## 6. Blocking points and disagreements

**Circular import (09-19).** Factory helpers creating ghosts and the player were added to
`core/world.py`, which `core/ghosts.py` already imported. Nothing imported any more, and
the whole test suite failed to collect. Resolved by moving the factories to `game.py`,
keeping `world.py` a low-level module that knows nothing about entities.

**Branch divergence (09-17).** Both developers had been merging into different
integration branches; `main` stayed at the initial commit while three branches carried
different versions of `main.py`, `parsing.py` and `shared_types.py`. Resolved with a
merge day and an agreement to integrate every two days. `main` still needs the final
merge.

**Ownership of state transitions.** Disagreement over whether the engine should run its
own timers for death and level change, or expose statuses and let the UI drive. Resolved
in favour of the UI, because animation length belongs to the presentation layer; the
engine validates every call instead.

**Greedy vs BFS ghosts.** Settled by running 480 chases rather than by argument.

**Machine-dependent paths.** Absolute paths appeared in `main.py` and in the highscore
tests, which breaks on the other developer's machine. Partly fixed; the tests still carry
an absolute path.

---