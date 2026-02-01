# 插画生成反面案例库

**目的**：记录生成过程中出现的错误，避免重复犯错

---

## 案例1：彩铅风格不明显（照片转换效果）

**日期**：2026-02-01
**画风**：细腻彩铅（西方）
**主题**：金鱼草

### 错误表现
- 生成的图片看起来像照片加滤镜
- 没有可见的彩铅笔触
- 没有纸张质感
- 过于光滑和写实

### 错误 Prompt
```
Technique: Layered burnishing, rich color saturation, smooth blending.
Texture: Polished finish, minimal paper grain, photorealistic rendering.
```

### 问题分析
- 过度强调 "photorealistic", "polished finish"
- 缺少彩铅核心特征关键词
- 没有强调手绘感

### 正确 Prompt
```
HAND-DRAWN colored pencil art with VISIBLE PENCIL STROKES.
Paper texture must be evident. Hand-drawn quality with slight natural imperfections.
Layered pencil marks creating rich color.
This is NOT a photo - it's hand-drawn colored pencil art.
```

### 关键教训
- 必须明确强调 "HAND-DRAWN", "VISIBLE PENCIL STROKES"
- 必须说明 "This is NOT a photo filter"
- 使用专业彩铅艺术家名字作为参考

---

## 案例2：画纸+背景效果

**日期**：2026-02-01
**画风**：细腻彩铅（西方）
**主题**：金鱼草

### 错误表现
- 看起来像"拍摄一幅画"
- 有白色画纸边缘
- 画纸周围有背景（桌面、其他物品）
- 元构图效果

### 问题分析
- AI 理解成了"在画纸上画画，然后拍摄画纸"
- 缺少明确约束说明这是画作本身

### 正确 Prompt
```
CRITICAL: This is the artwork itself filling the entire frame,
NOT a photograph of a drawing on paper.
No paper edges, no background behind the artwork, no meta-composition.
```

### 关键教训
- 必须明确说明这是画作本身，不是拍摄画作
- 禁止画纸边缘和背景分层
- 整个画面都是绘制的

---

## 案例3：构图差异不明显

**日期**：2026-02-01
**画风**：细腻彩铅（西方）
**主题**：金鱼草

### 错误表现
- 中景和整体全景看起来像同一张图
- 只是简单地把整体图两边抹白
- 没有真正的观看距离差异

### 错误 Prompt
```
Mid-range: Balanced composition, plant as main subject
Full Scene: Complete view, showing the complete plant-pot unit
```

### 问题分析
- 构图描述太模糊
- 缺少具体的裁切和百分比说明
- AI 理解成简单裁剪而非不同观看距离

### 正确 Prompt
```
Mid-range:
- Show the COMPLETE plant growing naturally from the pot
- Include: flowers → stems → leaves → pot (upper half)
- Pot bottom is cropped out

Full Scene:
- Show 100% of plant AND 100% of pot AND surface
- Complete pot visible from rim to base
- This is farther back than mid-range

CRITICAL DIFFERENCE: Mid-range crops pot bottom, Full Scene shows complete pot + base
```

### 关键教训
- 使用具体的百分比和裁切说明
- 明确说明不同视角的区别
- 强调不是简单裁剪，而是不同观看距离

---

## 案例4：植物逻辑错误（花朵和花盆分离）

**日期**：2026-02-01
**画风**：细腻彩铅（西方）
**主题**：金鱼草

### 错误表现
- 花朵看起来不是从花盆里生长
- 花朵悬浮在空中，花盆在下面
- 缺少茎叶连接
- 看起来像拼贴

### 错误 Prompt
```
Mid-range: Frame the flowers TIGHTLY
The flowers fill most of the image (80-90%)
The pot is BARELY visible at the bottom (10-20%)
```

### 问题分析
- 过度强调"紧密裁剪花朵"
- 导致裁掉了中间的茎叶连接部分
- AI 理解成"花朵+花盆"的拼贴

### 正确 Prompt
```
CRITICAL - PLANT CONTINUITY:
- Show the COMPLETE plant growing naturally from the pot
- You must see: flowers at top → stems in middle → leaves → pot (upper half)
- This is ONE continuous plant, not separate elements
- The plant EMERGES from the pot and grows upward naturally
```

### 关键教训
- 中景不是"紧密裁剪花朵"
- 中景是"显示植物的完整生长过程"
- 必须强调植物连续性，不是分离的元素

---

## 案例5：花朵密度不足

**日期**：2026-02-01
**画风**：细腻彩铅（西方）
**主题**：金鱼草

### 错误表现
- 花朵稀少，留白过多
- 不像参考图那样丰富饱满
- 构图空洞

### 问题分析
- 缺少花朵密度的描述
- 没有参考原图的丰富度

### 正确 Prompt
```
FLOWER DENSITY (IMPORTANT):
- Show ABUNDANT flowers - multiple flower spikes densely packed
- The flowers should be LUSH and FULL like in the reference photo
- Minimize empty space - create a full rich composition
- Think: A thriving plant in full bloom with many flowers
```

### 关键教训
- 必须强调花朵密集、丰富
- 参考原图的密度标准
- 减少留白，构图饱满

---

## 通用反面模式总结

### 反面模式1：过度写实导致失去手绘感
**关键词**：photorealistic, polished, smooth, digital
**后果**：看起来像照片滤镜，不是手绘艺术

### 反面模式2：模糊的构图描述
**关键词**：balanced, complete, general
**后果**：不同视角没有明显区别

### 反面模式3：元构图效果
**表现**：画纸+背景、拍摄画作
**后果**：不是纯粹的画作

### 反面模式4：忽视自然逻辑
**表现**：植物元素分离、悬浮
**后果**：不符合植物生长规律

### 反面模式5：过度留白
**表现**：花朵稀少、构图空洞
**后果**：不够丰富饱满

---

## 预防检查清单

在生成任何插画前，检查 Prompt 是否包含：

### 风格特征检查
- [ ] 是否强调手绘感？（HAND-DRAWN）
- [ ] 是否强调可见笔触？（VISIBLE STROKES）
- [ ] 是否说明不是照片？（NOT a photo filter）

### 构图逻辑检查
- [ ] 是否有具体的裁切说明？
- [ ] 是否明确不同视角的区别？
- [ ] 是否强调不是简单裁剪？

### 画面纯粹性检查
- [ ] 是否说明这是画作本身？
- [ ] 是否禁止画纸边缘？
- [ ] 是否禁止背景分层？

### 自然逻辑检查
- [ ] 是否强调植物连续性？
- [ ] 是否说明植物从盆里生长？
- [ ] 是否禁止元素分离？

### 画面饱满度检查
- [ ] 是否强调花朵密集？
- [ ] 是否要求减少留白？
- [ ] 是否参考原图密度？

---

**更新时间**：2026-02-01
**适用范围**：所有插画风格
