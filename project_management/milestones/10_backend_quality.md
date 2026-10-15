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
