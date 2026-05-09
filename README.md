# J-Run — Forest Chase

A 2D side-scrolling endless runner built with **Python + Pygame**. A man flees through a dense forest while a hungry tiger chases him from behind. Sudden barriers fly toward him — leap over logs, slide under low branches, or dash through wide hazards.

## Controls

| Key | Action |
| --- | --- |
| `Space` / `W` / `↑` | Jump |
| `S` / `↓` | Slide |
| `Shift` / `D` | Dash (short i-frames) |
| `P` | Pause |
| `R` | Restart after game over |
| `Esc` | Quit |

## How to play

- The man auto-runs to the right.
- Three kinds of barriers spawn:
  - **Logs / rocks** — low. **Jump** over them.
  - **Branches / vines** — high. **Slide** under them.
  - **Wide hazards** — too wide to jump or slide. **Dash** through with brief invulnerability.
- Each clean clear scores points; speed ramps up over time.
- Hit a barrier and the tiger closes in. Three hits and the tiger catches you.

## Tech stack

- **Python 3.10+**
- **Pygame 2.5+** — rendering, input, audio mixer
- All graphics are drawn procedurally (no image assets) so the repo stays tiny.

## Run

```sh
# 1. install pygame
pip install -r requirements.txt

# 2. play
python main.py
```

If you prefer a virtual environment:

```sh
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python main.py
```

## Project layout

```
main.py                 — entry point
requirements.txt        — pygame
j_run/
  __init__.py
  settings.py           — screen size, FPS, colors, tuning
  utils.py              — small helpers (clamp, lerp, AABB)
  input_handler.py      — keyboard mapping
  audio.py              — procedural SFX via pygame.mixer
  background.py         — parallax forest layers
  player.py             — man (run / jump / slide / dash)
  tiger.py              — chasing tiger
  obstacle.py           — barriers + spawner
  game.py               — Game class, state machine, main loop
```
