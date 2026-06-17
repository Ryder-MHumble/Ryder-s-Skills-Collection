# procedural-fish-render (companion)

## 触发条件

- brief 涉及**过程演示**、**时间线叙事**、**步骤流**
- 适合 "我是怎么一步步做 XXX 的" 类内容
- 需要程序化生成的鱼群/粒子作为视觉元素

## 与 v2 关系

v2 没有过程演示模板。procedural-fish 提供**动态背景** + 步骤流指示能力。

## 切换判断

- 内容是**线性步骤** → procedural-fish
- 内容是**单点强调** → v2 内置

## 输入参数

- 步骤列表（每步的标题/描述/时长）
- 鱼群/粒子参数（颜色、密度、速度）
- 视频比例

## 输出格式

- 1080×1920 (9:16) / 1920×1080 (16:9) MP4

## 典型用法

```bash
python3 scripts/render_procedural_fish.py \
  --steps "step1.md,step2.md,step3.md" \
  --output ~/workspace/hermes-output/vibe-remotion-animations/fish-demo.mp4
```

## 未安装时降级

没有真正的 fallback；如果 brief 强需求，提示用户安装或用 v2 的 svg-assembly 模拟"步骤装配"动效。
