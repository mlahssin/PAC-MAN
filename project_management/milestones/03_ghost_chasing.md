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

