---
name: vibe-remotion-animator
version: 2.0.0
description: "【社媒视频统一入口】基于 Remotion 制作讲解/分享/demo 类短视频。v2 物理整合 7 个核心场景组件 + 内置 Disney 12 动画设计原则 + 支持 3 平台规格（抖音/B 站/视频号），**强制先 ANALYSIS 后 BUILD 工作流**：Phase 1 拆解 brief + 选平台 + 场景路由矩阵，输出 ANALYSIS REPORT 经用户批准后，Phase 2 才进入施工。适用：抖音/B 站/视频号讲解、agent demo 演示、流程分享、AI/科技短视频。不适合：访谈长视频（用 Video-Wrapper-Skills）、直播、纯静态图。"
author: Ryder + Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [creative, video, remotion, social-media, douyin, bilibili, wechat-channels, motion-graphics, agent-demo]
    related_skills: [light-spotlight-render, claude-typer, svg-assembly-animator, wechat-2d-render, threejs-earth-render, remotion-vinyl-player, remotion-3d-ticker, remotion-video-maker, pixel2motion, procedural-fish-render, ruler-progress-render, disney-animation-rule-skill, Video-Wrapper-Skills]
prerequisites:
  commands: [python3, node, npm, npx]
  optional: [ffmpeg, puppeteer]
---

# Vibe Remotion Animator v2.0

社媒视频统一入口。从 "brief → 分析 → 渲染" 一站式，**先 ANALYSIS 后 BUILD**。

## v2 核心变化（vs v1）

| 维度 | v1 | v2 |
|---|---|---|
| 角色 | 路由器（dispatch to other skills）| 统一入口（路由器 + 物理整合 + 原则库）|
| 设计原则 | 文档零散提及 | **内置 Disney 12 原则库** |
| 工作流 | 直接调 starter 脚本 | **强制 ANALYSIS REPORT checkpoint** |
| 场景组件 | 6 个外部依赖 | **7 个物理整合 + 4 个 companion** |
| 平台支持 | 通用 | 抖音 + B 站 + 视频号 3 平台规格 |
| 路径 | 硬编码 codex 路径 | HERMES_HOME/HERMES_OUTPUT 环境变量 |

## 何时使用

- ✅ **讲解类短视频**（"我是怎么用 AI 做 XXX 的"）
- ✅ **Demo 演示视频**（agent 跑流程、工具操作）
- ✅ **工作流分享**（"我每天的工作流"）
- ✅ **品牌/产品介绍**（带 logo 动效）
- ✅ **知识科普**（步骤化讲解）

## 不适合

- ❌ **访谈长视频**（>10 分钟）→ 用 `Video-Wrapper-Skills`
- ❌ **直播 / 录屏** → 用 OBS / ScreenFlow
- ❌ **纯静态图** → 用 Figma / Sketch
- ❌ **音频播客** → 用 Audacity / 喜马拉雅
- ❌ **动画电影**（长篇）→ 用 After Effects

---

## 核心工作流：先 ANALYSIS 后 BUILD

**v2 强制两阶段，Phase 1 输出 ANALYSIS REPORT 必须经用户批准后才能进 Phase 2。**

```
[0] 接收 brief
   ↓
[1] ANALYSIS PHASE  ← 【必走，用户审批】
   ├─ 1.1 平台规格分析
   ├─ 1.2 内容类型识别
   ├─ 1.3 场景分解（shot table）
   ├─ 1.4 设计原则匹配（Disney 12 原则）
   ├─ 1.5 渲染器路由（routing matrix）
   └─ 1.6 输出 ANALYSIS REPORT
   ↓
[ USER APPROVES / REVISE / REJECT ]
   ↓
[2] BUILD PHASE
   ├─ 2.1 创建项目（create_remotion_motion_starter.py）
   ├─ 2.2 装依赖（npm install）
   ├─ 2.3 适配 scene components
   ├─ 2.4 渲染 MP4
   └─ 2.5 验证输出
```

---

## Phase 1: ANALYSIS

### 1.1 平台规格分析

读取 `references/platform-specs/`，按 brief 目标平台读取对应文件：
- `douyin.md` — 9:16 / ≤3min / 前 3s hook
- `bilibili.md` — 16:9 / 1-15min / 章节时间戳
- `wechat-channels.md` — 9:16 / ≤1min / 静音播放场景多

### 1.2 内容类型识别

| 内容类型 | 关键特征 | 优先模板 |
|---|---|---|
| 讲解类 | 步骤清晰、有逻辑链 | step-cards + text-reveal |
| Demo 类 | 工具操作、agent 跑流程 | agent-run + text-reveal |
| 分享类 | 经验、心得、观点 | text-reveal + music |
| 故事类 | 起承转合、人物 | custom + 3d/music |

### 1.3 场景分解

