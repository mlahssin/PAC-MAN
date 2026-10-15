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

## 6. Verification Checklist

- [ ] The player cannot cross walls or leave the maze.
- [ ] Valid directions are accepted; invalid directions are rejected.
- [ ] Blocked turns preserve the current direction.
- [ ] Pixel movement progresses smoothly between cell centers.
- [ ] Grid position changes correctly after a completed move.
- [ ] Reversing halfway through a cell behaves smoothly.

**Scope:** This document covers Mlahssin's backend movement implementation only (`Character`, `Player`, and maze movement validation). Keyboard-event handling, sprite rendering, and other Pygame interface code are excluded. Ghost AI, scoring, collisions, and level progression belong to later milestones.
