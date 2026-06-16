# Routing Decision Tree — 场景 → 渲染器路由

把 shot table 里的每个 scene **精确路由**到 v2 内置组件或 companion skill。

## 主决策流程

```
scene_type?
├── text-reveal
│   ├── 是品牌/标题大字? ─── yes → light-spotlight-render
│   ├── 是 AI/agent 输入? ── yes → claude-typer
│   └── 是动态打字效果? ─── yes → claude-typer
├── step-cards
│   ├── 需要 SVG 零件打散? ─ yes → svg-assembly-animator
│   └── 只是文字步骤? ──────── yes → custom Remotion (data-driven)
├── data-viz
│   ├── 百分比/进度? ──────── yes → ruler-progress-render (companion)
│   └── 数字滚动/对比? ────── yes → custom Remotion
├── chat
│   └── 微信风格? ────────── yes → wechat-2d-render
├── agent-run
│   ├── Claude UI? ───────── yes → claude-typer
│   ├── Codex UI? ────────── yes → claude-typer (改 model name)
│   └── 其他 agent? ──────── yes → custom Remotion
├── logo
│   ├── raster 输入? ─────── yes → pixel2motion (companion)
│   └── SVG 输入? ────────── yes → svg-assembly-animator
├── 3d
│   ├── 地球/航线? ───────── yes → threejs-earth-render
│   ├── 垂直滚动? ────────── yes → remotion-3d-ticker
│   └── 其他 3D? ─────────── yes → custom
├── music
│   └── 黑胶/音乐 UI? ────── yes → remotion-vinyl-player
├── process
│   └── 步骤流/时间线? ────── yes → procedural-fish-render (companion)
└── custom
    └── 以上都不覆盖 ──────── yes → custom Remotion + scene 路由说明
```

## 物理整合 vs Companion 决策

| 组件 | 类型 | 选择理由 |
|---|---|---|
| `light-spotlight-render` | 物理整合 | 社媒 logo/标题必备 |
| `claude-typer` | 物理整合 | agent 演示高频 |
| `svg-assembly-animator` | 物理整合 | 步骤卡/标志动效 |
| `wechat-2d-render` | 物理整合 | 微信聊天演示 |
| `threejs-earth-render` | 物理整合 | 品牌展示常需要 |
| `remotion-vinyl-player` | 物理整合 | 音乐类内容 |
| `remotion-3d-ticker` | 物理整合 | 3D 滚动效果 |
| `remotion-video-maker` | companion | 综合制作，v2 覆盖 80% |
| `pixel2motion` | companion | raster 输入场景少 |
| `procedural-fish-render` | companion | 流程演示较窄 |
| `ruler-progress-render` | companion | 数据可视化较窄 |

## 组合路由示例

### 例 1：30s 抖音讲解 "我如何用 AI 写周报"

| Scene | Type | Template | 备注 |
|---|---|---|---|
| 1 (0-3s) | text-reveal | claude-typer | "我用 AI 写周报" 打字动画 |
| 2 (3-8s) | step-cards | svg-assembly | 步骤 1-2-3 依次组装 |
| 3 (8-20s) | agent-run | claude-typer | 演示 AI agent 跑周报 |
| 4 (20-25s) | text-reveal | spotlight | "5 分钟搞定" 聚光灯 |
| 5 (25-30s) | text-reveal | custom Remotion | CTA + 关注引导 |

### 例 2：3min B 站教程 "vibe-motion 全流程"

| Scene | Type | Template |
|---|---|---|
| 1 (0-10s) | text-reveal | claude-typer (hook) |
| 2 (10-30s) | step-cards | svg-assembly (流程概览) |
| 3 (30-60s) | 3d | threejs-earth-render (用户分布) |
| 4 (60-120s) | data-viz | ruler-progress-render (companion) |
| 5 (120-160s) | agent-run | claude-typer (核心 demo) |
| 6 (160-170s) | music | vinyl-player (BGM 段) |
| 7 (170-180s) | text-reveal | spotlight (结尾) |

## 失败模式

- **scene_type 模糊**：拆成多个 scene
- **同 scene 用 2+ 模板**：违反"一个 dominant action"，拆
- **找不到合适模板**：用 custom Remotion，标"需要新组件"作为反馈
- **全用同一个模板**：通常意味着场景分解不够细，回到 shot table 重新看
