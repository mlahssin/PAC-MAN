# Milestone 07 — Level Progression

## Objective
Manage level completion, retries after timeout, advancement through ten levels, and the final victory condition.

## 1. Level Setup (`initialize_level`)

Each level generates a maze using its corresponding entry in `self.levels_seeds`. It recreates the player, four ghosts, gums, and supergums, then resets level-specific state and its 180-second deadline.

Ghost speed and random-movement frequency are adjusted using `self.levels_frames` and `self.random_per`. The game's score and remaining lives are not reset when a new level is initialized.

Entity positions and collectible placement are documented in **Milestone 01**.

## 2. Detecting the End of a Level (`does_level_completed`)

The method reports that a level has ended when either:

- Both `self.gums` and `self.super_gums` are empty; or
- The level timer reaches `self.level_expires_at`.

In either case, it sets `self.level_completed = True` and returns `True`. Otherwise it returns `False`.

## 3. Checking Successful Completion (`succesfully_complete_level`)

A level is successful only when **all normal gums and all supergums** have been collected. A timeout alone does not count as success.

## 4. Advancing (`Next_level`)

When the game is not over, `Next_level()` increases the level number. Levels 1–10 are playable; progressing beyond level 10 sets `self.game_won` and `self.game_over` to `True`. Otherwise, it calls `initialize_level()` to prepare the next level.

## 5. Level Outcome in the Game Loop

The existing game loop checks `does_level_completed()` and then `succesfully_complete_level()`:

- **Successful:** Call `Next_level()`.
- **Unsuccessful (timer expired):** Call `initialize_level()` to retry the current level.

This retry does not reset the accumulated score or remaining lives.
