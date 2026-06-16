# pixel2motion (companion)

## 触发条件

- brief 里有 logo / 品牌图标需要做动效
- 输入是 raster 格式（PNG/JPG/WebP/screenshot），不是 SVG

## 与 v2 关系

v2 的 `light-spotlight-render` 是给**文字**做聚光灯揭示。pixel2motion 是给**logo 图标**做矢量化 + 动效。两者场景不重叠。

## 切换判断

- brief 含 "我的 logo"、"品牌图标"、"应用 icon" → pixel2motion
- brief 含 "标题动画"、"文字揭示" → v2 内置 spotlight

## 输入参数

- raster 图像路径（PNG/JPG/WebP）
- 期望的动效类型（svg-assembly 风格 / fade-in / 旋转等）
- 目标尺寸

## 输出格式

- 矢量化后的 SVG
- Remotion 组件 / HTML 动画 / GIF / MP4（按用户选）

## 工作流

1. raster → minimal SVG（边缘平滑处理）
2. SVG → 动效模板
3. 渲染输出

## 未安装时降级

如果只有现成 SVG（不用矢量化），用 v2 内置的 `svg-assembly-animator` 组件。
