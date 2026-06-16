import React from 'react';
import {
  AbsoluteFill,
  Easing,
  interpolate,
  Sequence,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import type {ChatMessage, MotionBrief} from './content';

const clamp = {
  extrapolateLeft: 'clamp' as const,
  extrapolateRight: 'clamp' as const,
};

const easeOut = Easing.bezier(0.16, 1, 0.3, 1);

const panelStyle: React.CSSProperties = {
  borderRadius: 34,
  boxShadow: '0 28px 80px rgba(0,0,0,0.32)',
};

const typeSlice = (text: string, frame: number, start: number, speed = 0.72) => {
  const visible = Math.floor(interpolate(frame, [start, start + text.length * speed], [0, text.length], clamp));
  return text.slice(0, visible);
};

const MessageBubble: React.FC<{message: ChatMessage; colors: MotionBrief['colors']}> = ({message, colors}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const enter = spring({frame: frame - message.at, fps, config: {damping: 18, stiffness: 130}});
  const y = interpolate(enter, [0, 1], [28, 0]);
  const scale = interpolate(enter, [0, 1], [0.96, 1]);
  const opacity = interpolate(frame, [message.at, message.at + 10], [0, 1], clamp);
  const isLeader = message.role === 'leader';
  const isAi = message.role === 'ai';
  const bg = isLeader ? colors.ink : isAi ? '#E9FFFA' : '#FFFFFF';
  const color = isLeader ? '#FFFFFF' : colors.ink;
  const align = isLeader ? 'flex-start' : 'flex-end';

  return (
    <div style={{display: 'flex', justifyContent: align, opacity, transform: `translateY(${y}px) scale(${scale})`}}>
      <div style={{maxWidth: 600, padding: '22px 26px', borderRadius: 28, background: bg, color, border: isAi ? `2px solid ${colors.ai}` : 'none'}}>
        <div style={{fontSize: 20, letterSpacing: 1.4, textTransform: 'uppercase', opacity: 0.7, marginBottom: 8}}>{message.speaker}</div>
        <div style={{fontSize: 30, lineHeight: 1.25, fontWeight: 700}}>{typeSlice(message.text, frame, message.at + 8)}</div>
      </div>
    </div>
  );
};

const EvidenceStack: React.FC<{brief: MotionBrief; scale: number}> = ({brief, scale}) => {
  const frame = useCurrentFrame();
  return (
    <div style={{display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 18}}>
      {brief.evidenceCards.map((label, index) => {
        const local = frame - Math.round(96 * scale) - Math.round(index * 8 * scale);
        const p = spring({frame: local, fps: 30, config: {damping: 20, stiffness: 120}});
        return (
          <div key={label} style={{background: '#FFFFFF', borderRadius: 22, padding: 22, transform: `translateY(${interpolate(p, [0, 1], [40, 0])}px) rotate(${interpolate(p, [0, 1], [index === 1 ? 0 : 4 - index * 4, 0])}deg)`, opacity: interpolate(local, [0, 12], [0, 1], clamp)}}>
            <div style={{height: 9, width: 62, borderRadius: 999, background: brief.colors.alert, marginBottom: 22}} />
            <div style={{fontSize: 28, color: brief.colors.ink, fontWeight: 800}}>{label}</div>
            <div style={{fontSize: 18, color: brief.colors.muted, marginTop: 12}}>source ready</div>
          </div>
        );
      })}
    </div>
  );
};

const AiPlan: React.FC<{brief: MotionBrief; scale: number}> = ({brief, scale}) => {
  const frame = useCurrentFrame();
  return (
    <div style={{display: 'grid', gap: 16}}>
      {brief.aiSteps.map((step, index) => {
        const p = spring({frame: frame - Math.round(206 * scale) - Math.round(index * 10 * scale), fps: 30, config: {damping: 22, stiffness: 150}});
        return (
          <div key={step} style={{display: 'flex', alignItems: 'center', gap: 18, transform: `translateX(${interpolate(p, [0, 1], [70, 0])}px)`, opacity: interpolate(p, [0, 1], [0, 1])}}>
            <div style={{width: 44, height: 44, borderRadius: 14, background: brief.colors.ai, color: '#062B25', display: 'grid', placeItems: 'center', fontSize: 24, fontWeight: 900}}>{index + 1}</div>
            <div style={{fontSize: 34, fontWeight: 850, color: brief.colors.ink}}>{step}</div>
          </div>
        );
      })}
    </div>
  );
};

export const MotionCanvas: React.FC<MotionBrief> = (brief) => {
  const frame = useCurrentFrame();
  const {width, height, durationInFrames} = useVideoConfig();
  const isVertical = height > width;
  const pad = isVertical ? 72 : 86;
  const titleEnter = spring({frame, fps: 30, config: {damping: 18, stiffness: 110}});
  const timelineScale = durationInFrames / 720;
  const final = interpolate(frame, [durationInFrames - 90, durationInFrames - 35], [0, 1], {...clamp, easing: easeOut});

  return (
    <AbsoluteFill style={{background: brief.colors.background, fontFamily: 'Avenir Next, DIN Alternate, PingFang SC, sans-serif', color: brief.colors.ink, overflow: 'hidden'}}>
      <div style={{position: 'absolute', inset: 0, backgroundImage: 'linear-gradient(rgba(255,255,255,0.055) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.055) 1px, transparent 1px)', backgroundSize: '64px 64px', opacity: 0.85}} />
      <div style={{position: 'absolute', width: 680, height: 680, borderRadius: 999, right: -190, top: -240, background: `radial-gradient(circle, ${brief.colors.ai}66, transparent 65%)`}} />

      <div style={{position: 'absolute', left: pad, top: pad, right: pad, display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start'}}>
        <div style={{transform: `translateY(${interpolate(titleEnter, [0, 1], [38, 0])}px)`, opacity: interpolate(frame, [0, 14], [0, 1], clamp)}}>
          <div style={{fontSize: isVertical ? 62 : 76, lineHeight: 0.95, color: '#FFFFFF', fontWeight: 900, maxWidth: isVertical ? 780 : 920}}>{brief.title}</div>
          <div style={{fontSize: 28, color: '#A8B3C7', marginTop: 22}}>{brief.subtitle}</div>
        </div>
        <div style={{border: '1px solid rgba(255,255,255,0.18)', borderRadius: 999, color: '#DCE7F7', padding: '14px 20px', fontSize: 22}}>30fps deterministic</div>
      </div>

      <div style={{position: 'absolute', left: pad, right: pad, bottom: pad, height: isVertical ? height * 0.64 : height * 0.62, display: 'grid', gridTemplateColumns: isVertical ? '1fr' : '1.05fr 0.95fr', gap: 30}}>
        <div style={{...panelStyle, background: brief.colors.panel, padding: 34, display: 'flex', flexDirection: 'column', gap: 22, justifyContent: 'space-between'}}>
          {brief.messages.map((message) => (
            <MessageBubble
              key={`${message.role}-${message.at}`}
              message={{...message, at: Math.round(message.at * timelineScale)}}
              colors={brief.colors}
            />
          ))}
        </div>
        <div style={{display: 'grid', gridTemplateRows: '0.9fr 1.1fr', gap: 30}}>
          <div style={{...panelStyle, background: '#EAF0F7', padding: 28}}>
            <div style={{fontSize: 20, color: brief.colors.muted, fontWeight: 800, letterSpacing: 1.2, textTransform: 'uppercase', marginBottom: 20}}>Context stack</div>
            <EvidenceStack brief={brief} scale={timelineScale} />
          </div>
          <div style={{...panelStyle, background: '#FFFFFF', padding: 34, position: 'relative', overflow: 'hidden'}}>
            <div style={{position: 'absolute', right: -60, bottom: -90, width: 260, height: 260, borderRadius: 999, background: `${brief.colors.ai}33`}} />
            <div style={{fontSize: 20, color: brief.colors.muted, fontWeight: 800, letterSpacing: 1.2, textTransform: 'uppercase', marginBottom: 28}}>AI organizes the reply</div>
            <AiPlan brief={brief} scale={timelineScale} />
          </div>
        </div>
      </div>

      <Sequence from={durationInFrames - 100} durationInFrames={100}>
        <div style={{position: 'absolute', left: pad, right: pad, bottom: pad, height: 96, borderRadius: 28, background: brief.colors.ai, color: '#062B25', display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 34px', transform: `translateY(${interpolate(final, [0, 1], [120, 0])}px)`, opacity: final}}>
          <div style={{fontSize: 30, fontWeight: 900}}>Final status</div>
          <div style={{fontSize: 30, fontWeight: 800}}>{brief.finalStatus}</div>
        </div>
      </Sequence>
    </AbsoluteFill>
  );
};
