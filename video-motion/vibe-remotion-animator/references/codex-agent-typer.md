# Codex Agent Typer

Use this reference when the user asks for Codex typing animation, prompt-to-agent demo, agent running animation, coding agent workflow video, or a Codex version of a Claude-style typer.

## Design Direction

Do not reuse Claude branding. Build a Codex-specific interface:

- Product identity: `Codex`, `GPT-5 Codex` or the user-specified model label.
- UI: dark command center with prompt input, agent run timeline, terminal logs, file changes, and validation status.
- Logo: procedural Codex mark, such as a geometric C/hex ring with frame-driven orbit, glow, and draw-on progress.
- Motion: typed prompt first, then agent phases light up: plan, edit, run, verify, deliver.

## Starter Command

```bash
python3 "${HERMES_HOME:-$HOME/.hermes}/skills/creative/vibe-remotion-animator"/scripts/create_codex_agent_typer.py \
  --name codex-agent-typer-demo \
  --prompt "帮我生成一个办公聊天动效" \
  --model-label "GPT-5 Codex"
```

Default output root is `"${HERMES_OUTPUT:-$HOME/workspace/hermes-output}/vibe-remotion-animations"/<name>`.

## Visual Beats

| Time | Beat | Visual action |
| --- | --- | --- |
| 0-3s | Codex wakes | Logo ring draws, model chip locks in. |
| 3-7s | Prompt typing | User prompt types into command box with cursor. |
| 7-13s | Agent run | Plan/edit/validate steps activate with terminal lines. |
| 13-18s | Delivery | File cards and final success badge settle. |

## Implementation Rules

- Use Remotion primitives only: `useCurrentFrame`, `interpolate`, `spring`, `Sequence` if needed.
- Keep prompt, model label, terminal lines, phases, and colors in `src/content.ts`.
- Avoid remote render sites; keep this Codex version local and editable.
- Validate with typecheck and still frames before rendering MP4.
