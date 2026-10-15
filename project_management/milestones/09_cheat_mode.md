# Milestone 09 — Cheat Mode

## Objective

Implement optional cheat features that modify gameplay while cheat mode is enabled.

## 1. Cheat Mode Management

- `switch_to_cheat_mode()` enables cheat mode by setting `self.cheat_mode` to `True`.
- `switch_to_normal_mode()` disables cheat mode and resets invincibility, speed boost, ghost freezing, and the skip-level flag. It also calls `speed_boost()` to restore the player's normal movement speed.

The individual cheat methods check `self.cheat_mode` before applying their effects.

## 2. Available Cheats

| Method | Behavior |
|---|---|
| `iron_man()` | Toggles `self.invincible`, preventing life loss on dangerous-ghost collisions. |
| `add_life()` | Adds one life to `self.lives`. |
| `speed_boost()` | Toggles faster player movement by reducing `frames_per_cell` to half its normal value, with a minimum of `1`. |
| `ghost_freeze()` | Toggles `self.ghosts_frozen_active`, which the gameplay loop uses to skip ghost movement updates. |
| `skip_level()` | Calls `Next_level()` to advance to the next level. |

## 3. Implementation Choices

- **Centralized control:** Cheat flags and their effects are managed by the `Game` class.
- **Reversible toggles:** Invincibility, speed boost, and ghost freezing can be enabled or disabled without changing the normal gameplay algorithms.
- **Speed representation:** A smaller `frames_per_cell` means more pixels traveled per update, so the player moves faster.
- **Normal-mode reset:** Leaving cheat mode restores normal movement speed and disables active cheat flags.