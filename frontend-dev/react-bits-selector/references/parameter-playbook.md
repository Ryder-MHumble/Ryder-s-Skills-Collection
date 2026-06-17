# React Bits Parameter Playbook

React Bits components are configurable. Always inspect the selected component's props in `component-catalog.md`, `component-catalog.json`, or the local source before implementation.

## Global Rules

- Replace demo colors with project tokens or CSS variables.
- Match the host layout: container size, z-index, radius, typography, and spacing should come from the project, not the React Bits demo.
- Tune motion intensity to the surface: hero can be expressive; forms, dashboards, docs, and settings should be restrained.
- Add `prefers-reduced-motion` fallbacks when animation is prominent or continuous.
- Avoid stacking multiple continuous effects in the same viewport unless the user explicitly asks for a high-motion concept.

## Common Prop Families

### Color props
Look for props like `color`, `baseColor`, `textColor`, `backgroundColor`, `particleColors`, `strokeColor`, `gradient`, `from`, `to`, `hue`, `accentColor`.

- Use one coherent palette per page.
- For background components, lower alpha/saturation if content sits above it.
- Keep text contrast AA-friendly when animated text is still meaningful content.

### Motion props
Look for `duration`, `delay`, `speed`, `easing`, `stagger`, `threshold`, `radius`, `intensity`, `amplitude`, `frequency`, `smooth`, `lerp`.

- Hero text reveal: `duration` 0.6-1.4s, stagger subtle, no repeated loop unless purposeful.
- Pointer proximity: tune `radius` to 80-160px desktop; lower for dense UI.
- Ambient backgrounds: reduce speed/intensity 20-50% from demo defaults for production UI.
- Scroll effects: ensure enough section height and test with trackpad and mouse wheel.

### Layout props
Look for `className`, `style`, `width`, `height`, `size`, `gap`, `columns`, `items`, `container`, `itemClassName`.

- Set explicit height for canvas/WebGL/background/scroll components.
- Keep background components `position:absolute; inset:0; pointer-events:none` unless interactive.
- For card components, control card height, content hierarchy, and responsive breakpoints in host CSS.

## Component-Specific Notes

### ScrambledText
- Key props: `radius`, `duration`, `speed`, `scrambleChars`, `className`, `style`.
- Use for AI, terminal, security, or experimental text. Avoid for long body copy or accessibility-critical instructions.
- Keep the original text in DOM, which the component does; do not convert meaningful text to canvas.

### ScrollStack
- Depends on `lenis`; scroll container needs explicit height.
- Key props: `itemDistance`, `itemScale`, `itemStackDistance`, `stackPosition`, `scaleEndPosition`, `baseScale`, `rotationAmount`, `blurAmount`, `useWindowScroll`.
- Use for 3-6 cards. Too many cards makes the interaction feel slow.
- Tune `blurAmount` low (0-1px) unless the stack is decorative.

### TextType / DecryptedText / SplitText
- Use for assistant/chatbot copy, hero headline reveals, onboarding moments.
- Keep typing/decryption delay short; users should not wait for essential content.

### MagicBento / SpotlightCard / BorderGlow
- Use for feature cards and prompt cards.
- Set glow and border colors from brand tokens. Avoid default purple unless brand asks for it.

### WebGL/3D backgrounds
- Use only when the visual is a core deliverable.
- Provide static/gradient fallback for mobile or reduced motion.
- Do not put several WebGL components in the same viewport.
