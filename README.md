*This project has been created as part of the 42 curriculum by mlahssin, ayait-ih.*

# PAC-MAN

## Description

A Pac-Man game written in Python with Pygame. Move through an externally generated maze, collect gums, avoid dangerous ghosts, and eat edible ghosts. Complete ten levels to win and record your score. The game includes menus, instructions, persistent highscores, pause/resume, a gameplay HUD, ending screens, and evaluation cheats.

## Instructions

### Installation and execution

Requirements: Python 3.13 or later, `uv`, `make`, and a graphical desktop supporting Pygame. Keep the supplied generator wheel at the repository root. Run commands from the repository root because assets and configuration use relative paths.

```bash
make install
make run
```

Installation runs `uv sync` to create/synchronize `.venv` and install Pygame, Pydantic, and the external generator. No source compilation is needed. The application takes exactly one argument, a filename ending in `.json`:

```bash
uv run python main.py config.json
make run ARGS=custom.json
```

Missing/extra arguments or a non-JSON filename produce a clear error. Invalid or unreadable configuration content falls back to defaults with warnings.

### Controls and rules

| Input | Action |
|---|---|
| Arrow keys / WASD | Move |
| Escape / pause button | Pause |
| Mouse | Select menu buttons, resume, return to menu, or exit |
| Keyboard on ending screens | Enter a name; Backspace deletes a character |
| Save button | Save the score and return to the main menu |

Collect all regular gums and supergums to advance. Supergums temporarily make ghosts edible. Touching a dangerous ghost costs a life and returns the player to the center. Score and lives carry over between levels. Losing all lives ends the game; completing level ten wins. A timeout restarts the current level. Gameplay currently uses 180 seconds per level.

Press `C` to toggle cheat mode. While enabled:

| Key | Action |
|---|---|
| F1 | Toggle invincibility |
| F2 | Skip level |
| F3 | Toggle ghost freeze |
| F4 | Restore one life, up to three |
| F5 | Toggle increased player speed |

Disabling cheats resets invincibility, freeze, and increased speed.

### Development commands

```bash
make debug   # Launch under pdb
make lint    # Run flake8 and the required mypy checks
make clean   # Remove Python and analysis caches
```

The lint tools must be available to `uv run`. They are not declared in the current project dependencies; if necessary, install them with:

```bash
uv pip install flake8 mypy
```

## Configuration

The configuration is a JSON object. Whole lines starting with `#`, including indented comment lines, are ignored; inline comments are not supported. Missing/invalid values revert to defaults with messages on standard error. Unknown keys are ignored with a warning. Invalid `levels` values fall back to the default list.

Example of settings currently applied to gameplay:

```json
{
  "highscore_filename": "highscore.json",
  "lives": 3,
  "points_per_pacgum": 10,
  "points_per_super_pacgum": 50,
  "points_per_ghost": 200
}
```

| Key | Validation default | Accepted values / current behavior |
|---|---|---|
| `highscore_filename` | `"highscores.json"` | String path; relative to the working directory |
| `lives` | `3` | Integer, 1–3; starting lives |
| `points_per_pacgum` | `10` | Non-negative integer; regular gum points |
| `points_per_super_pacgum` | `50` | Non-negative integer; supergum points |
| `points_per_ghost` | `200` | Non-negative integer; edible ghost points |
| `pacgum` | `42` | Integer, 0–500; validated, but actual placement fills reachable cells except spawn cells |
| `seed` | `42` | Non-negative integer; validated, but gameplay fixes the first seed to 42 |
| `level_max_time` | `90` | Integer, 10–600; validated, but gameplay uses 180 seconds |
| `levels` | Ten objects with `width: 15`, `height: 15` | Non-empty array; integer dimensions 5–30; validated, but gameplay uses ten 15×15 levels |

The supplied `config.json` selects `highscore.json`, 12 points per regular gum, and 500 points per ghost. Its invalid supergum point value falls back to 50.

## Highscore

The game stores a JSON array of player-name/score records locally:

```json
[
  {"name": "PLAYER 1", "score": 1250}
]
```

JSON offers readable storage without a database or server, using Python's standard library. `highscore_filename` selects the file. Scores load at application startup and when opening the leaderboard. After victory or defeat, enter a name and click Save to persist your result and return to the menu.

