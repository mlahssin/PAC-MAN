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



