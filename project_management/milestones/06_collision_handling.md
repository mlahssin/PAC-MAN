# Milestone 06 — Collision Handling

## Objective
Detect collisions between the player and ghosts and apply the appropriate outcome based on the ghost's state.

## 1. Collision Detection (`detect_collision`)

The method compares the player's pixel coordinates with each ghost's pixel coordinates. A collision occurs when the squared distance between their centers is at most `(20 + 20) ** 2` (a combined radius of 40 pixels).

It returns the first colliding `Ghost`, or `None` when no collision is detected.

## 2. Collision Resolution (`handle_collisions`)

The response depends on the detected ghost's state:

| Ghost state | Result |
|---|---|
| `DANGEROUS` | Unless invincibility is enabled, the player loses one life. |
| `EDIBLE` | The ghost returns to its spawn position, enters `RESPAWNING`, and the player gains 200 points. |
| `RESPAWNING` | No collision effect is applied. |

### Dangerous ghost

When the player is not invincible, one life is deducted. If lives reach zero, `game_over` becomes `True`. Otherwise, the player is reset to the maze center and all ghosts return to their corner positions with their movement and ghost states reset to `DANGEROUS`.

### Edible ghost

The ghost's grid and pixel positions are reset to its original spawn position. Its movement state is cleared, its state becomes `RESPAWNING`, and a 10-second respawn deadline is set. The score increases by 200 points.

The timing and subsequent ghost-state transitions are documented in **Milestone 05 — Ghost States**.

## 3. Implementation Choices

- **Pixel-based detection:** Collisions are checked using the characters' displayed positions rather than requiring them to occupy the same grid cell.
- **Squared distance:** Comparing `dx * dx + dy * dy` avoids calculating a square root.
- **State-dependent handling:** A single collision-resolution method applies different outcomes according to ghost state.


### ayait-ih


## 4. When Collisions Are Checked (`GameScene.update`)
 
The UI calls `game.handle_collisions()` **after** the player and all the ghosts have moved in the current frame. This way, the collision is tested with the positions that will be drawn on screen, so a hit the player sees is always a hit in the game.
 
## 5. Showing the Result of a Collision
 
The UI does not need any special code for collisions: it reads the game state every frame, so every effect appears on the next frame.
 
| Collision effect | What the player sees |
|---|---|
| Life lost | One heart in the LIVES board becomes empty |
| Player reset | The player is drawn back at the center (its `x_pix`, `y_pix` were reset) |
| Ghosts reset | The ghosts are drawn back in their corners |
| Ghost eaten | The ghost is drawn back in its corner, and the SCORE board shows +200 |
 
### Lives Display (`draw_hearts`)
 
The LIVES board shows one heart per life:
 
- a **full** heart for each life left (`i < game.lives`);
- an **empty** heart for each life lost.
The hearts are centered inside the LIVES board, with the same gap between them. If a heart image is missing, a colored circle is drawn instead (red for a life left, grey for a life lost).
 
## 6. From Game Over to the End Screen
 
When the last life is lost, `handle_collisions()` sets `game_over = True`. At the end of `GameScene.update()`, the UI checks it:
 
```python
if game.game_over or game.game_won:
    self.app.last_score = game.score
    self.app.last_level = game.level
    self.game = None
    if game.game_won:
        self.app.change_scene("victory")
    else:
        self.app.change_scene("game_over")
    return
```
 
1. The final score and level are saved in `app`, so the end screen can show them.
2. The game is cleared (`self.game = None`), so the next PLAY starts a new game.
3. The scene changes to **Game Over** (or **Victory**).
4. `return` stops the update, so nothing runs on a game that has ended.
## 7. Issues Found and Fixed
 
### Back to Game Over After Playing Again
 
**Problem:** after losing and entering a name, pressing PLAY sent the player straight back to the Game Over screen.
 
**Cause:** the old game object was kept. It still had `game_over = True`, so the very first update ended the game again.
 
**Solution:** `GameScene.on_enter()` now creates a new game when there is none **or** when the old one is over:
 
```python
if self.game is None or self.game.game_over:
    self.game = Game(...)
```
 
### Crash After Clearing the Game
 
**Problem:** `'NoneType' object has no attribute 'player'`.
 
**Cause:** the game was set to `None`, but `App.change_scene()` did not call the new scene's `on_enter()`, so no new game was created before `update()` and `draw()` used it.
 
**Solution:** `App.change_scene()` now always calls `on_enter()`, and `GameScene` checks that a game exists before updating or drawing it.