# Milestone 08 — Pause and Resume

## Objective
Pause gameplay and resume it without losing time from active level and ghost-state timers.

## 1. Pausing (`pause_option`)

When the game is paused, `pause_option()`:

- Sets `self.game_paused = True`.
- Records the pause start using `time.monotonic()` in `self.pause_started_at`.

The game loop skips gameplay updates while `game_paused` is `True`. Keyboard handling and rendering are managed in the separate visual interface.

## 2. Resuming (`resume_game`)

The method calculates elapsed pause time:

```python
paused_time = time.monotonic() - self.pause_started_at
```

It then shifts active deadlines forward by that duration:

- `self.level_expires_at` — level time limit.
- `self.edible_active_unitl` — edible-mode expiration, when active.
- `g.respawn_time_at` — the deadline of each ghost in `RESPAWNING` state.

Finally, it clears the pause state and resets `self.pause_started_at` to `None`.

## 3. Technical Choice

**`time.monotonic()`** measures elapsed time independently of system-clock adjustments. Instead of pausing the clock itself, the implementation extends deadlines by the amount of time spent paused.
