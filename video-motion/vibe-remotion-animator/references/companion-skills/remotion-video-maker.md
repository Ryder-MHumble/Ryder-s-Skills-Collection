# remotion-video-maker (companion)

## 触发条件

- v2 内置的 `create_remotion_motion_starter.py` **不够用** 时
- 需要更复杂的 Remotion React 项目（多 composition、props 类型、zod schema）
- 需要 preview / 编辑工作流（不只是 render）

## 与 v2 关系

v2 的 starter 是**最简的最小可用**版本（适合短讲解）。当 brief 复杂度升级（多 scene 切换、复杂状态管理、TS 类型严格），升级到 remotion-video-maker。

## 切换判断

| v2 够用 | 用 remotion-video-maker |
|---|---|
| 1-3 个 scene | 4+ 个 scene |
| 单一 aspect ratio | 多平台（9:16 + 16:9）|
| 简单 props | 复杂 props + zod schema |
| 一次性 render | preview → 调参 → render 工作流 |

## 输入参数

- 完整 brief（与 v2 一致）
- 指定 Remotion 项目结构（src/compositions/, src/components/）
- 期望的 props schema

## 输出格式

- 完整 Remotion 项目脚手架（npm init + dependencies）
- TypeScript + 严格类型
- 自带 preview 脚本

## 未安装时降级

v2 的 `create_remotion_motion_starter.py` 可以覆盖 80% 场景；如果 brief 超出范围，在 ANALYSIS REPORT 里标 "需要 companion: remotion-video-maker" 并提示用户安装。
