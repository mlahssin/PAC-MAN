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

