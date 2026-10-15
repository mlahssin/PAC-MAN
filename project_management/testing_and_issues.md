# PAC-MAN — Testing, Issues, and Resolutions

## Evidence convention

- **Observed/reported:** A problem or behavior discussed during development; not necessarily backed by a saved automated test.
- **Fixed/reported working:** The implementation was changed and the team reported it working; attach logs/screenshots/commit links when available.
- **To verify:** An acceptance test we recommend but whose executed result is not documented.

## Issues and resolutions

| Issue | Cause / observation | Resolution or decision | Evidence status |
|---|---|---|---|
| Assigned `mazegenerator` wheel rejected by `uv` | Wheel filename `mazegenerator-00001-py3-none-any.whl` did not match internal version `2.0.2` | Renamed to `mazegenerator-2.0.2-py3-none-any.whl`, then ran `uv add ./mazegenerator-2.0.2-py3-none-any.whl`; package code unchanged | Fixed/reported working |
| Ghosts converge and travel together | Identical BFS decisions from the same position can lead to identical paths | Periodically choose a random accessible neighbor instead of the BFS successor | Implementation present; no formal test log |
| Ghost fleeing oscillates or stays near a corner | Greedy distance choice can revisit positions or dead ends | Filter dead-end-like neighbors when alternatives exist and avoid immediate return to `previous_pos` | Improved/reported; edge cases still possible |
| Git merges blocked/conflicted on compiled Python files | Tracked `__pycache__`/`.pyc` changed between branches | Stop tracking generated cache files and add ignore rules | Resolution discussed; verify repository state |
| Timers advance during pause | Wall-clock deadlines continue unless adjusted | On resume, shift level, edible, and respawn deadlines by paused duration | Implemented; edge tests pending |
| `Character.update()` position assignment after renaming variables | Old `tx, ty` references were undefined | Use `target_x, target_y` on completed movement | Corrected in reviewed code |
| `Caracter.py` formatting warnings | Whitespace, blank lines, indentation, and line length | Formatting-only cleanup prepared; no gameplay changes intended | Re-run `flake8` and record result |

## Acceptance test checklist

These are **test cases to execute or document**, not an assertion that they have all passed.

| Area | Test procedure | Expected result | Recorded result |
|---|---|---|---|
| Maze generation | Start the game and regenerate a level | Maze is created from the assigned package | To verify formally |
| Spawn positions | For every configured level seed, call spawn validation | Center and all four corners are reachable | To verify |
| Player movement | Request movement through a wall and through an open corridor | Walls block movement; accessible moves complete | To verify formally |
| Player reversal | Reverse direction halfway between two cells | Direction changes without incorrect position jump | To verify |
| Ghost chasing | Observe ghost following a reachable player | BFS-based next cell is chosen except on random steps | To verify |
| Ghost synchronization | Put two ghosts in the same cell | Occasional random choices can separate paths; separation is not guaranteed | To verify |
| Normal gum | Enter an unvisited cell containing a gum | Gum removed; score increases by 10 once | To verify |
| Supergum | Collect a corner supergum | Supergum removed; score increases by 50; ghosts enter edible state | To verify |
| Edible timer | Wait for edible deadline | Eligible edible ghosts become dangerous again | To verify |
| Edible-ghost collision | Contact a ghost in edible state | Ghost respawns; score increases by 200 | To verify |
| Dangerous-ghost collision | Contact ghost while not invincible | Lose a life and reset positions; zero lives ends game | To verify |
| Respawn timer | Allow respawn delay to expire | Ghost returns to dangerous state | To verify |
| Level completion | Collect all gums and supergums | Next level starts, preserving score and lives | User reported gameplay functional; save test evidence |
| Level timeout | Allow timer to expire with collectibles remaining | Current level restarts under team-selected rule | To verify formally |
| Final victory | Complete Level 10 | Game marks victory and game over | User reported functional; save test evidence |
| Pause/resume | Pause during active level, edible, and respawn timers | Position updates stop and deadlines are extended on resume | To verify formally |
| Cheat controls | Enable cheat mode and test invincibility, life, speed, freeze, skip | Each effect behaves as implemented; disabling resets toggles | To verify |
| Static checks | Run `flake8 .` and project `mypy` command | No remaining required violations | Pending |

## Remaining risks / follow-ups

1. `Game.initialize_level()` places corner ghosts and supergums without explicitly calling `Maze.validate_spawns()`; check all predefined seeds.
2. `Game.__init__()` receives `perfect` and `seed`, but level generation uses `False` and entries from `levels_seeds`; confirm intended configuration behavior.
3. The ghost fleeing heuristic and randomized chasing reduce repetitive behavior without guaranteeing it disappears.
4. Record actual execution dates, commands, outputs, screenshots, and commit links before reporting tests as passed.

## Test-record template

| Date | Commit/branch | Test | Steps/input | Expected | Actual | Pass/fail | Fix/reference |
|---|---|---|---|---|---|---|---|
| _Fill after execution_ | | | | | | | |