读 `references/scene-decomposition/shot-table-template.md`，按 8 列填表（time / story beat / visual action / scene type / template / transition / evidence frame）。

**原则**：
- 30s 视频 3-5 个 scene
- 1-3min 视频 8-15 个 scene
- 每个 scene 一个 dominant action

### 1.4 设计原则匹配

读 `references/design-principles/`，从 Disney 12 原则中**选 3-5 条**最相关的（不要全用）：
- **Squash & Stretch** — 物理感（按钮按下、弹起）
- **Anticipation** — 准备动作（跳跃前的下蹲）
- **Staging** — 主次清晰（突出关键信息）
- **Slow In & Slow Out** — 缓入缓出（自然感）
- **Arc** — 弧线运动（关节、生物）
- **Secondary Action** — 副动作（眨眼、手势）
- **Exaggeration** — 夸张（强调）

在 ANALYSIS REPORT 里**显式列出**选中的原则 + 选用理由。

### 1.5 渲染器路由

读 `references/scene-decomposition/routing-decision-tree.md`，按决策树把每个 scene 路由到：
- 7 个**内置组件**（见下文）
- 4 个 **companion skill**（见 `references/companion-skills/`）

### 1.6 输出 ANALYSIS REPORT

格式（用户必须看到完整内容才能批准）：

```markdown
# ANALYSIS REPORT

## 目标
- 平台: 抖音 + B 站
- 时长: 60-90s
- 比例: 9:16 主 / 16:9 副
- 类型: 讲解类（agent demo）

## 场景分解（shot table）
| # | Time | Story Beat | Action | Type | Template | Transition |
|---|---|---|---|---|---|---|
| 1 | 0-3s | Hook: 问题 | 大字 + 闪烁 | text-reveal | claude-typer | fade |
| 2 | 3-8s | 拆解: 3 步骤 | 卡片装配 | step-cards | svg-assembly | handoff: send-pulse |
| 3 | 8-50s | Demo: agent 跑 | typer + UI | agent-run | claude-typer | cut |
| 4 | 50-55s | 总结: 关键点 | spotlight | text-reveal | spotlight | fade |
| 5 | 55-60s | CTA: 关注 | brand | text-reveal | custom | none |

## 选用的设计原则
1. **Staging** — 每个 scene 主次清晰
2. **Anticipation** — scene 2 装配前有 0.3s 准备
3. **Slow In & Slow Out** — 全程不用 linear
4. **Exaggeration** — scene 3 打字速度比真实略夸张

## 渲染器路由
- 内置组件: claude-typer, svg-assembly, spotlight
- Companion: 无
- 路径冲突检查: ✓ 无

## 风险与建议
- 时长 60s scene 数量偏紧（5 个），如需展开扩到 8 个
- claude-typer 单 scene 最长 30s，本设计 scene 3=42s ⚠️ 建议拆成两个
```

**用户回复 `APPROVE` / `REVISE: <修改点>` / `REJECT` 后才进 Phase 2。**

---

## Phase 2: BUILD

### 2.1 创建项目

```bash
skill_dir="${HERMES_HOME:-$HOME/.hermes}/skills/creative/vibe-remotion-animator"
project_dir=$(python3 "$skill_dir/scripts/create_remotion_motion_starter.py" \
  --format horizontal \
  --duration 60 \
  --name my-motion)
```

输出位置：`"${HERMES_OUTPUT:-$HOME/workspace/hermes-output}/vibe-remotion-animations/my-motion"`

### 2.2 装依赖

```bash
cd "$project_dir"
npm install
```

### 2.3 适配 scene components

按 ANALYSIS REPORT 路由矩阵，从 `assets/scene-components/<template>/` 复制到项目 `src/components/animations/`，按 props 文档配置。

### 2.4 渲染 MP4

```bash
npm run still -- --frame=90   # 单帧验证
npm run render               # 全片渲染
```

### 2.5 验证输出

- 关键帧（evidence frame）与 ANALYSIS REPORT 一致？
- 平台规格（比例/时长/字幕）合规？
- 字幕全程显示？
- 静音播放体验？

---

## 内置场景组件（7 个物理整合）

| 组件 | 用途 | 路径 |
|---|---|---|
| `claude-typer` | 提示词打字机（agent 演示、标题）| `assets/scene-components/claude-typer/` |
| `light-spotlight-render` | 聚光灯扫字（标题、CTA）| `assets/scene-components/light-spotlight-render/` |
| `svg-assembly-animator` | SVG 零件组装（步骤卡、logo）| `assets/scene-components/svg-assembly-animator/` |
| `wechat-2d-render` | 微信聊天（消息流、社媒演示）| `assets/scene-components/wechat-2d-render/` |
| `threejs-earth-render` | Three.js 地球飞线（用户分布、全球）| `assets/scene-components/threejs-earth-render/` |
| `remotion-vinyl-player` | 黑胶唱片（音乐 UI）| `assets/scene-components/remotion-vinyl-player/` |
| `remotion-3d-ticker` | 3D 垂直滚动 ticker | `assets/scene-components/remotion-3d-ticker/` |

