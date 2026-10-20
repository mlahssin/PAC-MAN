# Milestone 04 — Collectibles and Scoring

## Objective

Implement the collection of normal gums and supergums and manage score updates.

## 1. Collectible Storage

Two sets store the positions of remaining collectibles:

- `self.gums`: normal gums on reachable maze cells, excluding the center and four corners.
- `self.super_gums`: four supergums, one at each corner.

`self.visited` records collected positions, preventing the same cell from awarding points twice. These collections are recreated in `initialize_level()` for each level, while the total `self.score` is preserved.

## 2. Collecting Items (`collect_gums`)

The method runs during gameplay and checks the player's logical cell position.

1. If `self.player.target_pos` is not `None`, the player is between cells, so collection is skipped.
2. If the current cell is already in `self.visited`, no points are awarded.
3. Otherwise, the method checks for a normal gum first, then a supergum.
4. A collected item is removed from its corresponding set and the position is added to `self.visited`.

This ensures collectibles are processed when the player reaches a cell and cannot be collected repeatedly.

## 3. Scoring Rules

| Collectible or event | Points | Implementation |
|---|---:|---|
| Normal gum | +10 | Remove the cell from `self.gums` |
| Supergum | +50 | Remove the cell from `self.super_gums` and activate edible mode | 

The score starts at `0` in `Game.__init__()` and carries over between levels.

## 4. Supergum Effect

When the player collects a supergum, `collect_gums()`:

score added is 50 to the original score


### ayait-ih

## 5. Drawing the Collectibles
 
The UI draws the gums directly from the two sets of the game, `game.gums` and `game.super_gums`, every frame.
 
| Collectible | Image | Size | Fallback |
|---|---|---|---|
| Normal gum | `gum.png` | `CELL // 3` | small white circle |
| Supergum | `supergum.png` | `CELL // 2` | bigger yellow circle |
 
A helper converts a grid cell into the pixel center of that cell:
 
```python
def cell_center(self, col, row):
    return (col * CELL + CELL // 2, row * CELL + CELL // 2)
```
 
Each image is then centered on that point with `get_rect(center=...)`.
 
**Technical choice:** the UI does not keep its own list of gums. Because it reads `game.gums` and `game.super_gums` every frame, a gum removed by `collect_gums()` disappears from the screen automatically on the next frame. The display always matches the game state.
 
## 6. Drawing Order (Layers)
 
Everything in the maze is drawn on the same surface, so the order decides what appears on top:
 
1. Dark transparent background of the maze
2. 42 pattern cells
3. Walls
4. Gums
5. Supergums
6. Player
7. Ghosts
Collectibles are drawn **before** the characters, so the player and the ghosts always appear on top of the gums.
 
## 7. Score Display (Sidebar)
 
The sidebar shows the game information on wooden boards, from top to bottom:
 
| Board | Value shown |
|---|---|
| Timer | Time left in the level (`MM:SS`) |
| SCORE | `game.score` |
| HIGH SCORE | Best saved score |
| LEVEL | `game.level` as `03 / 10` |
| LIVES | Full and empty hearts |
 
All boards are drawn by one method, `draw_board(label, value, y)`, which draws the board image, the label and the value, then returns the `y` position of the next board. This keeps every board the same size and evenly spaced.
 
**Technical choice:** the score is read from `game.score` every frame, so it updates as soon as a gum is collected, with no extra code in the UI.
 
## 8. Final Score on the End Screens
 
When the game ends, `GameScene` saves the result in the app before changing scene:
 
```python
self.app.last_score = game.score
self.app.last_level = game.level
```
 
The **Game Over** and **Victory** screens read these values to show the final score and level, then ask the player to enter a name for the highscores.
 
**Technical choice:** the values are copied into `app` because the game object is cleared (`game = None`) so that the next PLAY starts a new game. The end screens still have the final score.