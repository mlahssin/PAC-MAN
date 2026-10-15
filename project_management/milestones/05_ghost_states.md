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