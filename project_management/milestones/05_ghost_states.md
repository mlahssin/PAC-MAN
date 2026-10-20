# Milestone 05 — Ghost States

## Objective

Implement ghost states and manage their behavior and transitions during gameplay.

## 1. Ghost States

Each ghost stores its current state in `self.state`, initially set to `DANGEROUS`.

| State | Behavior |
|---|---|
| `DANGEROUS` | Chases the player using BFS, with occasional random movement. |
| `EDIBLE` | Attempts to flee by selecting a neighboring cell with a longer shortest path to the player. |
| `RESPAWNING` | Does not choose a movement direction while waiting to become dangerous again. |

`Ghost.choose_direction()` selects the behavior according to the current state. The chasing algorithm is documented in Milestone 03.

## 2. Activating Edible Mode

When a supergum is collected, `Game.collect_gums()` sets all ghosts to `EDIBLE` and sets `self.edible_active_unitl` to `time.monotonic() + 100`.

During this state, `Ghost.run_away()` selects a neighboring cell to increase the shortest-path distance from the player. It prefers avoiding dead ends and immediately returning to the previous cell when alternatives exist.

## 3. Ghost Respawning

When the player collides with an `EDIBLE` ghost, `Game.handle_collisions()`:

- Moves the ghost back to its starting position.
- Resets its movement information and sets its state to `RESPAWNING`.
- Sets `respawn_time_at` to `time.monotonic() + 10`.

The ghost remains unable to move until its respawn timer expires. Collision handling and the score awarded for eating a ghost are covered in Milestone 06.

## 4. Timer-Based Transitions (`ghost_update`)

`Game.ghost_update()` uses `time.monotonic()` to manage two transitions:

- **Edible timer expires:** Remaining `EDIBLE` ghosts return to `DANGEROUS` after 100 seconds.
- **Respawn timer expires:** A `RESPAWNING` ghost returns to `DANGEROUS` after 10 seconds.

The respawn timer is tracked separately for each ghost.


### ayait-ih

## 5. Calling the State Updates (`GameScene.update`)
 
The UI calls `game.ghost_update()` once per frame, after the gums are collected and before the ghosts move:
 
1. `game.collect_gums()`: a supergum can switch the ghosts to `EDIBLE`.
2. `game.ghost_update()`: the timers can switch ghosts back to `DANGEROUS`.
3. `ghost.choose_direction()` and `ghost.update()`: each ghost moves according to its **new** state.
**Technical choice:** with this order, a ghost never moves one extra frame with an old state.
 
## 6. Showing Each State on Screen
 
The UI reads `ghost.state` every frame and chooses the image:
 
| State | Image shown | Why |
|---|---|---|
| `DANGEROUS` | Normal sprite | The ghost is a threat |
| `EDIBLE` | Blue-tinted copy of the same sprite | The player sees at once which ghosts can be eaten |
| `RESPAWNING` | Normal sprite, at its start position | The ghost waits in its corner and does not move |
 
### Making the Edible Image
 
No extra image file is needed. In `GameScene.__init__()`, each ghost image is copied and tinted once:
 
```python
edible = img.copy()
edible.fill((120, 255, 255), special_flags=pygame.BLEND_RGB_MULT)
```
 
`BLEND_RGB_MULT` multiplies every pixel by the color: the red channel goes down, so the sprite becomes blue-cyan, while its shape and transparency stay the same.
 
**Technical choices:**
 
- The tinted images are created **once**, not every frame, to keep drawing fast.
- The edible ghost is the **same** character in another color, so the player knows which ghost it is.
- The UI only **reads** the state. Changing states and timers stays in the game logic.
## 7. Issue: Ghost Timers During Pause
 
### Problem
 
The edible and respawn timers use `time.monotonic()`, which is real time. When the player opened the pause menu, the clock kept running:
 
- an edible ghost could become dangerous again **while the game was paused**;
- a respawning ghost could come back during the pause;
- the level timer in the sidebar kept going down.
### Cause
 
`time.monotonic()` does not stop when the game stops. The pause menu only stopped calling `update()`, but the end times (`edible_active_unitl`, `respawn_time_at`, `level_expires_at`) were still compared to the real time.
 
### Solution
 
1. **First fix (UI side):** when entering the pause menu, the UI saved the pause time. On resume, it added the pause duration to every timer (level, edible, and each ghost respawn), so the remaining time was the same as before the pause.
2. **Final fix (shared):** pausing and resuming were moved into the game logic (`Game.pause_option()` and `Game.resume_game()`). The pause scene now only calls these two methods, so all the timer rules stay in one place.
### Result
 
When the game is paused, the ghost states, the respawn timers and the level timer are frozen, and they continue exactly where they stopped after **RESUME**.