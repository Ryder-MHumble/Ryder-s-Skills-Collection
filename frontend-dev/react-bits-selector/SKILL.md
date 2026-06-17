---
name: react-bits-selector
description: Select, configure, and implement the best React Bits animated React components for frontend projects, landing pages, app prototypes, UI modules, text animations, scroll effects, backgrounds, cards, navigation, galleries, cursor/hover effects, and high-polish visual demos. Use when Codex is asked to build or improve a React/Next/Vite frontend and should recommend or integrate React Bits components, including choosing variants, installing dependencies, tuning colors/animation parameters, and copying local component source from the bundled React Bits catalog.
---

# React Bits Selector

Use this skill to choose and implement React Bits components from the bundled local catalog. The goal is not to dump a demo component into a page; the goal is to pick the component that best fits the current UI, then tune it until it feels native to the project.

## Core Workflow

1. Classify the request: target module, interaction type, visual tone, performance budget, framework, TypeScript, Tailwind, and mobile requirements.
2. Search the local catalog:
   ```bash
   "${HERMES_HOME:-$HOME/.hermes}/skills/creative/react-bits-selector"/scripts/find_components.py "<brief>" -n 8
   ```
3. Read the relevant reference before implementing:
   - Broad component choice: `references/selection-guide.md`
   - Full component inventory: `references/component-catalog.md` or `references/component-catalog.json`
   - Prop/color/motion tuning: `references/parameter-playbook.md`
   - Copy/install details: `references/implementation-playbook.md`
4. Select one primary component and at most two supporting components. Avoid unrelated spectacle.
5. Copy the component into the project:
   ```bash
   "${HERMES_HOME:-$HOME/.hermes}/skills/creative/react-bits-selector"/scripts/install_component.py ComponentName --project /path/to/app
   ```
6. Install any missing dependencies printed by the script.
7. Integrate the component into the target UI and tune props/CSS to match the project design system.
8. Validate with the app's build/test command. For visual work, open the local page in Browser when available.

## Variant Rules

- Prefer `TS-TW` for TypeScript + Tailwind projects.
- Prefer `TS-CSS` for TypeScript projects without Tailwind.
- Prefer `JS-TW` for JavaScript + Tailwind projects.
- Prefer `JS-CSS` when the project is JavaScript, CSS-based, or unclear.
- In Next.js App Router, add `"use client"` to copied components that use hooks, DOM APIs, GSAP, Lenis, canvas, WebGL, scroll, or pointer events.

## Selection Discipline

- Choose components by user intent, not by novelty.
- Favor low-dependency components for ordinary production UI.
- Use `three`, `@react-three/*`, `ogl`, `matter-js`, and other heavy dependencies only when 3D, physics, particles, or high-impact visuals are explicitly valuable.
- Do not leave default demo colors, sizes, text, or animation intensity unchanged.
- Add reduced-motion or static fallbacks for prominent continuous animation.
- Keep existing project style and design system unless the user asks for a standalone concept.

## Bundled Resources

- `assets/react-bits/`: Local copy of React Bits component sources and registry variants.
- `references/component-catalog.json`: Machine-readable component index with category, description, variants, dependencies, source paths, props, and keywords.
- `references/component-catalog.md`: Human-readable catalog of all bundled components.
- `scripts/find_components.py`: Ranks components for a UI brief.
- `scripts/install_component.py`: Copies a component variant into a React project and reports dependency commands.

## Minimum Quality Bar

Every React Bits implementation should answer:

- Why this component is the best fit for the requested UI.
- Which props/colors/motion values were tuned for this project.
- Which dependency was added and why.
- How the result was validated.
