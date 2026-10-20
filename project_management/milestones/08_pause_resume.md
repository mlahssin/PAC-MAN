### mlahssin

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


### ayait-ih

## 4. Opening the Pause Menu
 
The player can pause the game in three ways:
 
| Input | Where it is handled |
|---|---|
| `P` key | `GameScene.handle_event()` |
| `ESC` key | `GameScene.handle_event()` |
| Pause button (top-right) | `GameScene.handle_event()`, left click only |
 
All three simply change the scene to `"pause"`.
 
**Technical choice:** the pause button is drawn directly on the **window**, not on the scaled game canvas. Its rectangle is in window coordinates, so `pause_rect.collidepoint(event.pos)` works with the mouse position without any conversion.
 
## 5. The Pause Scene (`scenes/pause.py`)
 
### Pausing and Resuming the Logic
 
The pause scene connects the UI to the methods in sections 1 and 2:
 
| UI moment | Game method called |
|---|---|
| The pause scene opens (`on_enter`) | `game.pause_option()` |
| The player clicks **RESUME** | `game.resume_game()`, then back to the game scene |
 
**Technical choice:** `pause_option()` is called in `Pause.on_enter()`, which runs **every time** the pause scene opens. So it does not matter if the pause came from `P`, `ESC` or the button: the game is always paused in exactly one place.
 
### Display
 
The pause scene draws on top of the game:
 
1. The game scene is drawn first, frozen in its current state.
2. A dark transparent layer covers the whole window.
3. The **PAUSED** title is drawn with a shadow.
4. Two buttons are drawn: **RESUME** and **MAIN MENU**.
The player still sees the maze behind the menu, so it is clear that the game is only paused.
 
### Buttons
 
| Button | Action |
|---|---|
| **RESUME** | `game.resume_game()` and back to the game |
| **MAIN MENU** | Clears the game (`game = None`) and goes to the main menu, so the next PLAY starts a new game |
 
`P` or `ESC` in the pause menu also resumes the game.
 
## 6. Freezing the Timer on Screen
 
`resume_game()` shifts the deadlines only when the game **resumes**. During the pause, `level_expires_at` is not changed yet, so a timer computed with `time.monotonic()` would keep going down behind the pause menu, then jump back on resume.
 
To keep the display frozen, the sidebar uses the pause start time as "now" while the game is paused:
 
```python
if game.game_paused:
    now = game.pause_started_at
else:
    now = time.monotonic()
time_left = game.level_expires_at - now
```
 
## 7. Issues Found and Fixed
 
| Problem | Cause | Fix |
|---|---|---|
| Timer kept running during pause, and showed `1023:56` after resume | The pause start time was never set (`0`), so `time.monotonic() - 0`, a huge number of seconds, was added to the deadline | The pause is started in `Pause.on_enter()`, so the start time is always recorded |
| PLAY after MAIN MENU continued the old game | The old game object was kept | MAIN MENU sets `game = None`, and PLAY starts a new game |
| Crash when clicking under the two buttons | The click loop checked 3 buttons, but there are only 2 | Loops use `len(self.options)` |
| Scrolling the mouse wheel over a button clicked it | The wheel also sends `MOUSEBUTTONDOWN` (buttons 4 and 5) | Only `event.button == 1` (left click) is accepted |
 
The timer problem is also described in **Milestone 05 — Ghost States**.