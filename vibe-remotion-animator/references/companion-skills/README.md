# Companion Skills — 外部依赖技能库

vibe-remotion-animator v2.0 **物理整合了 6 个核心场景组件** 到 `assets/scene-components/`。但社媒视频场景丰富，仍有 4 个相关 skill **未物理整合**——它们以"companion skill"形式存在，使用时按需引用。

## 为什么不全整合？

- **避免 v2 体积膨胀**：物理整合的核心是 6 个最常用组件
- **保持单一职责**：companion skill 自己也是独立可用的
- **降低升级成本**：companion 升级时不用动 v2
- **避免功能重复**：有的 companion 与 v2 有部分重叠，整合会丢失独立性

## Companion 列表

| Skill | 用途 | 与 v2 关系 |
|---|---|---|
| `remotion-video-maker` | Remotion React 视频综合制作 | 当 v2 的 `create_remotion_motion_starter.py` 不够用时使用 |
| `pixel2motion` | raster logo → minimal SVG → 动效 | 视频开头 logo 动画的专业工具 |
| `procedural-fish-render` | 流程鱼动画（克隆 vibe-motion/procedural-fish）| 适合过程演示、时间线类内容 |
| `ruler-progress-render` | 标尺进度动画（克隆 sxhzju/ruler-progress-animator）| 适合数据可视化、进度感内容 |

## 引用方式

v2 工作流在 routing matrix 阶段会标记"需要 companion skill"：

```
scene 1 (logo reveal) → pixel2motion (companion)
scene 2-5 (主内容) → vibe-remotion-animator 内置组件
scene 6 (进度展示) → ruler-progress-render (companion)
```

每个 companion 在 v2 里有独立 README（在 `references/companion-skills/`），说明：
- 触发条件（什么场景用）
- 输入参数
- 输出格式
- 失败 fallback（如未安装时如何降级）
