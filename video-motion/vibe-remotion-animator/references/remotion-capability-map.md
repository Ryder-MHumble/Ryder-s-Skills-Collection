# Remotion Capability Map

Use this reference to select Remotion APIs and decide when to load official docs. Check live docs/package versions for production because Remotion updates frequently.

## Core Mental Model

A Remotion video is a React composition rendered at a specific frame. Components should be pure functions of frame, props, and assets.

| Need | API or package | Notes |
| --- | --- | --- |
| Register renderable video | `Composition` | Define id, dimensions, fps, duration, default props, optional schema. |
| Current frame | `useCurrentFrame()` | Inside `Sequence`, frame is local to the sequence. |
| Video config | `useVideoConfig()` | Read width, height, fps, duration. |
| Numeric animation | `interpolate()` | Use clamped ranges and Bezier easing for precision. |
| Organic arrivals | `spring()` | Good for pop, settle, and physical arrival. Tune damping/stiffness. |
| Timeline placement | `Sequence`, `Series` | Use `Series` for sequential scenes; `Sequence` for overlays and stagger. |
| Scene transitions | `@remotion/transitions` | Add only when cuts need a designed transition. |
| Static assets | `staticFile()`, `Img` | Put files under `public/`; use `Img` instead of raw `img`. |
| Audio/video | `Audio`, `Video`, `OffthreadVideo` | Finalize audio before locking captions and beat timing. |
| Lottie | `@remotion/lottie` | Load with `delayRender()` and `continueRender()`. |
| Parameter UI | `zod`, `@remotion/zod-types` | Make text/colors/scenes editable through schemas. |
| 3D | React Three Fiber / Three.js | Keep camera and simulation deterministic per frame. |
| Rendering | Remotion CLI or SSR | Use local CLI for prototypes, SSR/Lambda for scale. |

## Official Docs To Consult

- Overview: https://www.remotion.dev/docs/
- Fundamentals: https://www.remotion.dev/docs/the-fundamentals
- Animating properties: https://www.remotion.dev/docs/animating-properties
- `useCurrentFrame()`: https://www.remotion.dev/docs/use-current-frame
- `interpolate()`: https://www.remotion.dev/docs/interpolate
- `spring()`: https://www.remotion.dev/docs/spring
- `Sequence`: https://www.remotion.dev/docs/sequence
- `Series`: https://www.remotion.dev/docs/series
- Rendering: https://www.remotion.dev/docs/render
- Player: https://www.remotion.dev/docs/player
- Input props and schemas: https://www.remotion.dev/docs/schemas
- AI skills: https://www.remotion.dev/docs/ai/skills
- License: https://www.remotion.dev/docs/license

## Version Rule

Before creating a new project, check the current package version:

```bash
npm view remotion version
```

Pin `remotion`, `@remotion/cli`, and all `@remotion/*` packages to the same version unless the project already has a working version set.

## Determinism Rules

- No CSS transitions, CSS animations, timers, `Date.now()`, or mutable frame cursors.
- Seed procedural randomness from stable inputs or precompute arrays.
- Keep async asset loading behind Remotion-supported loading primitives.
- Render frames may run in parallel and out of order; every frame must stand alone.
