# Quality Checklist

Use this before delivery.

## Static Checks

- `npm run typecheck` passes if available.
- Remotion package versions match exactly.
- No CSS transitions, CSS animations, wall-clock time, or unseeded randomness drive frame output.
- Assets live in `public/` or use stable URLs with network assumptions stated.
- Copy, colors, scene data, metrics, and CTA are configurable.

## Still-Frame QA

Render at least these frames:

| Frame type | Suggested frame |
| --- | --- |
| Hook readable | 1-2 seconds |
| Main transformation | midpoint |
| Fastest transition | the cut or peak action |
| Final lockup | last 2 seconds |

Check text overflow, contrast, safe area, hidden assets, camera crop, and final CTA.

## C-End Adaptation QA

No crop adaptation by default. For social/C-end previews, platform ratios, thumbnails, and phone-safe exports:

- Use contain/scale-to-fit first: preserve the full source frame and add padding, blur, color, or designed background as needed.
- Do not use center crop, overlay a larger source on a smaller canvas, or resize by changing only the container size when text/UI must remain visible.
- For ffmpeg preview composition, scale the foreground before overlay:

```bash
ffmpeg -y -f lavfi -i color=c=0x0b111d:s=1080x1080:r=30 -i input.mov \
  -filter_complex "[1:v]scale=1080:1080:force_original_aspect_ratio=decrease[fg];[0:v][fg]overlay=(W-w)/2:(H-h)/2:format=auto:shortest=1" \
  -c:v libx264 -pix_fmt yuv420p -movflags +faststart preview.mp4
```

- Verify at least one still from the adapted output itself. Passing source stills is not enough if the handoff file is resized or composited later.

## Render Commands

Use project scripts first. Generic commands:

```bash
npx remotion studio src/index.ts
npx remotion still src/index.ts MotionCanvas out/frame-90.png --frame=90
npx remotion render src/index.ts MotionCanvas out/motion.mp4
```

For transparent overlays, use MOV/ProRes only when the project is configured for alpha.

## Visual Bar

A finished motion piece should have:

- clear story in the first 2 seconds;
- one dominant action per scene;
- readable type at target resolution;
- motion that explains hierarchy or cause-effect;
- a final hold long enough to understand;
- no generic purple fog, random neural dots, or meaningless glow.

## Delivery Note

Report absolute paths for project, stills, and render. If skipped, state the exact validation gap, such as missing dependency install, render time, unavailable asset, or license check.
