### mlahssin

## 1. Maze Generator Installation — Issue and Resolution

### Problem

While installing the assigned `mazegenerator` package using `uv`, the installation failed with the following error:

```text
Wheel version does not match filename (2.0.2 != 1)
```

### Cause

The wheel filename did not match the package's internal version metadata:

- **Original filename:** `mazegenerator-00001-py3-none-any.whl`
- **Internal package version:** `2.0.2`

Since `uv` validates wheel filenames against their metadata, it rejected the package.

### Solution

We renamed the wheel to match its internal version:

```bash
mv mazegenerator-00001-py3-none-any.whl mazegenerator-2.0.2-py3-none-any.whl
```

Then installed it using:

```bash
uv add ./mazegenerator-2.0.2-py3-none-any.whl
```

### Result

The installation succeeded without modifying the package's internal code or metadata, preserving the original maze generator as required by the project.

---

## 2. Maze Class Implementation

We created a custom `Maze` class to integrate the external maze generator into our PAC-MAN game.

### Maze Initialization

The constructor validates the maze dimensions and seed before generating the grid using `MazeGenerator`.

The generated grid is stored in `self.grid`, alongside its width, height, and seed.

### Maze Navigation

We implemented the following methods:

| Method | Responsibility |
|---|---|
| `is_inside()` | Checks whether a position is within the maze boundaries. |
| `can_move()` | Validates movement using boundaries and wall bitmasks. |
| `get_neighbors()` | Returns accessible neighboring cells. |
| `get_reachable_cells()` | Uses BFS to find all reachable cells. |
| `get_42_cells()` | Identifies fully walled cells forming the maze's 42 pattern. |
| `validate_spawns()` | Checks whether all four corners are reachable from the center. |
| `start_reachable_cells()` | Delegates to `get_reachable_cells()`. |
| `find_shortest_path()` | Uses BFS to find the shortest path between two cells. |

### Technical Choices

- **Wall Representation:** We use the generator's wall bitmasks to determine valid movements between cells.
- **Breadth-First Search (BFS):** We use BFS for reachability checks and shortest-path calculations because the maze is an unweighted grid.
- **OOP Design:** The `Maze` class groups maze generation and navigation methods, keeping maze-related operations separate from gameplay logic in `Game`

## 3. Caracter implementation (player/ghost) initialisation:

i implemented a base Character class containing shared attributes such as position, direction, and movement state.

The Player and Ghost classes inherit from Character and initialize their specific attributes, including player direction requests and ghost states.

These classes are used to create the player and ghosts during level initialization.


## 4. Game Initialization and Entity Placement

### Game Initialization (`__init__`)

The `Game` constructor initializes the maze dimensions, player starting position (center), ghost spawn positions (four corners), and default game settings.

It then calls `initialize_level()` to prepare the first level.

### Level Initialization (`initialize_level`)

This method prepares each level by:

- Generating a maze using the predefined seed for the current level.
- Creating the player at the center and four ghosts at the corners.
- Configuring ghost movement parameters according to the level.
- Initializing gums, supergums, and level-specific state.

### Gums Placement (`gums_placement`)

We use BFS through `get_reachable_cells()` to identify all cells accessible from the maze center.

Normal gums are placed in these reachable cells, excluding the player's starting position and the four corners.

A `set` is used to store gum positions without duplicates.

### Supergums Placement (`super_gum`)

Four supergums are placed at the maze corners using the predefined `self.corners` positions.

Their positions are also stored in a `set` to prevent duplicates.

### ayait-ih

## 5. First Visual Prototype (`visual.py`)

To check the maze and the entities on screen, I built a first Pygame prototype that reads the data from `Game` and draws it.
 
### Window and Layout
 
The window is split into two surfaces:
 
| Surface | Content |
|---|---|
| `maze_sur` | The maze, the gums and the characters |
| `sidebar_sur` | The future HUD (score, lives, timer, level) |
 
Their positions are controlled by layout constants (`CELL`, `PADDING`, `GAP`, `SIDEBAR_WIDTH`), so the window size is calculated from the maze size instead of being hard-coded.
 
### Drawing Methods
 
| Method | Responsibility |
|---|---|
| `draw_maze()` | Reads `game.grid` and draws each wall from its bitmask. |
| `draw_42_cells()` | Fills the cells returned by `maze.get_42_cells()` to show the 42 pattern. |
| `draw_gums()` | Draws a small dot in every position of `game.gums`. |
| `draw_supergums()` | Draws a bigger dot in every position of `game.super_gums`. |
| `draw_player()` | Draws the player at its pixel position (`x_pix`, `y_pix`). |
| `draw_ghosts()` | Draws the four ghosts, each with its own color. |
| `draw_maze_side_bar()` | Draws the border of the sidebar panel. |
 
### Wall Drawing
 
Each cell is an integer where every bit is one wall:
 
| Bit | Value | Wall |
|---|---|---|
| North | `1` | top line |
| East | `2` | right line |
| South | `4` | bottom line |
| West | `8` | left line |
 
`cell & side != 0` tells whether a wall exists, then a line is drawn on that side of the cell. A cell is converted to pixels with `col * CELL` and `row * CELL`.
 
### Why a Prototype First
 
- It gave a **visual check** of Moaad's work: maze generation, the 42 pattern, the player at the center, the ghosts in the corners and the gum placement.
- It let us test the maze with the real `Game` data before the menus and scenes existed.
- Simple shapes (circles and lines) were used first, so the logic could be validated before spending time on images.
---
 
## 6. Visual Theme and Assets
 
### Theme Choice
 
We chose an original **ninja / moonlit night** theme: a blue night background, wooden and scroll-style UI elements, and ninja-style characters. All assets are original and do not use any existing franchise.
 
### Assets
 
| Asset | Usage |
|---|---|
| Player sprites (`player1.png`, `player2.png`) | Facing right and facing left |
| Ghost sprites (`ghost1` → `ghost4`) | One image per ghost |
| `gum.png`, `supergum.png` | Gums and supergums |
| Background images | Game scene and menus |
| Buttons, scroll panel, boards, hearts, timer sign | Menus and HUD |
| `Bangers-Regular.ttf` | Font used in the whole game |
 
### Technical Choices
 
- **Image scaling:** every image is resized to the cell size with `smoothscale`, so the sprites fit any maze size.
- **Fallback shapes:** if an image is missing, a simple circle or rectangle is drawn instead, so the game never crashes because of a missing asset.
- **Transparency:** PNG images are loaded with `convert_alpha()` to keep their transparent background, and the background with `convert()` for faster drawing.
---
 
## 7. From Prototype to Game Scene
 
The prototype was then turned into `GameScene`, the first scene of the scene architecture used for the whole UI (menu, instructions, leaderboard, pause, game over, victory).
 
| Prototype (`visual.py`) | Game scene (`scenes/game.py`) |
|---|---|
| Own window and game loop | Uses the window and loop of `App` |
| Fixed window size | Draws on a canvas, then scales it to fit any window |
| Circles and lines | Sprites, with shapes as fallback |
| No input | Arrow keys / WASD sent to `player.request_direction()` |
 
This separation keeps **drawing** in the UI part and **game rules** in `Game`, so both of us could work on our parts at the same time.