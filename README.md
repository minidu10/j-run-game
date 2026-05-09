<div align="center">

# J-Run — Forest Chase

**A man. A forest. A very hungry tiger.**

A 2D side-scrolling endless runner built with **Python + Pygame**. Sprint through a dark forest while a tiger snaps at your heels — leap over logs, slide under low branches, and dash through wide hazards. Survive as long as you can.

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](#)
[![Pygame](https://img.shields.io/badge/pygame-2.5%2B-green)](#)
[![Status](https://img.shields.io/badge/status-playable-brightgreen)](#)

</div>

---

## Play in 60 seconds

```sh
git clone https://github.com/minidu10/j-run-game.git
cd j-run-game
pip install -r requirements.txt
python main.py
```

> **Tip:** if `pip` isn't recognized on Windows, try `py -m pip install -r requirements.txt` and `py main.py`.

---

## Controls

| Action       | Keys                          | When to use                                     |
| ------------ | ----------------------------- | ----------------------------------------------- |
| **Jump**     | `Space` &nbsp;·&nbsp; `W` &nbsp;·&nbsp; `↑` | Clear logs and rocks on the ground.             |
| **Slide**    | `S` &nbsp;·&nbsp; `↓`         | Duck under hanging branches and vines.          |
| **Dash**     | `Shift` &nbsp;·&nbsp; `D`     | Burst through wide hazards (short i-frames).    |
| **Pause**    | `P`                           | Freeze the world for a breather.                |
| **Restart**  | `R`                           | Try again after the tiger catches you.          |
| **Quit**     | `Esc`                         | Leave the forest.                               |

The game is forgiving on input: jumps you press a fraction of a second early still register (jump buffering), and you keep a tiny window to jump just after stepping off a ledge (coyote time).

---

## What you're up against

| Barrier      | Looks like                | Beat it with     |
| ------------ | ------------------------- | ---------------- |
| **Log**      | Long brown trunk on ground | Jump             |
| **Rock**     | Grey jagged boulder       | Jump             |
| **Branch**   | Hanging leafy limb        | Slide            |
| **Vine**     | Hanging cluster of leaves | Slide            |
| **Wide hazard** | Spiked log on the path with a red warning marker | Dash |

Sometimes obstacles spawn in pairs — a low one and a high one in quick succession. You'll have to slide-then-jump or jump-then-slide on a tight clock. As your run goes on, the world speeds up, gaps shrink, and pairs become more frequent.

---

## Survival rules

- The tiger is always behind you. **Every clean obstacle gives you a tiny bit of distance back.**
- Hitting a barrier costs a heart **and** the tiger surges forward. Lose all hearts, or let the tiger close the gap, and it's over.
- Dash has a cooldown. Don't waste it on stuff you could have jumped or slid.
- Watch the speed bar in the top-right — the higher it climbs, the more you should be reading the next two obstacles ahead, not just the one in front of you.

---

## Tech stack

| Layer              | Choice                                      | Why                                                  |
| ------------------ | ------------------------------------------- | ---------------------------------------------------- |
| Language           | **Python 3.10+**                            | Readable, batteries-included.                        |
| Engine             | **Pygame 2.5+**                             | Mature 2D engine, runs on Windows/macOS/Linux.       |
| Rendering          | All shapes drawn procedurally               | Zero image assets — the repo stays tiny.             |
| Audio              | `pygame.mixer` + procedural tones via NumPy | No `.wav` files to ship; falls back to silent mode.  |
| Game loop          | Fixed timestep with `pygame.time.Clock`     | Stable physics independent of monitor refresh rate.  |

---

## Project layout

```
j-run-game/
├── main.py                  # Thin entrypoint: builds Game, calls run()
├── requirements.txt         # pygame
├── README.md
├── .gitignore
└── j_run/                   # Game package
    ├── __init__.py
    ├── settings.py          # Tunable constants (speed, gravity, palette)
    ├── utils.py             # clamp / lerp / aabb helpers
    ├── input_handler.py     # Keyboard mapping (held vs. just-pressed)
    ├── audio.py             # Procedural SFX
    ├── background.py        # Parallax forest layers + ground
    ├── player.py            # Man — run / jump / slide / dash
    ├── tiger.py             # Tiger that chases by gap distance
    ├── obstacle.py          # Barrier types + difficulty-aware spawner
    └── game.py              # Game class, state machine, main loop
```

---

## Tuning the game

All gameplay numbers live in [`j_run/settings.py`](j_run/settings.py). Tweak any of these and play immediately:

| Constant            | What it controls                                |
| ------------------- | ----------------------------------------------- |
| `START_SPEED`       | World scroll speed at the start of a run.       |
| `MAX_SPEED`         | Hard cap on how fast it ever gets.              |
| `SPEED_RAMP`        | How quickly difficulty climbs.                  |
| `GRAVITY`           | Pull on the player. Lower = floatier jumps.     |
| `JUMP_VELOCITY`     | Initial jump impulse.                           |
| `SLIDE_DURATION`    | How long a slide can be held.                   |
| `DASH_DURATION`     | Length of the dash i-frame window.              |
| `DASH_COOLDOWN`     | Seconds before dash is available again.         |
| `PLAYER_LIVES`      | How many hits before game over.                 |
| `TIGER_BASE_GAP`    | Resting distance between tiger and player.      |
| `TIGER_CATCH_GAP`   | If the gap shrinks to this, the tiger wins.     |
| `HIT_TIGER_PUSH`    | How far the tiger surges on a player hit.       |

Want a friendlier game? Lower `SPEED_RAMP` and `HIT_TIGER_PUSH`. Want pain? Raise both.

---

## Troubleshooting

<details>
<summary><b>Nothing happens, or I get a black window</b></summary>

Make sure pygame installed cleanly:

```sh
python -c "import pygame; print(pygame.version.ver)"
```

If that errors, reinstall: `pip install --force-reinstall pygame`.
</details>

<details>
<summary><b>The game runs but is silent</b></summary>

That's fine — audio is optional. The mixer falls back to silent if NumPy is missing or the OS audio device is unavailable. Install NumPy to enable SFX:

```sh
pip install numpy
```
</details>

<details>
<summary><b>Performance feels choppy</b></summary>

Some Linux/Windows setups default to vsync off. The clock targets 60 FPS, but if your refresh rate is lower, lower `FPS` in [`j_run/settings.py`](j_run/settings.py) to match (e.g. 30).
</details>

<details>
<summary><b>Keyboard input feels missed</b></summary>

The window must have focus. Click on the game window first, then press keys. Some terminals (notably IDE-integrated ones) intercept keystrokes — running from a plain terminal helps.
</details>

---

## Roadmap

- [ ] Coins / pickups for bonus score and dash recharge
- [ ] Day/night cycle in the forest
- [ ] Power-ups (shield, magnet)
- [ ] On-screen touch controls for tablets
- [ ] Local high-score persistence (JSON file)
- [ ] Optional pixel-art assets in place of procedural drawing

Have an idea? Open an issue.

---

## Author

Built by **Minidu dhananjana** — [@minidu10](https://github.com/minidu10).
