# PAC-MAN — Progress Tracking

## Tracking method

We organize backend work into ten milestones and document the implementation separately in `milestones/`. The table below reflects our discussions and reviewed code; **"Implemented" means code has been shared/reviewed, not that all acceptance tests passed**.

| # | Backend milestone | Implementation status | Documentation status | Final verification |
|---|---|---|---|---|
| 01 | Maze and entity placement | Implemented | Drafted/reviewed | Spawn reachability across seeds pending confirmation |
| 02 | Player movement | Implemented | Drafted/reviewed | Full movement regression test not recorded |
| 03 | Ghost chasing | Implemented | Drafted/reviewed | Repeatability and synchronization tests not recorded |
| 04 | Collectibles and scoring | Implemented | Drafted/reviewed | Full test evidence not recorded |
| 05 | Ghost states | Implemented | Drafted/reviewed | Timer/state-transition test evidence not recorded |
| 06 | Collision handling | Implemented | Drafted | Regression evidence not recorded |
| 07 | Level progression | Implemented | Drafted | User reported Levels 1–10 functional; record reproducible tests |
| 08 | Pause/resume | Implemented | Drafted | Timer compensation edge tests not recorded |
| 09 | Cheat mode | Implemented | Drafted | Feature-by-feature regression tests not recorded |
| 10 | Backend quality | In progress | To complete | `flake8`, `mypy`, types, docstrings and final tests pending |

## Planned versus actual progress

The intended sequence follows milestones 01 through 10. Work on UI integration, game behavior, and bug fixes also occurred iteratively; the actual chronological order of every feature has not been verified from Git history.

| Evidence to add | Source | Status |
|---|---|---|
| Planned date for each milestone | Team plan / board | Not provided |
| Actual start and completion dates | Git history / team notes | Not yet compiled |
| Commit or PR demonstrating each feature | Git log / pull requests | Not yet linked |
| Test result / acceptance status | `testing_and_issues.md` and test output | Partially documented |
| Ayoub's UI and configuration milestones | Team member's own task tracking | To integrate |
