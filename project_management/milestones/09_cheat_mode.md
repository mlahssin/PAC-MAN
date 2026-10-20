### mlahssin

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


### ayait-ih


## 4. Cheat Keys (`GameScene.handle_event`)
 
The UI connects the keyboard to the cheat methods of `Game`:
 
| Key | Action | Method called |
|---|---|---|
| `C` | Turn cheat mode on / off | `switch_to_cheat_mode()` / `switch_to_normal_mode()` |
| `F1` | Invincibility | `iron_man()` |
| `F2` | Skip the level | `skip_level()` |
| `F3` | Freeze the ghosts | `ghost_freeze()` |
| `F4` | Add one life | `add_life()` |
| `F5` | Speed boost | `speed_boost()` |
 
`F1` to `F5` only work **while cheat mode is on**. When it is off, these keys do nothing, so a player cannot use a cheat by mistake.
 
**Technical choice:** the UI only reads the keys and calls the methods. Every cheat effect stays in `Game`, as described in section 3.
 
## 5. Freezing the Ghosts in the Game Loop
 
`ghost_freeze()` only sets the flag `ghosts_frozen_active`. The ghosts are moved by `GameScene.update()`, so the UI has to read this flag and skip the ghost movement:
 
```python
if not game.ghosts_frozen_active:
    for ghost in game.ghosts:
        ghost.choose_direction(game.maze, game.player.pos)
        ghost.update(game.maze)
```
 
The ghosts are still **drawn** and collisions are still checked, so a frozen ghost stays visible in place.
 
## 6. Showing the Cheats on Screen
 
| Cheat | What the player sees |
|---|---|
| Cheat mode on | A **CHEAT MODE** label in the sidebar |
| Add life | One more heart in the LIVES board |
| Speed boost | The player crosses the cells twice as fast |
| Freeze | The ghosts stop where they are |
| Skip level | A new maze appears, and the LEVEL board goes up by one |
 
The LIVES board draws one heart per life, so the number of hearts follows `game.lives` and a life added by `F4` is visible.
 
## 7. Issue: Cheat Keys Not Working
 
### Problem
 
After turning cheat mode on with `C`, pressing `F1` to `F5` seemed to do nothing.
 
### Cause
 
Two different causes had to be checked, by adding a `print` of the key name in `handle_event()`:
 
1. **The key never reached the game:** on many keyboards (Mac and laptops), `F1`–`F12` are media keys (brightness, volume…), so the system uses them first. They need `fn` + `F1`.
2. **The key arrived, but the effect was missing:** some cheats only set a flag (for example `ghosts_frozen_active`). Because the game loop is in `GameScene.update()`, the UI must read that flag itself, as shown in section 5.
### Solution
 
- The flags set by the cheats are read in the UI game loop.
- The README and the instructions screen explain the keys, and that `fn` may be needed on some keyboards.