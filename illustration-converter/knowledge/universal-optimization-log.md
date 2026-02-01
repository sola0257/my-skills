# 通用优化应用日志

**日期**：2026-02-01
**版本**：v2.1 - 通用优化版
**影响范围**：所有10种画风

---

## 优化内容

### 1. 构图差异明确化（所有画风）

**问题**：中景视角和整体全景构图差异不明显，看起来像同一张图

**解决方案**：

#### 中景视角
```
- Show approximately 60-70% of the plant (upper portion with flowers/leaves)
- Pot is PARTIALLY visible - only the TOP EDGE or RIM of the pot should be in frame
- The bottom of the pot and base are CUT OFF by the frame edge
- This creates a "portrait" feel focusing on the plant's character
```

#### 整体全景
```
- Show 100% of the plant AND 100% of the pot AND the surface/base it sits on
- The COMPLETE pot must be visible from rim to bottom
- Include the surface the pot rests on (table, ground, etc.)
- This is the "documentary" view showing the complete subject
```

#### 关键对比说明
```
CRITICAL DIFFERENCE from Mid-range: Mid-range crops the pot, Full Scene shows the complete pot and base.
```

**预期效果**：
- 中景视角：植物肖像感，聚焦植物性格
- 整体全景：标本记录感，完整展示

---

### 2. 植物特征约束（所有画风的意境氛围图）

**问题**：意境氛围图容易改变植物特征，与参考图差异较大

**解决方案**：

在所有画风的第4张图（意境氛围）添加最高优先级约束：

```
BOTANICAL ACCURACY (MOST IMPORTANT - APPLIES TO ALL STYLES):
- The plant MUST maintain its exact characteristics from the reference photo
- Flower shape, color, and structure must match the reference (e.g., if snapdragons, they must look like snapdragons)
- Do NOT change the plant species or significantly alter its appearance
- The artistic interpretation is in the ENVIRONMENT, not in changing the plant itself
```

**关键说明**：
```
Place the plant-pot unit within an imagined beautiful garden setting, but the plant itself remains botanically accurate to the reference.
```

```
Natural Logic (CRITICAL):
- Maintain botanical accuracy - the plant species and characteristics must match the reference photo
- Only the environment is imagined, the plant itself is accurate
```

**预期效果**：
- 植物保持参考图的准确特征
- 艺术发挥体现在环境氛围
- 避免过度想象导致植物变形

---

### 3. 画风特定约束（所有画风）

**问题**：不同画风需要不同的技法提醒，避免生成通用的"数字艺术"效果

**解决方案**：

为每种画风添加专属的 `medium_specific` 约束：

#### 彩铅（Colored Pencil）
```
COLORED PENCIL SPECIFIC: Show VISIBLE PENCIL STROKES. Paper texture must be evident. Hand-drawn quality with slight natural imperfections. Layered pencil marks creating rich color. This is NOT a photo - it's hand-drawn colored pencil art.
```

#### 水彩（Watercolor）
```
WATERCOLOR SPECIFIC: Show transparent washes, soft edges, water blooms, and natural color bleeding. Visible brushstrokes and paper texture. This is watercolor painting, not digital art.
```

#### 国画（Ink Painting）
```
INK PAINTING SPECIFIC: Show ink gradations (墨分五色), expressive brushstrokes, and natural ink flow. This is traditional ink painting, not digital art.
```

#### 油画（Oil Painting）
```
OIL PAINTING SPECIFIC: Show visible brushstrokes, impasto texture where appropriate, and rich color layering. This is oil painting, not digital art.
```

#### 彩绘（Gouache）
```
GOUACHE SPECIFIC: Show opaque flat colors, clean edges, and matte finish. This is gouache painting, not digital art.
```

**预期效果**：
- 每种画风都有明确的技法特征
- 避免生成通用的"AI 艺术"效果
- 强调传统媒介的真实质感

---

## 技术实现

### 代码结构

```python
# 识别画风类型
is_pencil = "pencil" in style_code
is_watercolor = "watercolor" in style_code
is_ink = "ink" in style_code
is_oil = "oil" in style_code
is_gouache = "gouache" in style_code

# 根据画风选择技法术语和约束
if is_pencil:
    technique_term = "drawn"
    medium_specific = "COLORED PENCIL SPECIFIC: ..."
elif is_watercolor:
    technique_term = "painted"
    medium_specific = "WATERCOLOR SPECIFIC: ..."
# ... 其他画风
```

### 应用位置

1. **局部特写**：添加画风特定约束
2. **中景视角**：添加构图约束 + 画风特定约束
3. **整体全景**：添加构图约束 + 画风特定约束
4. **意境氛围**：添加植物特征约束 + 画风特定约束

---

## 影响的画风列表

✅ 已应用通用优化的画风（10种）：

1. watercolor_oriental - 清新水彩（东方）
2. watercolor_western - 清新水彩（西方）
3. ink_oriental - 水墨国画（东方）
4. ink_western - 水墨国画（西方）
5. pencil_oriental - 细腻彩铅（东方）
6. pencil_western - 细腻彩铅（西方）
7. oil_oriental - 质感油画（东方）
8. oil_western - 质感油画（西方）
9. gouache_oriental - 装饰彩绘（东方）
10. gouache_western - 装饰彩绘（西方）

---

## 验证计划

### 优先级1：彩铅西方（已测试）
- 测试主题：金鱼草
- 状态：待 API 恢复后验证第3轮优化

### 优先级2：其他彩铅
- pencil_oriental - 细腻彩铅（东方）
- 验证是否需要额外的风格特征优化

### 优先级3：水彩系列
- watercolor_oriental
- watercolor_western
- 验证构图差异和植物特征约束效果

### 优先级4：其他画风
- 国画、油画、彩绘
- 逐一验证通用优化效果

---

## 预期收益

1. **减少调试时间**：
   - 通用问题一次性解决
   - 避免逐一发现和修复

2. **提高一致性**：
   - 所有画风使用统一的构图策略
   - 所有画风都有植物特征约束

3. **提升质量**：
   - 构图差异更明显
   - 意境氛围图更准确
   - 画风特征更突出

---

## 后续工作

1. ⏳ 等待 API 恢复
2. 🧪 验证彩铅西方优化效果
3. 🧪 逐一测试其他画风
4. 📝 根据测试结果微调
5. 📚 更新 style-prompt-templates.md

---

**更新时间**：2026-02-01
**更新人**：Claude (基于用户反馈优化)
