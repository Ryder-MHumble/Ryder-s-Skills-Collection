# ruler-progress-render (companion)

## 触发条件

- brief 涉及**数据可视化**、**进度感**、**量化对比**
- 需要 "X% 完成" 风格的视觉锚点
- 适合教程完成度、加载状态、KPI 展示

## 与 v2 关系

v2 没有数字/百分比动效模板。ruler-progress 提供**标尺类视觉**（带刻度 + 进度填充）。

## 切换判断

- 需要"百分比" / "N/N 完成" / "倒计时" 视觉 → ruler-progress
- 只是展示文字/图标 → v2 内置

## 输入参数

- 目标百分比（0-100）或步骤数
- 标尺样式（线性 / 圆形 / 数字滚动）
- 动画时长

## 输出格式

- 透明背景 MP4 / GIF
- 可叠加到其他视频

## 典型用法

```bash
python3 scripts/render_ruler_progress.py \
  --percent 75 \
  --style linear \
  --output ruler-75percent.mp4
```

## 未安装时降级

用 v2 内置的 `svg-assembly-animator` 做 "数字揭示" 动效作为简单替代。
