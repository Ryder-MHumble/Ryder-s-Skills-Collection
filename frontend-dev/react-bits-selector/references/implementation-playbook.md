# React Bits Implementation Playbook

## Recommended Workflow

1. Search candidates:
   ```bash
   "${HERMES_HOME:-$HOME/.hermes}/skills/creative/react-bits-selector"/scripts/find_components.py "<brief>" -n 8
   ```
2. Inspect the chosen component in `references/component-catalog.md` or `references/component-catalog.json`.
3. Copy the component into the React app:
   ```bash
   "${HERMES_HOME:-$HOME/.hermes}/skills/creative/react-bits-selector"/scripts/install_component.py ComponentName --project /path/to/app
   ```
4. Install missing dependencies printed by the script.
5. Import the component from `src/components/reactbits/ComponentName/ComponentName` and build the target UI.
6. Tune props and CSS using `references/parameter-playbook.md`.
7. Validate with the project build/test command and, for visual work, open the local page in Browser when available.

## Manual Copy Fallback

If the script cannot be used, copy from:

```text
"${HERMES_HOME:-$HOME/.hermes}/skills/creative/react-bits-selector"/assets/react-bits/src/content/<Category>/<Component>/<Component>.jsx
"${HERMES_HOME:-$HOME/.hermes}/skills/creative/react-bits-selector"/assets/react-bits/src/content/<Category>/<Component>/<Component>.css
```

Variant roots:

- `src/content`: JS + CSS
- `src/tailwind`: JS + Tailwind
- `src/ts-default`: TS + CSS
- `src/ts-tailwind`: TS + Tailwind

## Import Patterns

Default component:

```jsx
import ScrambledText from './components/reactbits/ScrambledText/ScrambledText';
```

Component with named item subcomponent:

```jsx
import ScrollStack, { ScrollStackItem } from './components/reactbits/ScrollStack/ScrollStack';
```

CSS variants usually import their local CSS internally. Keep that import unless the host project requires central CSS bundling.

## Next.js App Router

Many React Bits components use DOM, scroll, pointer, canvas, or animation APIs. When installing into Next.js App Router:

- Put `"use client"` at the top of copied components if they use hooks, DOM APIs, GSAP, Lenis, canvas, or WebGL.
- Import them only from client components.
- Avoid server-rendering browser-only globals.

## Dependency Installation

Use the existing package manager:

- `pnpm add <deps>` if `pnpm-lock.yaml` exists.
- `yarn add <deps>` if `yarn.lock` exists.
- `bun add <deps>` if `bun.lock`/`bun.lockb` exists.
- Otherwise use `npm install <deps>`.

Common dependencies: `gsap`, `motion`, `lenis`, `three`, `@react-three/fiber`, `@react-three/drei`, `ogl`, `matter-js`.

## Integration Quality Bar

- The selected component must solve the requested module; do not add animation for its own sake.
- The final implementation should look native to the project, not like an unmodified React Bits demo.
- Build must pass before final response whenever project setup allows.
- Mention any heavy dependency or browser/performance caveat in the final answer.
