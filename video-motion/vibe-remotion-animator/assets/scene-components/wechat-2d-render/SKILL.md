---
name: wechat-2d-render
description: Clone or update https://github.com/sxhzju/wechat-2d and render the default WeChat-style 2D chat motion video with Remotion. Use when users ask for 微信聊天动画, wechat 2d chat render, 微信视频消息动效, or exporting the default demo from the wechat-2d project.
---

# WeChat 2D Render

## Workflow

1. Use `scripts/render_wechat_2d.sh` from this skill.
2. Pass `workspace_dir` as the first argument when the user specifies a folder; otherwise use the current directory.
3. Pass `output_path` as the second argument when the user specifies output; otherwise use `out/wechat-2d-transparent.mov`.
4. Pass a props JSON path as the third argument when the user provides custom Remotion props; otherwise use `shared/project/render-presets/default.json`.
5. Run the script and wait for completion.
6. Return the final absolute output path printed by the script.

## Command

```bash
bash scripts/render_wechat_2d.sh [workspace_dir] [output_path] [props_file]
```

## Installed Skill Resolution

Use the installed skill copy, not the source repo checkout:

```bash
    skill_dir="${HERMES_HOME:-$HOME/.hermes}/skills/creative/wechat-2d-render"
