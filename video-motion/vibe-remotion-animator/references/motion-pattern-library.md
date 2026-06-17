# Motion Pattern Library

Use this reference to map a creative request to reusable Remotion patterns.

## Chat And Messaging

Best for enterprise chat, AI assistant, social comments, support conversations, and task assignment scenes.

- Data model: `messages = [{speaker, role, text, at, tone, status}]`.
- Entrance: bubble `spring()` scale from 0.96 to 1 plus y from 24 to 0.
- Urgency: one or two frame-driven pulses, not constant shake.
- Typing: string slicing; never per-character opacity for long text.
- AI assist: convert clutter into structured chips; use calm, slower stagger.
- Human-in-loop: show choice chips, cursor confirmation, or edited draft before send.

## Kinetic Typography

Best for short explainers, launch hooks, manifestos, quotes, and title cards.

- Split text into semantic phrases, not individual letters by default.
- Use one dominant motion vocabulary: smash, slide, mask reveal, highlighter, or typewriter.
- Keep text within safe areas; rewrite long copy rather than shrinking it.
- Use `Sequence` for phrase timing and a shared normalized progress for opacity, y, scale, and blur.

## Data And Dashboard Motion

Best for metrics, roadmaps, OKRs, market sizing, experiment reports, and AI insight cards.

- Start with real labels and values; do not fake precision.
- Animate from structure to insight: axes/cards first, values second, conclusion last.
- Tie chart masks to normalized progress. Keep labels visible at evidence frames.
- Use no more than 3 metrics on vertical and 5 on horizontal unless the brief is dense by design.

## Logo And Brand Motion

Best for logo reveals, splash screens, loading states, and brand intros.

- If the input is raster, vectorize or simplify first. Animate semantic parts, not noisy traced pixels.
- Land exactly on the approved final mark.
- Common choreography: draw-on, split-fill, orbit-and-lock, part assembly, mask sweep, or material wipe.
- For transparent handoff, render ProRes 4444 MOV or PNG sequence.

## UI Walkthroughs

Best for product demos, onboarding, workflow explainers, and SaaS feature reveals.

- Treat panels, cards, cursors, tooltips, and data rows as actors with stable IDs.
- Use camera moves only to clarify focus; do not zoom constantly.
- Replace unreadable real UI text with faithful simplified UI when the video is about a concept.
- Show cause and effect: click, system response, confirmation.

## Looping Systems

Best for tickers, carousels, photo walls, route loops, clocks, and ambient backgrounds.

- Duplicate domains (`[...items, ...items]`) and translate to `-50%` for seamless reset.
- Confirm first and last frames match visually.
- Keep loop duration an integer number of seconds when exporting GIFs.
- Use modular arithmetic from `frame` for spinners and progress sweeps.

## Lottie And Asset Composition

Best when the user supplies a Lottie, icon pack, illustration, or screenshot.

- Use supplied assets as actors inside a larger scene, not as the whole design unless requested.
- For Lottie, load JSON with Remotion loading primitives and animate its wrapper transform/opacity.
- Normalize asset resolution and aspect ratio before render.

## Audio, Captions, And Voiceover

Best for narrated videos, music-driven visuals, subtitles, and explainers.

- Lock the script and audio before final timing.
- Use captions as data with start/end frames.
- Keep background music below speech; avoid busy motion behind subtitles.
- If audio visualization is needed, derive bars or waves from analyzed audio data, not random values.

## Transitions

Use transitions only when they communicate a cut:

- Fade: time passage or calmer section change.
- Slide: product panel or workflow handoff.
- Wipe: data reveal or compare/contrast.
- Light leak/glitch: brand flavor, not default decoration.

If a cut is already clear, prefer a clean cut with a sound or small overlay accent.
