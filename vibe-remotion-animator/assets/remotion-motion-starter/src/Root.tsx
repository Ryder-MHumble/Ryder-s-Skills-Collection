import React from 'react';
import {Composition} from 'remotion';
import {z} from 'zod';
import {zColor} from '@remotion/zod-types';
import {defaultBrief} from './content';
import {MotionCanvas} from './MotionCanvas';

export const motionBriefSchema = z.object({
  title: z.string(),
  subtitle: z.string(),
  format: z.string(),
  colors: z.object({
    background: zColor(),
    panel: zColor(),
    ink: zColor(),
    muted: zColor(),
    accent: zColor(),
    ai: zColor(),
    alert: zColor(),
  }),
  messages: z.array(z.object({
    speaker: z.string(),
    role: z.enum(['leader', 'worker', 'ai']),
    text: z.string(),
    at: z.number(),
  })),
  evidenceCards: z.array(z.string()),
  aiSteps: z.array(z.string()),
  finalStatus: z.string(),
});

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="MotionCanvas"
      component={MotionCanvas}
      durationInFrames={__DURATION_FRAMES__}
      fps={__FPS__}
      width={__WIDTH__}
      height={__HEIGHT__}
      defaultProps={defaultBrief}
      schema={motionBriefSchema}
    />
  );
};