每个组件单独 README 在子目录内（`README.md`），含 props + 用法示例。

---

## Companion Skills（4 个外部依赖）

未物理整合，按需引用，详见 `references/companion-skills/`：

| Skill | 触发条件 | 文档 |
|---|---|---|
| `remotion-video-maker` | v2 starter 不够（4+ scene、复杂 props）| `remotion-video-maker.md` |
| `pixel2motion` | raster logo → 动效 | `pixel2motion.md` |
| `procedural-fish-render` | 过程演示、时间线 | `procedural-fish-render.md` |
| `ruler-progress-render` | 百分比/进度可视化 | `ruler-progress-render.md` |

---

## 设计原则库

`references/design-principles/` 内置 **Disney 12 原则**作为工程规则：

| 文件 | 内容 |
|---|---|
| `README.md` | 原则库总览（基于原 disney-animation-rule-skill）|
| `twelve-principles.md` | 12 原则全文 |
| `implementation-patterns.md` | 工程模式（pure state evaluation, semantic timeline...）|
| `clawd-jump-case-study.md` | 案例研究（"Clawd 跳跃"的对比）|

**使用方法**：Phase 1.4 选 3-5 条原则，在 ANALYSIS REPORT 显式列出选用理由。

---

## 平台规格

`references/platform-specs/` 三大目标平台硬约束：

| 平台 | 比例 | 时长 | 必加 |
|---|---|---|---|
| 抖音 | 9:16 | ≤ 3min（最佳 15-60s）| 字幕 + 前 3s hook |
| B 站 | 16:9 | 1-15min | 章节时间戳 |
| 视频号 | 9:16 | ≤ 1min 最佳 | 字幕（静音播放多）|

跨平台发布：先做 9:16 竖版（覆盖抖音+视频号），B 站另出 16:9 横版。

---

## Quick Start

```bash
# 1. 设置环境变量（首次）
export HERMES_HOME="$HOME/.hermes"
export HERMES_OUTPUT="$HOME/workspace/hermes-output"

# 2. 接收 brief → 走 ANALYSIS PHASE
# （v2 强制先输出 ANALYSIS REPORT，批准后才进 BUILD）

# 3. 用户批准后，创建项目
skill_dir="$HERMES_HOME/skills/creative/vibe-remotion-animator"
project_dir=$(python3 "$skill_dir/scripts/create_remotion_motion_starter.py" \
  --format horizontal \
  --duration 60 \
  --name my-motion)

# 4. 进入项目
cd "$project_dir"
npm install

# 5. 渲染
npm run still -- --frame=90  # 关键帧
npm run render              # 全片
```

---

## 路径解析

v2 用环境变量避免硬编码（修复 v1 的硬编码问题）：

- `$HERMES_HOME` — Hermes 安装目录（默认 `$HOME/.hermes`）
- `$HERMES_OUTPUT` — 输出目录（默认 `$HOME/workspace/hermes-output`）

**未设置时 fallback 到默认值**，不报错。

---

## 升级路线

| 版本 | 计划 |
|---|---|
| v2.0 (当前) | 重构入口 + 物理整合 + Disney 原则 + 平台规格 |
| v2.1 | 加 `scripts/check_platform_compliance.py`（自动验证）|
| v2.2 | 加 `scripts/analyze_brief.py`（自动生成 ANALYSIS REPORT 初稿）|
| v3.0 | 接入 LLM 生成 shot table（用户只给 brief）|

---

## 与其他 skill 关系

| Skill | 关系 |
|---|---|
| `Video-Wrapper-Skills` | **互补**：v2 做"内容"，wrapper 做"包装"（访谈后处理）|
| `video-downloader` | **工具**：v2 制作完成后用此下载参考素材 |
| `kol-interview-to-wiki` | **正交**：KOL 内容转 wiki，与社媒视频独立 |
| `deep-research` | **正交**：调研素材来源，可与 v2 配合（先调研后做视频）|

---

## 维护说明

- **升级 6 个内置组件**：直接编辑 `assets/scene-components/<name>/`，按组件原仓库升级方式
- **新增内置组件**：物理整合到 `assets/scene-components/`，更新本 SKILL.md 组件表
- **新增 companion**：在 `references/companion-skills/` 加 README，不动物理目录
- **设计原则升级**：在 `references/design-principles/` 加新文档，README 引用
- **平台规格更新**：直接改 `references/platform-specs/<platform>.md`

---

**用 v2 制作社媒视频前，先读 SKILL.md 顶部的工作流图，再开始 Phase 1。**
