# PAC-MAN — Project Management

## Project objective

Build a playable PAC-MAN game for the 1337 project using the assigned `mazegenerator` package, including maze and entity initialization, player movement, ghost behavior, collectibles, collisions, ten levels, pause/resume, and cheat mode.

## Team organization

| Contributor | Main responsibilities |
|---|---|
| Mlahssin | Python gameplay/backend: maze integration, entity initialization and placement, character movement, ghost AI and states, collectibles and scoring, collisions, level progression, timers, and cheat logic. |
| Ayoub | Pygame visual interface: rendering and assets, game UI, keyboard integration, and interface-related features; configuration and menu work coordinated with the backend. |

These are the primary areas of work, not a claim that every task was performed exclusively by one person.

## Development approach

We divided the backend into ten milestones. For each milestone, the workflow is **implement → review/refine → test → document**. The milestone notes explain the actual code and technical choices, while progress and test evidence are tracked separately.

Collaboration is handled through Git branches and merges into the shared project, with conflicts reviewed before committing and pushing. Generated cache files should not be version-controlled.

## Documentation map

| File | Focus |
|---|---|
| `progress.md` | Milestone status and planned-versus-actual tracking |
| `testing_and_issues.md` | Known issues, resolutions, and verification evidence |
| `milestones/01_maze_entities.md` | Maze setup and entity placement |
| `milestones/02_player_movement.md` | Player movement backend |
| `milestones/03_ghost_chasing.md` | BFS chasing and random decisions |
| `milestones/04_collectibles_scoring.md` | Gum collection and score |
| `milestones/05_ghost_states.md` | Dangerous, edible, and respawning states |
| `milestones/06_collision_handling.md` | Collision rules and resets |
| `milestones/07_level_progression.md` | Levels, timeout, victory |
| `milestones/08_pause_resume.md` | Pause/resume and timer compensation |
| `milestones/09_cheat_mode.md` | Cheat features |
| `milestones/10_backend_quality.md` | Final lint, typing, refactoring, and tests |

## Technical decisions

- **Assigned generator retained:** `Maze` wraps the provided package rather than modifying its implementation.
- **Grid logic + pixel movement:** logical cells govern gameplay; pixel coordinates give smooth transitions.
- **BFS for an unweighted maze:** used for reachability and shortest routes.
- **Occasional random ghost moves:** reduce ghost synchronization on identical BFS routes and moderate difficulty.
- **`time.monotonic()` deadlines:** used for levels, edible mode, and respawning.

## Remaining project-management evidence

Fill in dates and concrete Git commit/PR references from repository history where available. Maintain the test log as checks are executed; do not mark proposed checks as passed before running them.
