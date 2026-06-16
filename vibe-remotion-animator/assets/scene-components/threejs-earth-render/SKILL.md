---
name: threejs-earth-render
description: Clone or update https://github.com/vibe-motion/threejs-earth and render the Three.js Earth route animation with Puppeteer frame capture. Use when users ask for 三维地球航线动画, Three.js Earth, 地球飞线, globe route animation, or exporting an Earth GIF/MP4/PNG sequence.
---

# Three.js Earth Render

## Workflow

1. Use `scripts/render_threejs_earth.py` from this skill.
2. Pass `--workspace` when the user specifies where the source checkout should live; otherwise use the current directory.
3. Pass `--output` when the user specifies a GIF/MP4 path; otherwise use `out/threejs-earth.gif`.
4. For customized routes, edit `threejs-earth/src/routeConfig.js` first and render with `--skip-update` so local edits are preserved.
5. Run the script and wait for completion.
6. Return the final absolute output path printed by the script.

## Command

```bash
python3 scripts/render_threejs_earth.py \
  --workspace "$(pwd)" \
  --output "$(pwd)/out/threejs-earth.gif"
```

## Installed Skill Resolution

Use the installed skill copy, not the source repo checkout:

```bash
    skill_dir="${HERMES_HOME:-$HOME/.hermes}/skills/creative/threejs-earth-render"
