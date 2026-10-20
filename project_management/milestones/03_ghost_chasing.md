### mlahssin

# Milestone 03 — Ghost Chasing

## Objective

Implement ghost navigation toward the player using Breadth-First Search (BFS), with occasional random moves to make ghost behavior less predictable.

## 1. Ghost Movement Structure

The `Ghost` class inherits grid and pixel movement from `Character`:

- `pos` stores the current grid cell.
- `direction` stores the selected direction.
- `target_pos` stores the next cell during movement.
- `moves` counts completed cell transitions.

The `Ghost.choose_direction()` method selects where the ghost should move; the inherited `Character.start_move()` and `Character.update()` methods validate and perform the movement.

## 2. Chasing the Player with BFS

When a ghost is in the `DANGEROUS` state, it can chase the player's current grid position.

1. Call `Maze.find_shortest_path(ghost.pos, player_pos)`.
2. The maze uses BFS over accessible neighboring cells to find a shortest path in the unweighted grid.
3. If the path has at least two cells, select `path[1]` as the next destination; `path[0]` is the ghost's current cell.
4. If no next cell is available, clear the direction and return `False`.

**Technical choice:** BFS finds a shortest route through accessible passages without crossing walls.

## 3. Random Movement

Since all ghosts use the same BFS algorithm, ghosts reaching the same position may follow identical paths and move together. We introduced occasional random movements to reduce this synchronization and prevent ghosts from reaching the player too quickly.

- `self.coefecient` controls how frequently random movement occurs.
- When `self.moves % self.coefecient == 0`, the ghost selects a random accessible neighbor using `Maze.get_neighbors()`.
- Otherwise, it follows the BFS shortest path toward the player.
- If no accessible neighbor exists, the ghost stops moving.

The initial coefficient is `4`, and `Game.initialize_level()` adjusts it for each level using `self.random_per`.


## 4. Converting the Destination into a Direction

After selecting `next_pos`, `Ghost.choose_direction()` calculates the grid offset between the current and next cells. It compares this offset with `DIRECTIONS` to set the corresponding direction (`up`, `down`, `left`, or `right`).

If the ghost is already moving toward a `target_pos`, the method does not select a new direction until the current cell transition ends.

## 5. Main Methods

| Method | Responsibility |
|---|---|
| `Ghost.choose_direction()` | Select the next movement direction according to ghost state. |
| `Maze.find_shortest_path()` | Find a shortest path from ghost to player using BFS. |
| `Maze.get_neighbors()` | Return accessible adjacent cells for random movement and pathfinding. |
| `Character.start_move()` | Validate movement and set the next target cell. |
| `Character.update()` | Move progressively toward the target and complete the cell transition. |
| `Game.initialize_level()` | Set the ghost's movement parameters for the level. |


### ayait-ih

## 6. Updating the Ghosts Every Frame (`GameScene.update`)
 
The UI calls the ghost logic once per frame, after the player has moved:
 
```python
for ghost in game.ghosts:
    ghost.choose_direction(game.maze, game.player.pos)
    ghost.update(game.maze)
```
 
1. `choose_direction()` receives the player's **current grid cell** (`player.pos`), so each ghost chases the player's latest position.
2. `update()` moves the ghost a few pixels toward its next cell.
3. `game.handle_collisions()` is called **after** all characters have moved, so collisions are checked with the final positions of the frame.
**Technical choice:** the UI only calls the methods in the right order. Where the ghost goes (BFS or random move) is decided entirely by `Ghost.choose_direction()`.
 
## 7. Drawing the Ghosts
 
### One Sprite per Ghost
 
Four ghost images are loaded once in `GameScene.__init__()` and stored in a list. Ghost number `i` in `game.ghosts` uses image number `i`, so each ghost always keeps the same look and the player can follow each one on screen.
 
| Ghost index | Image |
|---|---|
| `0` | `ghost1.png` |
| `1` | `ghost2.png` |
| `2` | `ghost3.png` |
| `3` | `ghost4.png` |
 
### Smooth Position
 
Like the player, each ghost is drawn at its **pixel position** (`x_pix`, `y_pix`) and centered with `get_rect(center=...)`, so the ghost slides smoothly between cells instead of jumping.
 
## 8. Showing the Ghost State
 
The ghost image depends on its `state`:
 
| State | Image |
|---|---|
| `DANGEROUS` | Normal sprite |
| `EDIBLE` | Tinted copy of the same sprite |
 
### How the Edible Image is Made
 
No extra image file is needed. In `__init__()`, each ghost image is **copied** and tinted with a color multiplication:
 
```python
edible = img.copy()
edible.fill((120, 255, 255), special_flags=pygame.BLEND_RGB_MULT)
```
 
`BLEND_RGB_MULT` multiplies each pixel by the color, so the red channel is reduced and the sprite turns blue-cyan, while its shape and transparency stay the same.
 
**Technical choices:**
 
- The tinted images are created **once** at start, not every frame, to keep drawing fast.
- The player instantly recognizes a weak ghost because it is the **same** character with a different color.
- The UI only **reads** `ghost.state`. The state itself (when a ghost becomes edible and for how long) is managed by the game logic.
