export type CodexContent = {
  prompt: string;
  modelLabel: string;
  title: string;
  subtitle: string;
  phases: string[];
  terminalLines: string[];
  files: string[];
  colors: {
    bg: string;
    panel: string;
    panel2: string;
    ink: string;
    muted: string;
    codex: string;
    success: string;
    warning: string;
  };
};

export const defaultContent: CodexContent = {
  prompt: __PROMPT_JSON__,
  modelLabel: __MODEL_LABEL_JSON__,
  title: 'Codex agent run',
  subtitle: 'Prompt typing, plan, edit, verify, deliver.',
  phases: ['理解需求', '制定计划', '编辑文件', '运行验证', '交付结果'],
  terminalLines: [
    '$ codex run --agent',
    'reading workspace instructions...',
    'planning minimal motion system...',
    'editing Remotion components...',
    'npm run typecheck  PASS',
    'rendered MP4 and still frames',
  ],
  files: ['src/content.ts', 'src/CodexAgentTyper.tsx', 'out/codex-agent-typer.mp4'],
  colors: {
    bg: '#060A12',
    panel: '#101722',
    panel2: '#F4F0E8',
    ink: '#EAF2FF',
    muted: '#8B99AE',
    codex: '#26D7B8',
    success: '#62E6A7',
    warning: '#FFB020',
  },
};
