# Milestone 06 — Collision Handling

## Objective
Detect collisions between the player and ghosts and apply the appropriate outcome based on the ghost's state.

## 1. Collision Detection (`detect_collision`)

The method compares the player's pixel coordinates with each ghost's pixel coordinates. A collision occurs when the squared distance between their centers is at most `(20 + 20) ** 2` (a combined radius of 40 pixels).

It returns the first colliding `Ghost`, or `None` when no collision is detected.

## 2. Collision Resolution (`handle_collisions`)

The response depends on the detected ghost's state:

| Ghost state | Result |
|---|---|
| `DANGEROUS` | Unless invincibility is enabled, the player loses one life. |
| `EDIBLE` | The ghost returns to its spawn position, enters `RESPAWNING`, and the player gains 200 points. |
| `RESPAWNING` | No collision effect is applied. |

### Dangerous ghost

When the player is not invincible, one life is deducted. If lives reach zero, `game_over` becomes `True`. Otherwise, the player is reset to the maze center and all ghosts return to their corner positions with their movement and ghost states reset to `DANGEROUS`.

### Edible ghost

The ghost's grid and pixel positions are reset to its original spawn position. Its movement state is cleared, its state becomes `RESPAWNING`, and a 10-second respawn deadline is set. The score increases by 200 points.

The timing and subsequent ghost-state transitions are documented in **Milestone 05 — Ghost States**.

## 3. Implementation Choices

- **Pixel-based detection:** Collisions are checked using the characters' displayed positions rather than requiring them to occupy the same grid cell.
- **Squared distance:** Comparing `dx * dx + dy * dy` avoids calculating a square root.
- **State-dependent handling:** A single collision-resolution method applies different outcomes according to ghost state.

