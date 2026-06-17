# React Bits Selection Guide

Use this guide after reading the user's frontend brief. Pick a small set of components that directly supports the requested module; do not decorate with unrelated effects.

## Selection Heuristic

1. Identify the UI surface: hero, landing section, card grid, gallery, nav, chatbot, dashboard, app shell, background, cursor/hover, or scroll story.
2. Identify the interaction: on-load reveal, hover, pointer proximity, click, scroll, continuous ambient background, carousel/gallery, or stacked cards.
3. Check project constraints: TypeScript, Tailwind, server components, mobile, performance budget, accessibility, and existing design system.
4. Choose one primary React Bits component and at most two supporting components.
5. Prefer low-dependency components unless the brief explicitly needs WebGL/3D/physics.
6. Tune color, scale, speed, intensity, and density to the project; never ship the demo defaults unchanged.

## Intent To Component Families

### Hero / landing headline
- Safer text: `SplitText`, `BlurText`, `TextType`, `ShinyText`, `GradientText`, `TrueFocus`.
- Hacker/AI/decryption: `DecryptedText`, `ScrambledText`, `GlitchText`, `Shuffle`.
- Kinetic/expressive: `RotatingText`, `TextPressure`, `VariableProximity`, `FuzzyText`.
- Supporting reveal: `AnimatedContent`, `FadeContent`, `GradualBlur`.

### Scroll storytelling
- Stacked narrative cards: `ScrollStack`.
- Text reveal while scrolling: `ScrollReveal`, `ScrollFloat`.
- Marquee/velocity text: `ScrollVelocity`, `CurvedLoop`.
- Page section entrance: `AnimatedContent`, `FadeContent`.

### Cards, bento, product modules
- Premium bento/card grid: `MagicBento`, `SpotlightCard`, `BorderGlow`, `GlassSurface`, `GlassIcons`.
- Card movement: `CardSwap`, `Stack`, `BounceCards`, `TiltedCard`, `DecayCard`.
- Profile or people modules: `ProfileCard`, `Lanyard`.
- Counters/stats: `Counter`, optionally with `AnimatedContent`.

### Navigation and app chrome
- Desktop dock / command bar: `Dock`.
- Product nav: `CardNav`, `PillNav`, `GooeyNav`, `StaggeredMenu`, `FlowingMenu`, `BubbleMenu`.
- Folder/file metaphor: `Folder`.

### Media, gallery, portfolio
- Image/gallery: `Masonry`, `Carousel`, `CircularGallery`, `DomeGallery`, `ChromaGrid`.
- Product/model hero: `ModelViewer` only when a real 3D asset exists.
- Poster wall: `FlyingPosters` only when WebGL is acceptable.

### Backgrounds
- Elegant/low-risk: `Aurora`, `SoftAurora`, `Threads`, `Waves`, `LightRays`, `FloatingLines`, `DotGrid`.
- Tech/cyber: `GridScan`, `FaultyTerminal`, `LetterGlitch`, `Hyperspeed`, `DarkVeil`.
- Premium liquid/chrome: `Silk`, `Iridescence`, `LiquidChrome`, `LiquidEther`, `Prism`.
- Particle/space: `Particles`, `Galaxy`, `Orb`, `Balatro`.
- Avoid heavy WebGL backgrounds on mobile unless the user asks for high-impact motion.

### Cursor and hover effects
- Subtle hover: `GlareHover`, `Magnet`, `SpotlightCard`, `StickerPeel`.
- Playful pointer: `BlobCursor`, `SplashCursor`, `GhostCursor`, `TargetCursor`, `PixelTrail`, `ImageTrail`.
- Click feedback: `ClickSpark`.
- Avoid custom cursors on accessibility-critical or mobile-first experiences.

### C-end AI chatbot / consumer app
- Good defaults: `TextType` or `DecryptedText` for assistant copy, `MagicBento` or `SpotlightCard` for prompt cards, `Dock` for bottom nav, `Aurora`/`SoftAurora`/`Threads` for background, `ClickSpark` only if playful.
- Avoid: full-screen heavy WebGL unless the app is a visual concept demo.

### Dashboard / data product
- Good defaults: `Counter`, `AnimatedList`, `SpotlightCard`, `BorderGlow`, `DotGrid`, `GridScan`.
- Keep effects restrained; data clarity wins over spectacle.

## Dependency Budget

- No dependency or CSS-only components are safest.
- `gsap` components are acceptable for text/scroll effects; isolate in client components in Next.js.
- `lenis` is acceptable for scroll experiences like `ScrollStack`; ensure the scroll container has explicit height.
- `motion` is acceptable for UI transitions.
- `three`, `@react-three/*`, `ogl`, `matter-js` are heavy. Use only for explicit 3D, physics, particle, or visual hero requests.

## Variant Choice

- Existing TypeScript + Tailwind: prefer `TS-TW`.
- Existing TypeScript without Tailwind: prefer `TS-CSS`.
- Existing JavaScript + Tailwind: prefer `JS-TW`.
- Existing JavaScript without Tailwind or unclear: prefer `JS-CSS`.
- In Next.js App Router, add `"use client"` to components that access DOM, pointer, scroll, canvas, or animation APIs if not already present.
