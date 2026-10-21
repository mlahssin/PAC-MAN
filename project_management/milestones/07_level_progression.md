### mlahssin

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


### ayait-ih


## 6. Level Check in `GameScene.update`
 
The game loop described in section 5 is in `GameScene.update()`. After everything has moved and collisions are handled, the UI asks the game if the level is over:
 
```python
if game.does_level_completed():
    if game.succesfully_complete_level():
        game.Next_level()
    else:
        game.initialize_level()
```
 
The UI does not need to redraw anything by hand: on the next frame, it draws the new maze, the new gums and the characters from the new level data.
 
## 7. Showing the Level and the Time
 
### Level Board
 
The LEVEL board in the sidebar shows the current level out of 10:
 
```python
f"{game.level:02d} / 10"     # level 3 -> "03 / 10"
```
 
`:02d` always writes two digits, so the board keeps the same width from level 1 to level 10.
 
### Level Timer
 
The timer at the top of the sidebar shows the time left before `level_expires_at`:
 
```python
time_left = max(0, game.level_expires_at - time.monotonic())
minutes, seconds = divmod(int(time_left), 60)
text = f"{minutes:02d}:{seconds:02d}"      # 95 s -> "01:35"
```
 
- `max(0, ...)` never shows a negative time.
- `divmod(x, 60)` splits the seconds into minutes and seconds.
- The text is drawn on a wooden timer sign image.
## 8. Victory
 
When `Next_level()` goes past level 10, it sets **both** `game_won` and `game_over` to `True`. The UI checks `game_won` **first**:
 
```python
if game.game_won:
    self.app.change_scene("victory")
else:
    self.app.change_scene("game_over")
```
 
**Technical choice:** because `game_over` is also `True` after a win, checking it first would send a winner to the Game Over screen. Testing `game_won` first gives the correct screen.
 
The level number is already `11` after the last level, so the UI saves it as `min(game.level, 10)`. The Victory screen then shows **10 / 10** instead of 11 / 10.
 
The Victory screen shows the final score and level, then lets the player enter a name for the highscores, like the Game Over screen.
 
## 9. Testing All the Levels
 
Playing ten full levels to test the victory screen takes a long time. During development, a key calls `game.Next_level()` directly, to jump to the next level and quickly test:
 
- that each level loads a new maze;
- that the LEVEL board and the timer update;
- that finishing level 10 opens the Victory screen.
This key is now part of the **cheat mode** used during the evaluation.
