export type ChatMessage = {
  speaker: string;
  role: 'leader' | 'worker' | 'ai';
  text: string;
  at: number;
};

export type MotionBrief = {
  title: string;
  subtitle: string;
  format: '__FORMAT__';
  colors: {
    background: string;
    panel: string;
    ink: string;
    muted: string;
    accent: string;
    ai: string;
    alert: string;
  };
  messages: ChatMessage[];
  evidenceCards: string[];
  aiSteps: string[];
  finalStatus: string;
};

export const defaultBrief: MotionBrief = {
  title: 'Task lands. Human + AI reply.',
  subtitle: 'A frame-driven office collaboration motion template.',
  format: '__FORMAT__',
  colors: {
    background: '#0B111D',
    panel: '#F6F1E7',
    ink: '#142033',
    muted: '#6C7480',
    accent: '#2F6BFF',
    ai: '#22C7A9',
    alert: '#FFB020',
  },
  messages: [
    {
      speaker: 'Leader',
      role: 'leader',
      text: 'Please send the weekly project update before 18:00. Include risks and next steps.',
      at: 18,
    },
    {
      speaker: 'Worker',
      role: 'worker',
      text: 'Got it. I will collect meeting notes and table data first.',
      at: 420,
    },
    {
      speaker: 'AI',
      role: 'ai',
      text: 'Draft ready: data sources, risk list, suggested actions, and a concise reply.',
      at: 270,
    },
  ],
  evidenceCards: ['meeting notes', 'status table', 'risk log'],
  aiSteps: ['extract signals', 'group risks', 'draft reply'],
  finalStatus: 'In progress - first draft at 17:30',
};
