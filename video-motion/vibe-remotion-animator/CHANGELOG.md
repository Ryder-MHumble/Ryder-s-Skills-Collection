# Changelog

`vibe-remotion-animator` 演进记录。

---

## v2.0.0 (2026-06-16) — 当前版本

**核心改动**：从"路由器"升级为"社媒视频统一入口"

### 破坏性变化

- 路径硬编码 → 环境变量 (`HERMES_HOME` / `HERMES_OUTPUT`)
- 工作流强制两阶段（ANALYSIS → BUILD），v1 是直接调脚本
- 输出位置从 `~/Desktop/vibe-remotion-animations/` 改为 `$HERMES_OUTPUT/vibe-remotion-animations/`

### 新增

- **7 个物理整合的场景组件**（`assets/scene-components/`）：
  - `claude-typer` — 提示词打字机（agent 演示、标题）
  - `light-spotlight-render` — 聚光灯扫字
  - `svg-assembly-animator` — SVG 零件组装
  - `wechat-2d-render` — 微信聊天
  - `threejs-earth-render` — Three.js 地球飞线
  - `remotion-vinyl-player` — 黑胶唱片
  - `remotion-3d-ticker` — 3D 垂直滚动 ticker（已剔除 26MB demo GIF）

- **Disney 12 原则库**（`references/design-principles/`）：
  - 整体物理整合自 `disney-animation-rule-skill`
  - 工程模式 + 案例研究

- **3 平台规格库**（`references/platform-specs/`）：
  - 抖音 9:16 / ≤3min
  - B 站 16:9 / 1-15min
  - 视频号 9:16 / ≤1min

- **场景分解方法库**（`references/scene-decomposition/`）：
  - shot-table 8 列模板
  - 渲染器路由决策树

- **4 个 companion skill 文档**（`references/companion-skills/`）：
  - `remotion-video-maker`, `pixel2motion`, `procedural-fish-render`, `ruler-progress-render`

- **强制 ANALYSIS REPORT checkpoint**：
  - 5 步骤分析（平台 / 类型 / 场景 / 原则 / 路由）
  - 用户必须 `APPROVE` / `REVISE` / `REJECT` 才进 Phase 2

### 修改

- SKILL.md 完全重写（v1 是路由式入口，v2 是工作流入口）
- 路径引用从绝对路径改为环境变量

### 升级方式

如已部署 v1：
1. 删除 `~/.codex/skills/vibe-remotion-animator`（避免双份）
2. 在新 session 加载 v2（hermes 自动发现 `~/.hermes/skills/creative/vibe-remotion-animator`）
3. 设置 `HERMES_OUTPUT` 环境变量（可选，默认 `$HOME/workspace/hermes-output`）

---

## v1.x (历史)

v1 是从 sxhzju/vibe-motion 项目 fork 的"路由器"型 skill：
- 文档里**显式调用** 6 个其他 skill
- 用户必须自己安装所有依赖
- 没有"先分析"工作流，直接调 starter 脚本
- 路径硬编码到 `/Users/rydersun/.codex/skills/...`

v1 备份在 `~/workspace/hermes-output/.archive/vibe-remotion-animator-v1-2026-06-16/`。
