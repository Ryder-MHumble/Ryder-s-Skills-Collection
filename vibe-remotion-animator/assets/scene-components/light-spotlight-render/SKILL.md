---
name: light-spotlight-render
description: Generate a swinging spotlight text-reveal HTML animation with configurable text, swing angle, lamp scale, glow, and colors. Use when users ask for 聚光灯扫字动画, spotlight text reveal, light logo reveal, 发光文字揭示动画, or want a reusable HTML animation instead of a static image.
---

# Light Spotlight Render

## Workflow

1. Collect the animation parameters:
   - `label_text`
   - `swing_angle_degrees`
   - `swing_cycle_seconds`
   - `lamp_scale`
   - `glow_opacity`
   - `mask_color`
   - `text_color`
   - `background_color`
   - `video_width`
   - `video_height`
   - optional `output`
2. Resolve the installed skill directory and run `scripts/render_light_spotlight.py`.
3. Return the final absolute HTML path printed by the script.

## Command

```bash
python3 scripts/render_light_spotlight.py \
  --label-text "vibe-motion" \
  --output "out/light-spotlight-vibe-motion.html"
```

## Installed Skill Resolution

Use the installed skill copy, not the source repo checkout:

```bash
    skill_dir="${HERMES_HOME:-$HOME/.hermes}/skills/creative/light-spotlight-render"
