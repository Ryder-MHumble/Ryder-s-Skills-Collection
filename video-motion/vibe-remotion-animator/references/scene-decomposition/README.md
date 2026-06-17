# Scene Decomposition — 场景分解方法

v2 工作流的核心前置：**先把 brief 分解成可执行场景**，再施工。

## 为什么必须先分解？

- **避免一次画布装所有内容**（观众认知过载）
- **明确每个 scene 的渲染器路由**（避免临时决策）
- **输出可被用户审的 shot table**（v2 的 ANALYSIS REPORT checkpoint）

## 两份核心文档

| 文档 | 用途 |
|---|---|
| `shot-table-template.md` | 标准 shot table 模板（8 列）|
| `routing-decision-tree.md` | 场景 → 渲染器路由决策树 |

## 工作流位置

```
[0] 接收 brief
   ↓
[1] ANALYSIS PHASE
   ├─ 1.1 平台规格分析
   ├─ 1.2 内容类型识别
   ├─ 1.3 场景分解  ← 【本目录】
   ├─ 1.4 设计原则匹配
   ├─ 1.5 渲染器路由  ← 【本目录】
   └─ 1.6 输出 ANALYSIS REPORT
   ↓
[2] BUILD PHASE
```

## 关键原则

- **每个 scene 一个 story beat**：一句话能说清这个 scene 在表达什么
- **每个 scene 一个 dominant action**：避免一个画面里多个动画打架
- **scene 间有明确 transition**：handoff、cut、mask wipe，不能直接接
- **scene 总数控制**：30s 视频 3-5 个 scene；3min 视频 8-12 个
- **不要把"原理说明"塞进一个 scene**：拆成 "原理 1" + "原理解释" 两个 scene
