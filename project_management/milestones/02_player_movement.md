### mlahssin

# Milestone 02 — Player Movement

## Objective

Implement player movement through accessible maze cells, including direction changes, wall restrictions, and smooth pixel movement.

## 1. Movement Representation

The `Character` base class provides movement attributes shared by the player and ghosts:

- `pos`: current logical grid position `(x, y)`.
- `x_pix`, `y_pix`: current pixel coordinates.
- `direction`: active movement direction.
- `target_pos`: next grid cell, or `None` when no cell transition is active.
- `frames_per_cell`: number of movement updates used to cross one cell.
- `previous_pos` and `moves`: previous completed cell and completed-move count.

**Technical choice:** Grid coordinates handle navigation, while pixel coordinates are updated progressively for smooth movement.

## 2. Player Direction Management

The `Player` class inherits from `Character` and adds `requested_direction`.

- **`request_direction()`** validates a direction (`up`, `down`, `left`, or `right`), converts it to lowercase, and stores it.
- **`choose_direction()`** applies the requested direction when the next movement is possible.
- When movement toward another cell is already in progress, an opposite-direction request reverses movement by swapping `pos` and `target_pos` and updating `direction`.
- Other direction requests remain stored until a turn can be applied; a blocked turn does not replace the current direction.

## 3. Movement Validation

**`Character.start_move()`** first checks that no movement is already in progress, then calls `Maze.can_move()` to verify the requested movement against maze boundaries and wall bitmasks.

If movement is valid, it calculates and stores the adjacent cell in `target_pos`. Otherwise, it returns `False`.

## 4. Smooth Movement Between Cells

**`Character.update()`** advances movement using pixel coordinates:

1. Start a valid move if `target_pos` is not yet set.
2. Calculate the pixel center of the destination cell.
3. Calculate horizontal and vertical movement steps using `frames_per_cell`.
4. Advance `x_pix` and `y_pix`, clamping them to the destination to prevent overshooting.
5. Once the destination is reached, update `previous_pos` and `pos`, increment `moves`, and clear `target_pos`.

The default value is **20 movement updates per cell**. The logical grid position changes only when a cell transition finishes, except when the player reverses direction mid-transition.

## 5. Main Methods

| Method | Responsibility |
|---|---|
| `Player.request_direction()` | Validate and store a requested direction. |
| `Player.choose_direction()` | Apply a turn or reverse an ongoing movement. |
| `Character.start_move()` | Validate and set the next target cell. |
| `Character.update()` | Progress pixel movement and complete cell transitions. |
| `Maze.can_move()` | Check boundaries and walls before movement. |


### ayait-ih

## 6. Keyboard Input (`GameScene.handle_event`)
 
The UI reads the keyboard and sends the direction to the player. The UI never moves the player itself: it only *requests* a direction, and the game logic decides if the move is possible.
 
| Keys | Direction |
|---|---|
| `←` or `A` | `left` |
| `→` or `D` | `right` |
| `↑` or `W` | `up` |
| `↓` or `S` | `down` |
 
Both arrow keys and WASD are supported, as required by the subject ("arrow keys or WASD, depending on your keyboard").
 
**Technical choice:** `handle_event()` only stores the key in `self.direction`. The direction is sent to the player once per frame in `update()`, so all game changes happen in the same place and in a fixed order.
 
## 7. Frame Update Order (`GameScene.update`)
 
Every frame, `GameScene.update()` calls the game logic in this order:
 
1. If a key was pressed, call `player.request_direction(direction)`, then clear it.
2. `player.choose_direction(maze)`: apply the turn if it is possible.
3. `player.update(maze)`: move the player a few pixels.
4. Collect gums, then update and move the ghosts.
5. Handle collisions.
6. Check if the level is completed, or if the game is won or lost.
The game runs at a fixed **60 FPS** (`clock.tick(60)` in `App`). With the default `frames_per_cell = 20`, the player crosses one cell in **20 / 60 = 0.33 seconds**.
 
## 8. Drawing the Player
 
### Smooth Position
 
The player is drawn at its **pixel position** (`x_pix`, `y_pix`), not at its grid cell. This shows the smooth movement calculated by `Character.update()` between two cells.
 
The sprite is centered on that position with `img.get_rect(center=(x_pix, y_pix))`.
 
### Facing Direction
 
The player has two sprites: one facing **right** and one facing **left**.
 
| Player direction | Sprite used |
|---|---|
| `left` | Facing left |
| `right` | Facing right |
| `up` / `down` | Keeps the last horizontal sprite |
 
**Technical choice:** a `facing` attribute remembers the last horizontal direction, so the player does not "flip" when moving up or down. It is reset to `right` when a new game starts.
 
### Fallback
 
If a sprite image is missing, a circle is drawn at the same position, so the game still works.
 
## 9. Scaling the Maze to the Window
 
The maze is drawn on a **canvas** at a fixed design size (`CELL = 80` pixels per cell). The finished canvas is then resized to fit the window and centered:
 
| Step | Detail |
|---|---|
| Scale | `min(window_width / canvas_width, window_height / canvas_height)`: the canvas fits without being cut |
| Resize | `pygame.transform.smoothscale(canvas, scaled_size)` |
| Center | An `offset` adds the same empty space on both sides |
 
**Technical choice:** the movement logic always works with the same cell size (80 px), whatever the window size. The UI only changes how big the result is displayed.
