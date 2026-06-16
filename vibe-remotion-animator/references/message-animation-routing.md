# Message Animation Routing

Use this reference when the request is about sending messages, chat bubbles, conversation playback, reply workflows, group chat, DM, customer support, or AI assistant conversation.

## Default Route

Prefer the installed `wechat-2d-render` for conversation/message animation requests when the user wants a chat-style video, message bubbles, transparent overlay, or a realistic send/receive flow. In short: route message animation to installed wechat-2d-render first.

1. Resolve installed `wechat-2d-render`:

```bash
skill_dir=""
for base in "${AGENTS_HOME:-$HOME/.agents}" "${CLAUDE_HOME:-$HOME/.claude}" "${CODEX_HOME:-$HOME/.codex}"; do
  if [ -d "$base/skills/wechat-2d-render" ]; then
    skill_dir="$base/skills/wechat-2d-render"
    break
  fi
done
```

2. If installed, use its render script and pass a custom props JSON when possible:

```bash
bash "$skill_dir/scripts/render_wechat_2d.sh" "$workspace" "$output" "$props_json"
```

3. If the desired visual is not WeChat-like, first try to modify the `wechat-2d-render` project structure or props. Use `vibe-remotion-animator` custom Remotion scenes only when the chat needs a non-chat product layout such as dashboards, task cards, or multi-panel storytelling.
4. For a larger video, treat each chat segment as a source scene. Render or adapt the chat scene, then compose it with other scenes through `Series`/`Sequence` rather than recreating every bubble from scratch.

Do not start from the generic starter for ordinary message sending, chat playback, or reply-bubble animations.

## When To Use Custom Remotion Instead

Use a custom Remotion scene instead of `wechat-2d-render` when:

- The UI must look like DingTalk, Slack, Discord, Codex, email, CRM, or a custom enterprise app.
- The scene needs dashboards, task cards, AI plans, file cards, or multi-panel storytelling around the chat.
- The user asks for vertical social content, kinetic typography overlays, or product explainer pacing rather than realistic chat playback.
- `wechat-2d-render` is not installed and installing it would slow down the task more than building a small deterministic scene.

## Conversation Data Shape

Keep conversation content data-driven:

```json
{
  "messages": [
    {"role": "leader", "name": "周总", "text": "18:00 前给我一版周报", "at": 18},
    {"role": "ai", "name": "AI 助手", "text": "我来整理纪要、表格和群聊", "at": 240},
    {"role": "me", "name": "我", "text": "收到，17:30 给您初稿", "at": 510}
  ]
}
```

Use string slicing for typing. Use frame-derived send pulses and read receipts. Do not use timers, CSS transitions, or mutable cursors.

## Composition Handoffs

When a message scene feeds an agent or product scene:

- Use the sent bubble, send button, unread badge, or read receipt as the transition object.
- Keep chat text short enough to read before the cut.
- If the next scene is Codex/Claude Code execution, the outgoing chat bubble should become a requirement card or query prompt.
- If the previous scene is agent delivery, the output card should become the outgoing reply bubble.
