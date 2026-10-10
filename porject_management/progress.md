# Pac-Man — Project Progress

Updated: 10 October 2026

## Team responsibilities

- mlahssin: maze integration and game logic.
- Ayoub: graphics, keyboard input, configuration, menus,
  highscores and packaging.
- Both: integration, reviews, decisions and documentation.

## Milestone 0 — Shared foundation

Status: mlahssin's coding preparation completed;
shared setup and agreement pending.

### Progress

- [x] MazeGenerator import successful.
- [x] Character, Player and Ghost skeletons reviewed.
- [x] Correct direction mapping implemented in maze.py.
- [x] Ghost-state constants defined.
- [x] Coordinate and timing conventions documented.
- [ ] Confirm DANGEROUS constant usage in the Ghost constructor.
- [ ] Agree on the engine/UI interface with Ayoub.
- [ ] Verify the project skeleton on both machines.
- [ ] Complete the initial README, Makefile and .gitignore.
- [ ] Ayoub: verify a basic graphics window.
- [ ] Ayoub: draft configuration and screen flow.
- [ ] Ayoub: choose a platform and try packaging early.

### Coordinates

- Positions use immutable integer tuples: (x, y).
- Access the maze grid using grid[y][x].
- (0, 0) is the top-left cell.
- x increases to the right.
- y increases downward.

### Directions

Direction names use lowercase strings.

Each direction contains:
(dx, dy, wall_mask, opposite_wall_mask).

| Direction | dx | dy | Wall mask | Opposite mask |
|-----------|----|----|-----------|---------------|
| up        | 0  | -1 | 1         | 4             |
| right     | 1  | 0  | 2         | 8             |
| down      | 0  | 1  | 4         | 1             |
| left      | -1 | 0  | 8         | 2             |

- A nonzero cell_value & wall_mask means a wall exists.
- Maze checks walls and boundaries.
- The assigned maze-generator package remains unchanged.

### Movement and timing

These are planned conventions; movement is not implemented yet.

- speed: cells per second; must be positive.
- move_interval: seconds per step, calculated as 1 / speed.
- time_since_last_move: accumulated movement time; starts at 0.0.
- dt: elapsed gameplay seconds supplied by the game loop.
- Character.update(dt, maze) will handle movement.
- Player and Ghost inherit update().
- Direction selection happens separately from movement.
- Pause must freeze movement and gameplay timers.
- If speed changes, move_interval must be recalculated.

### Player skeleton

- direction: current movement direction.
- requested_direction: direction requested by the user.
- request_direction(direction): will store valid input.
- choose_direction(maze): will apply a requested turn when legal.
- The engine will not read the keyboard directly.

### Ghost skeleton

- pos: current position.
- spawn_pos: saved initial corner position.
- DANGEROUS: ghost can hurt the player.
- EDIBLE: player can eat the ghost.
- RESPAWNING: ghost waits and cannot move.
- respawn_time_remaining: seconds before returning to spawn.
- choose_direction(maze, player_pos): will choose a direction.
- Level will manage the respawn countdown.

## Milestone 1 — Maze integration

Owner: mlahssin.
Status: core adapter implemented; remaining work listed below.

### Implemented

- [x] Created a Maze adapter around the assigned MazeGenerator.
- [x] Passed width, height, seed and perfect=False to generation.
- [x] Exposed grid, width and height.
- [x] Implemented is_inside(pos).
- [x] Implemented can_move(pos, direction).
- [x] Checked both sides of a shared wall before allowing movement.
- [x] Returned False for invalid directions.
- [x] Implemented get_neighbors(pos).
- [x] Implemented get_reachable_cells(start) using BFS.
- [x] Used a visited set to prevent repeated exploration.
- [x] Returned an empty set for outside or fully blocked starts.
- [x] Implemented validate_spawns().
- [x] Added integer and minimum-size dimension validation.
- [ ] Confirm seed validation is integrated into the constructor.

### Verified results

Results were reported by mlahssin from local execution.

| Check | Actual result | Status |
|-------|---------------|--------|
| 15 × 15, seed 42: centre and corners connected | True | Passed |
| 20 × 20, seed 42: spawn validation | False | Invalid layout detected |
| 20 × 20 centre cell value | 15 | Fully blocked |
| Reachability from the blocked centre | set() | Passed |
| Move above the top boundary | False | Passed |
| Move beyond the left boundary | False | Passed |
| Move from an outside starting position | False | Passed |
| Unknown direction: diagonal | False | Passed |
| 15 × 15 cell (0, 0) value | 11 | Up, Right and Left walls |
| Move Right from that cell | False | Passed |
| Move Down from that cell | True | Passed |

### Proposed MVP policy

Not yet applied in the application.

- Start with the verified 15 × 15 layout.
- Accept a layout only when spawn validation succeeds.
- Reject invalid layouts with a clear message.
- Validate later randomly generated layouts too.
- Do not modify the external generator to unblock the centre.

### Remaining work

- [ ] Apply the invalid-spawn policy.
- [ ] Define supported dimensions and an upper size limit.
- [ ] Handle generation failures without a traceback.
- [ ] Verify invalid dimensions and seeds.
- [ ] Verify repeated generation with the fixed seed.
- [ ] Move standalone checks behind a main guard or into a test file.
- [ ] Complete formatting, type hints and docstrings.
- [ ] Ayoub: render the generated walls and corridors.
- [ ] Verify integration on both machines.

Generation-error handling was explicitly deferred by mlahssin.

## Agreement with Ayoub

Status: pending; shared work resumes when Ayoub is available.

- [ ] Agree on coordinates and lowercase direction names.
- [ ] Agree on timing units and pause behaviour.
- [ ] Define engine methods called by the application.
- [ ] Define game state exposed to the UI.
- [ ] Record the agreement date and any changes.

## Open decisions and blockers

- Graphics library: not recorded.
- Supported maze dimensions: not finalized.
- Invalid-spawn policy: proposed, not applied.
- Timeout behaviour: not agreed.
- Edible duration and respawn delay: not agreed.
- Generation-error handling: deferred.
- Shared interface and both-machine checks: pending.
- Ghost algorithms: not implemented.

## Next — Milestone 2

First task: implement Player.request_direction(direction).

- Accept known direction strings.
- Ignore invalid input.
- Store valid input in requested_direction.
- Do not move the player or check walls in this method.

Then implement legal direction selection and timed movement.

## Verification limits

The reviewed code and reported checks support the results above.
Full gameplay, graphics, packaging and both-machine execution
have not been verified.

Milestones 0 and 1 remain open for their pending shared,
validation and error-handling tasks.



## Decision — Graphics library

Date: 10 October 2026
Agreed by: mlahssin and Ayoub
Choice: Pygame.

- Ayoub handles the window, keyboard input, rendering and frame timing.
- mlahssin keeps the game engine independent of Pygame.
- Elapsed time passed to the engine uses seconds.

Status: library selected; window setup on both machines
has not yet been verified.