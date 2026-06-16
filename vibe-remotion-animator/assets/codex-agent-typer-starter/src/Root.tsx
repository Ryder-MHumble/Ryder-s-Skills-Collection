import React from 'react';
import {Composition} from 'remotion';
import {z} from 'zod';
import {zColor} from '@remotion/zod-types';
import {CodexAgentTyper} from './CodexAgentTyper';
import {defaultContent} from './content';

const contentSchema = z.object({
  prompt: z.string(),
  modelLabel: z.string(),
  title: z.string(),
  subtitle: z.string(),
  phases: z.array(z.string()),
  terminalLines: z.array(z.string()),
  files: z.array(z.string()),
  colors: z.object({
    bg: zColor(),
    panel: zColor(),
    panel2: zColor(),
    ink: zColor(),
    muted: zColor(),
    codex: zColor(),
    success: zColor(),
    warning: zColor(),
  }),
});

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="CodexAgentTyper"
      component={CodexAgentTyper}
      durationInFrames={__DURATION_FRAMES__}
      fps={__FPS__}
      width={__WIDTH__}
      height={__HEIGHT__}
      defaultProps={defaultContent}
      schema={contentSchema}
    />
  );
};
