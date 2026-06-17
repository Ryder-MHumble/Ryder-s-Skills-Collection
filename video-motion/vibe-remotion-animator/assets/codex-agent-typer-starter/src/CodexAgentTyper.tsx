import React from 'react';
import {
  AbsoluteFill,
  Easing,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import type {CodexContent} from './content';

const clamp = {
  extrapolateLeft: 'clamp' as const,
  extrapolateRight: 'clamp' as const,
};

const easeOut = Easing.bezier(0.16, 1, 0.3, 1);
const easeInOut = Easing.bezier(0.45, 0, 0.55, 1);

const p = (frame: number, start: number, end: number, easing = easeOut) =>
  interpolate(frame, [start, end], [0, 1], {...clamp, easing});

const visibleText = (text: string, frame: number, start: number, speed = 0.82) => {
  const chars = Math.floor(interpolate(frame, [start, start + text.length * speed], [0, text.length], clamp));
  return text.slice(0, chars);
};

const CodexLogo: React.FC<{color: string}> = ({color}) => {
  const frame = useCurrentFrame();
  const draw = p(frame, 8, 56, easeInOut);
  const spin = frame * 1.5;
  const pulse = 0.84 + Math.sin(frame / 9) * 0.06;

  return (
    <div style={{position: 'relative', width: 112, height: 112, display: 'grid', placeItems: 'center'}}>
      <div style={{position: 'absolute', inset: 0, borderRadius: 32, border: `2px solid ${color}`, opacity: 0.26 + draw * 0.45, transform: `rotate(${spin}deg) scale(${pulse})`}} />
      <div style={{position: 'absolute', inset: 15, borderRadius: 26, background: `radial-gradient(circle, ${color}44, transparent 68%)`, filter: 'blur(1px)', opacity: draw}} />
      <svg width="88" height="88" viewBox="0 0 88 88" style={{position: 'relative', overflow: 'visible'}}>
        <path
          d="M57 20 L31 20 L18 44 L31 68 L57 68"
          fill="none"
          stroke={color}
          strokeWidth="8"
          strokeLinecap="round"
          strokeLinejoin="round"
          pathLength="1"
          strokeDasharray="1"
          strokeDashoffset={1 - draw}
        />
        <path
          d="M56 32 L42 32 C34 32 29 37 29 44 C29 51 34 56 42 56 L56 56"
          fill="none"
          stroke="#EAF2FF"
          strokeWidth="6"
          strokeLinecap="round"
          pathLength="1"
          strokeDasharray="1"
          strokeDashoffset={1 - Math.max(0, draw - 0.22) / 0.78}
        />
      </svg>
    </div>
  );
};

const PhaseList: React.FC<{content: CodexContent}> = ({content}) => {
  const frame = useCurrentFrame();
  return (
    <div style={{display: 'grid', gap: 14}}>
      {content.phases.map((phase, index) => {
        const start = 214 + index * 42;
        const active = p(frame, start, start + 18);
        const done = frame > start + 36;
        return (
          <div key={phase} style={{display: 'grid', gridTemplateColumns: '48px 1fr 84px', alignItems: 'center', gap: 16, padding: '14px 16px', borderRadius: 18, background: done ? 'rgba(98,230,167,0.13)' : 'rgba(255,255,255,0.055)', opacity: interpolate(frame, [start - 8, start + 10], [0.35, 1], clamp), transform: `translateX(${interpolate(active, [0, 1], [24, 0])}px)`}}>
            <div style={{width: 44, height: 44, borderRadius: 15, background: done ? content.colors.success : content.colors.codex, color: '#031B18', display: 'grid', placeItems: 'center', fontWeight: 950, fontSize: 22}}>{done ? '✓' : index + 1}</div>
            <div style={{fontSize: 27, color: content.colors.ink, fontWeight: 900}}>{phase}</div>
            <div style={{height: 8, borderRadius: 999, background: 'rgba(255,255,255,0.10)', overflow: 'hidden'}}>
              <div style={{height: '100%', width: `${interpolate(frame, [start, start + 34], [0, 100], clamp)}%`, background: done ? content.colors.success : content.colors.codex, borderRadius: 999}} />
            </div>
          </div>
        );
      })}
    </div>
  );
};

const Terminal: React.FC<{content: CodexContent}> = ({content}) => {
  const frame = useCurrentFrame();
  return (
    <div style={{borderRadius: 24, background: '#05080E', border: '1px solid rgba(255,255,255,0.10)', padding: 22, fontFamily: 'Menlo, SFMono-Regular, monospace', minHeight: 238}}>
      {content.terminalLines.map((line, index) => {
        const start = 220 + index * 36;
        const shown = visibleText(line, frame, start, 0.65);
        return (
          <div key={line} style={{height: 32, color: index === 0 ? content.colors.codex : content.colors.ink, opacity: interpolate(frame, [start, start + 12], [0, 1], clamp), fontSize: 19}}>
            {shown}
          </div>
        );
      })}
    </div>
  );
};

const FileCards: React.FC<{content: CodexContent}> = ({content}) => {
  const frame = useCurrentFrame();
  return (
    <div style={{display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16}}>
      {content.files.map((file, index) => {
        const local = frame - (394 + index * 16);
        const s = spring({frame: local, fps: 30, config: {damping: 17, stiffness: 125}});
        return (
          <div key={file} style={{borderRadius: 20, background: content.colors.panel2, color: '#172033', padding: 18, opacity: interpolate(local, [0, 14], [0, 1], clamp), transform: `translateY(${interpolate(s, [0, 1], [34, 0])}px) scale(${interpolate(s, [0, 1], [0.94, 1])})`}}>
            <div style={{fontSize: 15, color: '#617084', fontWeight: 900, marginBottom: 12}}>UPDATED</div>
            <div style={{fontSize: 21, fontWeight: 950, lineHeight: 1.18}}>{file}</div>
          </div>
        );
      })}
    </div>
  );
};

export const CodexAgentTyper: React.FC<CodexContent> = (content) => {
  const frame = useCurrentFrame();
  const {width, height, fps, durationInFrames} = useVideoConfig();
  const isVertical = height > width;
  const pad = isVertical ? 58 : 82;
  const hero = spring({frame, fps, config: {damping: 18, stiffness: 100}});
  const promptStart = 84;
  const promptText = visibleText(content.prompt, frame, promptStart, 0.72);
  const cursorOn = Math.floor(frame / 12) % 2 === 0;
  const final = p(frame, durationInFrames - 92, durationInFrames - 34);

  return (
    <AbsoluteFill style={{background: content.colors.bg, color: content.colors.ink, fontFamily: 'Avenir Next, DIN Alternate, PingFang SC, sans-serif', overflow: 'hidden'}}>
      <div style={{position: 'absolute', inset: 0, backgroundImage: 'radial-gradient(circle at 20% 12%, rgba(38,215,184,0.22), transparent 30%), radial-gradient(circle at 88% 80%, rgba(47,107,255,0.22), transparent 32%), linear-gradient(rgba(255,255,255,0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.04) 1px, transparent 1px)', backgroundSize: 'auto, auto, 58px 58px, 58px 58px'}} />

      <div style={{position: 'absolute', left: pad, right: pad, top: 54, display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
        <div style={{display: 'flex', alignItems: 'center', gap: 26, opacity: interpolate(frame, [0, 20], [0, 1], clamp), transform: `translateY(${interpolate(hero, [0, 1], [32, 0])}px)`}}>
          <CodexLogo color={content.colors.codex} />
          <div>
            <div style={{fontSize: isVertical ? 52 : 72, fontWeight: 950, letterSpacing: -2}}>{content.title}</div>
            <div style={{fontSize: 25, color: content.colors.muted, marginTop: 8}}>{content.subtitle}</div>
          </div>
        </div>
        <div style={{display: 'grid', gap: 10, justifyItems: 'end'}}>
          <div style={{border: `1px solid ${content.colors.codex}55`, background: `${content.colors.codex}16`, borderRadius: 999, padding: '12px 20px', color: content.colors.ink, fontSize: 21, fontWeight: 900}}>{content.modelLabel}</div>
          <div style={{fontSize: 18, color: content.colors.muted}}>Codex UI · local Remotion</div>
        </div>
      </div>

      <div style={{position: 'absolute', left: pad, right: pad, top: 212, bottom: 96, display: 'grid', gridTemplateColumns: isVertical ? '1fr' : '1fr 0.92fr', gap: 28}}>
        <div style={{borderRadius: 34, background: content.colors.panel, border: '1px solid rgba(255,255,255,0.10)', padding: 30, display: 'grid', gridTemplateRows: 'auto 1fr auto', gap: 24, boxShadow: '0 34px 90px rgba(0,0,0,0.38)'}}>
          <div style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between'}}>
            <div style={{fontSize: 22, color: content.colors.muted, fontWeight: 900}}>Prompt</div>
            <div style={{fontSize: 18, color: content.colors.codex, fontWeight: 900}}>agent mode</div>
          </div>
          <div style={{borderRadius: 26, background: '#060A12', border: '1px solid rgba(255,255,255,0.10)', padding: 28, fontSize: 35, lineHeight: 1.28, fontWeight: 850}}>
            <span style={{color: content.colors.codex}}>› </span>{promptText}<span style={{opacity: cursorOn ? 1 : 0, color: content.colors.codex}}>▍</span>
          </div>
          <Terminal content={content} />
        </div>

        <div style={{display: 'grid', gridTemplateRows: '1fr auto', gap: 24}}>
          <div style={{borderRadius: 34, background: 'rgba(255,255,255,0.075)', border: '1px solid rgba(255,255,255,0.10)', padding: 28, boxShadow: '0 34px 90px rgba(0,0,0,0.28)'}}>
            <div style={{fontSize: 22, color: content.colors.muted, fontWeight: 900, marginBottom: 22}}>Agent run</div>
            <PhaseList content={content} />
          </div>
          <FileCards content={content} />
        </div>
      </div>

      <div style={{position: 'absolute', left: pad, right: pad, bottom: 28, height: 46, display: 'flex', alignItems: 'center', justifyContent: 'space-between', opacity: 0.92}}>
        <div style={{height: 8, flex: 1, borderRadius: 999, background: 'rgba(255,255,255,0.10)', overflow: 'hidden'}}>
          <div style={{height: '100%', width: `${interpolate(frame, [0, durationInFrames - 1], [0, 100], clamp)}%`, background: `linear-gradient(90deg, ${content.colors.codex}, ${content.colors.success})`}} />
        </div>
        <div style={{marginLeft: 24, fontSize: 20, color: content.colors.muted, fontWeight: 800}}>deterministic frames</div>
      </div>

      <div style={{position: 'absolute', right: pad, bottom: 88, borderRadius: 24, background: content.colors.success, color: '#042318', padding: '18px 24px', fontSize: 28, fontWeight: 950, opacity: final, transform: `translateY(${interpolate(final, [0, 1], [60, 0])}px)`}}>
        Done · ready to review
      </div>
    </AbsoluteFill>
  );
};
