# Brief To Motion Plan

Use this reference when the user gives a vague animation idea and expects a polished Remotion result.

## Inputs To Capture

| Input | Default if absent |
| --- | --- |
| Platform | 16:9 horizontal presentation/demo |
| Duration | 20-30 seconds for short story, 6-10 seconds for loop/logo |
| FPS | 30 |
| Language | Match user language |
| Output | MP4 unless transparency or editing handoff requires MOV/PNG sequence |
| Assets | Use procedural shapes unless user supplies brand files |
| Factual claims | Verify or remove; do not invent metrics, customers, or compliance claims |

Ask only when the answer changes the artifact materially: brand assets, exact platform, required facts, or hard delivery constraints.

## Shot Table Format

Create a compact table before coding:

| Time | Beat | Visual action | Scene type | Preferred template | Transition | Evidence frame |
| --- | --- | --- | --- | --- | --- | --- |
| 0-3s | Hook | Main object arrives, headline locks | title / UI | custom Remotion | clean cut | 45 |
| 3-9s | Build | Chat or source cards stagger in | message | `wechat-2d-render` | send pulse | 150 |
| 9-16s | Transformation | Prompt types and agent phases run | agent typer | `claude-typer` concept / Codex typer | camera slide | 330 |
| 16-22s | Resolution | Final reply sends and status holds | message + delivery card | `wechat-2d-render` + custom | receipt lock | 570 |

Keep one idea per beat. If a beat requires more than three simultaneous actions, split it.

## Scene Packet Format

For every row in the shot table, create a scene packet before coding:

```json
{
  "id": "agent-execution",
  "time": "10-20s",
  "storyBeat": "Claude Code receives the decomposed prompt and starts working",
  "sceneType": "agent-typer",
  "template": "claude-typer concept via local Codex typer starter",
  "inputs": ["query prompt", "agent phases", "terminal lines"],
  "dominantAction": "prompt types, then plan/edit/verify phases light up",
  "transitionIn": "camera slide from extracted requirement card",
  "transitionOut": "file card becomes delivery artifact",
  "evidenceFrame": 450
}
```

Scene packets are the handoff contract between idea decomposition and implementation. If a later animation scene cannot point back to a packet, the scene is speculative and should be removed.

## Complexity Ladder

1. **Static composition plus simple entrances**: best for quick product/story shorts.
2. **Data-driven UI motion**: arrays for messages, metrics, panels, steps, and tags.
3. **Reusable component system**: typed props, scene registry, multiple aspect ratios.
4. **Media composition**: external images/video/audio/Lottie, captions, voiceover.
5. **3D or procedural simulation**: React Three Fiber, canvas-like SVG, seeded particles.

Use the lowest level that satisfies the brief. Do not start at level 4 or 5 unless the prompt requires it.

## Multi-Scene Switching

Use explicit scene switches when the subject changes from one medium to another, for example: business chat -> AI requirement extraction -> Claude/Codex execution -> generated artifact -> reply sent. Choose one of these transition types per switch:

- **Send pulse:** a message bubble's send icon expands into the next scene.
- **Card handoff:** a requirement card slides into a prompt box or output card.
- **Camera slide:** the canvas pans from chat to agent console when the workflow moves into development.
- **Receipt lock:** read receipt or delivery status becomes the final CTA.

Do not dissolve through unrelated scenes. The viewer should understand what object or status caused the switch.

## Office Chat Example Plan

| Time | Beat | Visual action | Notes |
| --- | --- | --- | --- |
| 0-3s | Task lands | Leader bubble pops in with urgency pulse | Keep message short and readable. |
| 3-7s | Worker context | Files, meetings, and table cards slide into a cluttered stack | Convey pressure without tiny text. |
| 7-14s | AI assist | AI chip breaks task into data, risks, and reply plan | Use organized stagger and calm color. |
| 14-20s | Human judgment | Worker chooses tone chips and adjusts draft | Show human-in-loop, not autopilot. |
| 20-24s | Reply sent | Final bubble sends and task status changes | Slow down and hold final answer. |

## Agent Automation Example Plan

| Time | Beat | Visual action | Template |
| --- | --- | --- | --- |
| 0-4s | Business request arrives | Business-side chat bubble lands while PM is silent | `wechat-2d-render` |
| 4-9s | AI reads context | Related chat/doc signals snap into a requirement card | custom Remotion UI |
| 9-17s | Query prompt sent | Prompt types into Claude Code/Codex console | `claude-typer` concept / Codex typer |
| 17-25s | Agent develops | Plan, edit, validate, artifact cards run in sequence | Codex typer + custom terminal |
| 25-32s | Result returns | Final result card converts into a sent reply bubble | `wechat-2d-render` + custom delivery |
