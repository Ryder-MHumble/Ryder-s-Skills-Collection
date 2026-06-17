# Shot Table 模板

## 模板（8 列）

| # | Time (s) | Story Beat | Visual Action | Scene Type | Template | Transition | Evidence Frame |
|---|---|---|---|---|---|---|---|
| 1 | 0.0-3.0 | Hook: 抛出问题 | 大字 + 闪烁背景 | text-reveal | spotlight / claude-typer | fade-in | frame 30 |
| 2 | 3.0-8.0 | 拆解问题 | 步骤卡片依次出现 | step-cards | svg-assembly | handoff: send-pulse | frame 90, 180 |
| 3 | ... | ... | ... | ... | ... | ... | ... |

## 字段说明

- **#**: scene 编号（从 1 开始）
- **Time (s)**: 起止时间（精确到 0.1s）
- **Story Beat**: 这个 scene 在叙事上说什么（**一句话**）
- **Visual Action**: 视觉上发生什么（**具体动作描述**，不是抽象概念）
- **Scene Type**: 场景类型分类（text-reveal / step-cards / data-viz / chat / agent-run / logo / 3d / custom）
- **Template**: 用哪个组件（v2 内置的 scene-components 或 companion）
- **Transition**: 与下一个 scene 的衔接方式（cut / fade / handoff: send-pulse / handoff: camera-slide / mask-wipe / status-bar）
- **Evidence Frame**: 关键帧（用于 still-frame 验证，frame 编号按 30fps 算）

## Scene Type 枚举

| Type | 典型用途 | 优先模板 |
|---|---|---|
| `text-reveal` | 标题、副标题、关键句揭示 | spotlight, claude-typer |
| `step-cards` | 步骤、清单、流程 | svg-assembly, custom Remotion |
| `data-viz` | 数字、图表、对比 | ruler-progress (companion), custom |
| `chat` | 微信聊天、消息流 | wechat-2d |
| `agent-run` | agent 执行过程、typer、plan-edit-verify | claude-typer, custom |
| `logo` | 品牌图标、应用 icon | pixel2motion (companion), svg-assembly |
| `3d` | 3D 地球、3D 滚动、3D 模型 | earth-render, 3d-ticker |
| `music` | 音乐播放器 UI、黑胶 | vinyl-player |
| `process` | 过程演示、线性步骤 | procedural-fish (companion) |
| `custom` | 以上都不覆盖的 | custom Remotion scene |

## Transition 枚举

- `cut` — 硬切（无过渡，节奏最快）
- `fade` — 淡入淡出（0.3-0.5s）
- `handoff: send-pulse` — 一个元素"发射"出去，下个 scene 接收（chaining）
- `handoff: camera-slide` — 摄像机滑动
- `mask-wipe` — 遮罩扫过
- `status-bar` — 通过共享的 UI 元素（如顶部状态条）连接
- `none` — 直接接（仅当 scene 共享一个 canvas 时用）

## 长度建议

| 视频总时长 | scene 数量 | 平均时长 |
|---|---|---|
| 15-30s | 3-5 | 4-6s |
| 30-60s | 5-8 | 5-8s |
| 1-3min | 8-15 | 6-10s |
| 3-8min | 15-30 | 10-20s |
| > 8min | 30+ | 20s+ |

## 验证检查

- [ ] 每个 scene 的 Story Beat 用一句话能说清
- [ ] 每个 scene 只有一个 dominant action
- [ ] Total time = 各 scene 时长之和 + transition 时长
- [ ] 没有"原理说明"塞进一个 scene
- [ ] 没有 scene 共享一个 canvas（除非 explicit 标注）
