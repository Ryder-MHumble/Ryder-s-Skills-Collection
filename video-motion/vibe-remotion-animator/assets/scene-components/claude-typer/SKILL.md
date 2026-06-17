---
name: claude-typer
description: Render a Claude-style prompt typing animation video by calling Remotion CLI against the remote site https://www.laosunwendao.com. Use when the user asks for "做一个 claude 的提示词打字机动画", "做 Claude 打字动画", "创建提示词动画", or similar requests that convert a text prompt into a typing-animation video.
---

# Claude Typer

## Workflow

1. Extract the text that should be typed in the animation as `prompt`.
2. Run:
   - ```bash
    skill_dir="${HERMES_HOME:-$HOME/.hermes}/skills/creative/claude-typer"
    python3 "$skill_dir/scripts/render_claude_typer.py" "$prompt"
    ```

## Parameters

| Parameter | Default | Description |
|---|---|---|
| `prompt` | (required) | Text to animate in the typing animation. |
| `--typingSpeedMs` | `30` | Typing speed in milliseconds per character. 30ms is snappy and readable — the preferred default. Use 60+ for very deliberate demos, 20 for ultra-fast. |
| `--video-width` | `1080` | Video width in pixels. |
| `--video-height` | `1080` | Video height in pixels. |
| `--claude-width` | `880` | Width of the Claude window inside the video. |
| `--fps` | `30` | Output frames per second. |
| `--codec` | `prores` | Video codec (`prores`, `h264`, etc.). |
| `--scale` | `2` | Render scale factor. |
| `--dry-run` | `false` | Print commands only without rendering. |

## Bypassing the Script

When you need props the Python script doesn't expose (like custom `tiltDurationRatio` or `model`), call Remotion CLI directly:

```bash
eval "$(fnm env)"
bunx @remotion/cli render https://www.laosunwendao.com Typer30fps output.mov \
  --fps=30 --codec=prores --scale=2 \
  --prores-profile=4444 --pixel-format=yuva444p10le --image-format=png \
  --props='{"prompt":"Your text","typingSpeedMs":30,"model":"Claude Opus 4.8","videoWidth":1080,"videoHeight":1080,"claudeWidth":880,"tiltStartX":9.2,"tiltStartY":0,"tiltEndX":-2.2,"tiltEndY":10.5,"tiltDurationRatio":1}'
```

See `references/remotion-rendering-notes.md` for full prop list and rendering notes.

## Design DNA

claude-typer belongs to the "instruction → process → result" visualization family. New templates should share this DNA — they must visualize the **flow of sending an instruction and seeing its result**, not generic product demos or feature cards.

## Pitfalls

- **typingSpeedMs must go in --props**: Remotion CLI reads props from `--props` JSON. The script now correctly passes it through `build_props()`, but if calling Remotion CLI directly, don't use `--typingSpeedMs` as a standalone flag — put it inside `--props` JSON.
- **fnm required on this machine**: Always prefix with `eval "$(fnm env)"` or rendering fails with "npx not found".
- **Remote site version vs local CLI**: Version mismatch warning (e.g. site on 4.0.440, CLI on 4.0.473) is benign.