Loaded records are filtered to names of at most ten characters containing letters, digits, or spaces, and non-negative integer scores. Loading sorts descending and keeps ten entries; saving also sorts and retains ten. Missing files are created when possible. Filesystem and JSON errors produce warnings; failed loads use an empty board.

The ending screens uppercase typed names. Their current length check happens before uppercasing, so a Unicode character that expands during conversion can exceed the intended ten-character limit.

## Maze Generation

`maze.py` adapts the assigned external A-Maze-ing package. `pyproject.toml` installs the bundled `mazegenerator-2.0.2-py3-none-any.whl`. The project-management notes record renaming the supplied wheel to match its internal version, without changing package code.

Generation uses the external interface:

```python
MazeGenerator(size=(width, height), perfect=False, seed=seed).maze
```

The returned wall-bitmask grid drives movement and rendering. `Maze` supplies navigation helpers and breadth-first searches; it delegates maze generation to the package. Level one uses seed 42. Nine random seeds are selected for subsequent levels when a new game is created. Generator exceptions print an error to standard error and exit with status 1.

## Implementation

Grid coordinates govern walls, collectibles, and pathfinding; interpolated pixel coordinates provide movement. `Player` and `Ghost` inherit shared movement from `Character`. The player queues requested directions. Ghosts combine shortest-path chasing with occasional random moves and choose routes away from the player while edible.

`Game` owns collisions, lives, scoring, collectibles, progression, timers, and cheats. Supergums enable edible mode for 100 seconds. Eaten ghosts return to their corner in a respawning state for ten seconds. Deadlines use `time.monotonic()` and are compensated after a pause.

`App` runs the Pygame event/update/draw loop at a target of 60 FPS. Scenes implement the interface; Pydantic validates configuration, and the standard `json` module handles score persistence.

## General Software Architecture

| Module/directory | Responsibility |
|---|---|
| `main.py` | CLI validation, configuration loading, application startup |
| `config.py` | `Config`, `Settings`, and `Level`: parsing, comment removal, validation/defaults |
| `app.py` | Window, loop, scene registry, settings, and score engine |
| `Game.py` | Gameplay state; creates `Maze`, `Player`, and four `Ghost` objects |
| `Character.py` | Shared `Character` movement and specialized player/ghost behavior |
| `maze.py` | External generator adapter and navigation helpers |
| `Leaderboard.py` | `Leaderboard_Engine`: score loading, filtering, sorting, saving |
| `scenes/base.py` | Common scene interface |
| `scenes/` | Menu, gameplay, instructions, leaderboard, pause, defeat, and victory screens |
| `assets/` | Images and font |
| `project_management/` | Team organization, milestones, decisions, progress, and issue records |

Flow: `main.py` loads settings and creates `App`; `App` dispatches events to its active scene. `GameScene` uses `Game` for gameplay. Ending screens use the application's score engine to save results.

## Project Management

The team divided backend/gameplay and graphical-interface work, coordinating integration through Git. Recorded responsibilities assign maze integration, movement, ghost logic, scoring, collisions, progression, timers, and cheats to mlahssin; Pygame rendering, assets, menus, and interface/input integration to ayait-ih (Ayoub).

See the [dedicated project-management directory](project_management/README.md), [progress tracking](project_management/progress.md), and [testing and issue records](project_management/testing_and_issues.md). These documents describe milestones and technical choices and distinguish implemented/reported behavior from checks still awaiting recorded test evidence.

## Resources

- [Pygame documentation](https://www.pygame.org/docs/): graphics, events, fonts, images, and the game loop.
- [Pydantic documentation](https://docs.pydantic.dev/latest/): configuration models and validation.
- [uv documentation](https://docs.astral.sh/uv/): dependency and environment management.
- Official Pac-Man subject v1.4 and correction sheet supplied through the school project page: project requirements and evaluation criteria.
- Assigned A-Maze-ing wheel and its bundled source/metadata: generator interface and wall representation.

### AI usage

AI was used to help us understand programming concepts, including how Pygame works, and to assist with debugging when we struggled with errors. This included explanations related to the graphical interface and help investigating gameplay, configuration, and highscore issues.


## Packaging and Deployment Status

The repository currently supports running from source. A root packaging script/spec and a documented downloadable gaming-platform build remain to be supplied. The commands above describe source execution, not a packaged release.
