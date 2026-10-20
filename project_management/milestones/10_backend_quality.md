# Milestone 10 — Backend Quality

## Objective

Improve backend code quality, maintainability, and reliability without changing the existing gameplay behavior.

## 1. Code Review and Cleanup

We reviewed the backend classes (`Maze`, `Character`, `Player`, `Ghost`, and `Game`) to:

- Keep methods focused on clear responsibilities.
- Remove obsolete commented-out code and unnecessary duplication where appropriate.
- Improve readability and add concise docstrings.
- Organize `Game` methods by responsibility (initialization, placement, levels, scoring, collisions, ghost states, pause/resume, and cheats).

Existing algorithms and public names were preserved where changing them would require updating other modules.

## 2. Formatting and Linting

We corrected reported `flake8` formatting issues in `Caracter.py`, including spacing, blank lines, indentation, trailing whitespace, and line length.

Final checks to run from the project root:

```bash
make lint
```

The Makefile's lint target runs `flake8` and `mypy`. A successful full-project lint run has not yet been recorded here.

## 3. Type Hints and Documentation

Short method and class docstrings were added during the backend review. Type annotations and final static-type checks remain part of this milestone.

The project's intended `mypy` options are:

```bash
uv run mypy . \
    --warn-return-any \
    --warn-unused-ignores \
    --ignore-missing-imports \
    --disallow-untyped-defs \
    --check-untyped-defs
```

## 4. Error Handling and Reliability

Existing validations include maze dimensions and seed, character position and direction, and player direction requests.

Remaining checks include:

- Ensure movement parameters used as divisors or modulo operands stay positive.
- Validate spawn accessibility for the configured level seeds.
- Check initialization and reset paths for consistent player and ghost state.
- Review unused constructor parameters, imports, and attributes before removing them.

## 5. Regression Testing

After cleanup, verify that the game still behaves as intended:

| Scenario | Expected result |
|---|---|
| Player moves into a wall | Movement is blocked |
| Player reverses direction mid-cell | Direction changes without inconsistent positioning |
| Ghost chases and sometimes moves randomly | Valid movement without crossing walls |
| Collect gums and supergums | Correct removal, score, and edible-state trigger |
| Player collides with a dangerous ghost | Life decreases and characters reset |
| Player collides with an edible ghost | Ghost respawns and score increases |
| Level completes or times out | Advance or retry according to game rules |
| Pause and resume | Movement stops and active deadlines are compensated |
| Cheat features | Work only under their intended conditions |
| Complete level 10 | Victory state is reached |

These are verification scenarios; passing results must be recorded after testing, not assumed.

## Status

**In progress.** Core backend code review and initial docstrings are done. Full-project linting, type annotations, and recorded regression-test results remain to be completed.


### ayait-ih


# Frontend Quality (UI and Scenes)
 
The same review was done on the UI side: `app.py` and the scenes in `scenes/` (`menu`, `instructions`, `leaderboard`, `game`, `pause`, `game_over`, `victory`).
 
## 6. Linting Results
 
A first run of the `make lint` commands on the UI files gave:
 
| Check | First run | Main causes |
|---|---:|---|
| `flake8` | 45 errors | 41 lines over 79 characters, 1 unused import, trailing spaces, blank lines, indentation |
| `mypy` (lint options) | 107 errors | Functions without type hints |
 
Long lines were split inside parentheses, and long texts were split into two strings (Python joins them).
 
| File | `flake8` | Docstrings |
|---|---|---|
| `app.py` | ✅ | ✅ |
| `scenes/menu.py` | ✅ | ✅ |
| `scenes/instructions.py` | ✅ | ✅ |
| `scenes/leaderboard.py` | ✅ | ✅ |
| `scenes/game_over.py` | ✅ | ✅ |
| `scenes/game.py` | ⏳ | ⏳ |
| `scenes/pause.py` | ⏳ | ⏳ |
| `scenes/victory.py` | ⏳ | ⏳ |
 
Docstrings follow the **Google style** (summary line, `Args:`, `Returns:`), as allowed by PEP 257, and are checked with `pydocstyle --convention=google`.
 
## 7. Error Handling
 
| Problem | Fix |
|---|---|
| A missing image stopped a scene with `running = False`, but `App` set `running = True` again **after** creating the scenes, so the game crashed later with a traceback | `running = True` is set **before** the scenes are created |
| Only `FileNotFoundError` was caught when loading assets | `OSError` is caught (missing file, folder, no permission), plus `pygame.error` (corrupt file) |
| A missing **icon** stopped the whole instructions screen | Each icon has its own `try`: a missing icon is skipped with a warning |
| `last_score` / `last_level` started as `None`, so `f"{score:02d}"` could raise `TypeError` | They start at `0` and `1` |
| The app was created at module level (global variable) | Started inside `main()` with `if __name__ == "__main__":` |
 
## 8. Cleanup
 
- Removed debug prints (`print("Event")` on every mouse move, `print(target)`).
- Removed unused constants and fonts (`ICE_BLUE`, `MID_BROWN`, `MEDALS`, unused fonts in the end screens).
- Replaced fixed loop sizes (`range(3)`, `range(4)`) with `range(len(self.options))`, which fixed a crash in the pause menu.
- Buttons react to the **left click only** (`event.button == 1`), because the mouse wheel also sends `MOUSEBUTTONDOWN`.
- `dt` is now in **seconds** (`clock.tick(fps) / 1000`) instead of milliseconds.
- `change_scene()` always calls `on_enter()`, so each scene resets its state (name field, selection) when it opens.
## 9. UI Regression Testing
 
| Scenario | Expected result | Result |
|---|---|---|
| Click each menu button | The right scene opens, QUIT closes the game | |
| Scroll the mouse wheel over a button | Nothing happens | |
| PLAY after MAIN MENU in pause | A new game starts | |
| PLAY after Game Over / Victory | A new game starts | |
| `P`, `ESC`, pause button | The pause menu opens, the timer stops | |
| RESUME | The game continues with the same time left | |
| Type a name (letters, digits, spaces, Backspace) | Max 10 characters, uppercase | |
| Open Game Over / Victory a second time | The name field is empty | |
| Remove an image from `assets/` | Clear message, no traceback | |
| Remove an icon from `assets/` | Instructions still open without that icon | |
| Window of another size | Every scene scales and stays centered | |
 
Results must be filled in after testing.
 
## Frontend Status
 
**In progress.** `flake8` and docstrings are done for `app.py`, `menu`, `instructions`, `leaderboard` and `game_over`. Remaining: `game`, `pause` and `victory`, type hints for every UI method, and the recorded test results.