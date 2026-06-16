# Remotion Rendering Notes (claude-typer)

Session-validated rendering notes from actual use.

## Rendering Architecture

claude-typer renders against a **remote Remotion serve URL**, not a local project:
- Serve URL: `https://www.laosunwendao.com`
- Composition: `Typer30fps`
- No local Remotion project clone needed — just `@remotion/cli` + network access

## Runner Priority (script auto-detects)

1. `bunx @remotion/cli` (preferred if bunx available)
2. `npx -y -p @remotion/cli@4.0.440 -p @remotion/tailwind-v4@4.0.440 remotion` (fallback)

Both require Node.js in PATH. On macOS with fnm, run `eval "$(fnm env)"` before executing the script.

## Default Output

| Parameter | Value |
|---|---|
| Resolution | 1080×1080 |
| FPS | 30 |
| Codec | ProRes 4444 |
| Pixel format | yuva444p10le (transparent alpha) |
| Image format | PNG (frame capture) |
| Scale | 2x (retina) |
| Concurrency | 1 (for stability) |
| Timeout | 300s (5 minutes) |
| Default output | `<prompt>.mov` in current directory |

## Chrome Auto-Detection

The script auto-detects Chrome/Chromium on macOS at:
- `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
- `/Applications/Chromium.app/Contents/MacOS/Chromium`

And passes `--browser-executable` to Remotion. No manual configuration needed.

## Session Examples

### Basic (2026-06-07)

```bash
cd ~/workspace/hermes-output/claude-typer
eval "$(fnm env)"
python3 ~/.hermes/skills/creative/claude-typer/scripts/render_claude_typer.py "Ryder"
```

Result: `Ryder.mov` (8.2 MB, 41 frames at 30fps). Rendered in ~30s.

### Custom speed + model via direct Remotion CLI (2026-06-07)

When the Python script's arg parsing doesn't cover what you need, call Remotion CLI directly:

```bash
eval "$(fnm env)"
bunx @remotion/cli render \
  https://www.laosunwendao.com \
  Typer30fps \
  output.mov \
  --fps=30 --codec=prores --scale=2 \
  --prores-profile=4444 --pixel-format=yuva444p10le --image-format=png \
  --props='{"prompt":"Your text here","typingSpeedMs":60,"model":"Claude Opus 4.8","videoWidth":1080,"videoHeight":1080,"claudeWidth":880,"tiltStartX":9.2,"tiltStartY":0,"tiltEndX":-2.2,"tiltEndY":10.5,"tiltDurationRatio":1}'
```

## Composition Props

| Prop | Default | Description |
|---|---|---|
| `prompt` | (required) | Text to animate |
| `typingSpeedMs` | 30 | Typing speed per character (ms). 30ms is snappy and readable — the preferred default. |
| `model` | "Claude Opus 4.8" | Model name displayed in animation |
| `videoWidth` | 1080 | Canvas width |
| `videoHeight` | 1080 | Canvas height |
| `claudeWidth` | 880 | Claude window width in animation |
| `tiltStartX` / `tiltStartY` | 9.2 / 0 | 3D tilt start angle |
| `tiltEndX` / `tiltEndY` | -2.2 / 10.5 | 3D tilt end angle |
| `tiltDurationRatio` | 1 | Tilt animation duration ratio |

## Pitfalls

1. **typingSpeedMs must go in --props, not as a standalone flag**: The Remotion CLI only reads `typingSpeedMs` from `--props` JSON. Passing `--typingSpeedMs 60` as a standalone CLI arg does NOT override the prop value. Always pass it inside `--props`.
2. **fnm required on this machine**: `npx`/`bunx` are not in the default PATH. Always prefix with `eval "$(fnm env)"`.
3. **Version mismatch warning is benign**: Remote site bundled with `4.0.440`, local renderer may be `4.0.473+`. Warning only, no block.
4. **Long prompts = long render**: ProRes 4444 at 1080x1080 ≈ 6-8 MB per second of video.
