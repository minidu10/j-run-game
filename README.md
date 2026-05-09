# J-Run — Forest Chase

A 2D side-scrolling endless runner. A man flees through a dense forest while a hungry tiger chases him from behind. Sudden barriers fly toward him — leap over logs, slide under low branches, or dash sideways past hazards.

Pure HTML5 Canvas + vanilla JavaScript. No build step. Open `index.html` in a browser and play.

## Controls

| Key | Action |
| --- | --- |
| `Space` / `W` / `↑` | Jump |
| `S` / `↓` | Slide |
| `Shift` / `D` | Dash (short i-frames) |
| `P` | Pause |
| `R` | Restart after game over |

## How to play

- The man auto-runs to the right.
- Three kinds of barriers spawn from the right edge:
  - **Logs / rocks** — low. **Jump** over them.
  - **Branches / vines** — high. **Slide** under them.
  - **Lateral hazards** — wide. **Dash** through with brief invulnerability.
- Each clean clear scores you points; speed ramps up over time.
- Hit a barrier and the tiger closes in. Three hits and the tiger catches you.

## Tech stack

- **HTML5 Canvas 2D** — rendering
- **Vanilla ES Modules** — zero-dep, zero-build
- **requestAnimationFrame loop** — fixed-timestep update, interpolated render
- **Web Audio API** — minimal SFX (procedural)

## Run locally

Just open `index.html` in any modern browser. Or serve the folder:

```sh
npx serve .
# or
python -m http.server 8000
```

Then visit `http://localhost:8000`.

## Deploy to GitHub Pages

Push to `main` and enable Pages from the repo settings (root, `main` branch). The game runs as a static site.

## Project layout

```
index.html        — entry point + canvas
style.css         — page chrome + HUD
src/
  game.js         — game class, state machine, main loop
  player.js       — man character (run / jump / slide / dash)
  tiger.js        — chasing tiger AI
  obstacle.js     — barrier types & spawning
  background.js   — parallax forest layers
  input.js        — keyboard input
  audio.js        — Web Audio SFX
  utils.js        — shared helpers (rng, AABB, lerp)
```
