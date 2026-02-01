# 细腻彩铅（西方美感）Prompt 优化记录

**日期**：2026-02-01
**测试主题**：金鱼草（Snapdragon）
**参考图片**：/Users/dj/Downloads/IMG_5244.JPG

---

## 优化历程

### 第1轮生成（失败）

**Prompt 特征**：
- 使用通用模板，没有针对4张系列图的独立 Prompt
- 技法描述：`Layered burnishing, rich color saturation, smooth blending`
- 质感描述：`Polished finish, minimal paper grain, photorealistic rendering`

**用户反馈（不满意 ❌）**：
1. ❌ **风格问题**：生成的不是彩铅风格
2. ❌ **构图问题**：局部特写和整体景观没有明显区别
3. ❌ **真实感问题**：局部特写不真实，像是照片贴画
4. ❌ **第四张问题**：意境氛围图明显不是彩铅画风

**核心问题诊断**：
- Prompt 没有强调彩铅的核心特征（笔触、纸张质感、手绘感）
- 过度强调"photorealistic"导致 AI 生成照片转换效果
- 缺少"visible pencil strokes"、"paper texture"等关键词

---

### 第2轮生成（部分改进）

**Prompt 优化**：
1. **强化彩铅特征**：
   - 新增：`HAND-DRAWN colored pencil art, visible pencil strokes, paper texture`
   - 新增：`This must look like REAL COLORED PENCIL ART, not a photo filter`
   - 技法：`VISIBLE PENCIL STROKES throughout, paper tooth texture showing, hand-drawn quality`

2. **艺术家参考更新**：
   - 从 "Margaret Mee" 改为 "Ann Swan, Janie Gildow"（专业彩铅艺术家）

3. **针对彩铅的特殊 Prompt 添加**：
   - 局部特写：强调"Show VISIBLE PENCIL STROKES at this close range"
   - 中景视角：强调"Varying stroke directions following plant forms"
   - 整体全景：强调"Consistent colored pencil technique across entire image"
   - 意境氛围：强调"EVERYTHING must show COLORED PENCIL TEXTURE"

**用户反馈（部分可以）**：
1. ✅ **局部特写**：可以
2. ❌ **中景和整体全景**：用的是一张图，没有太大变化
3. ❌ **意境氛围**：跟参考图里的花相差有点远

**新问题诊断**：
- 彩铅风格问题已解决（局部特写可以）
- 新问题：构图差异不够明显（中景 vs 整体全景）
- 新问题：意境氛围图改变了植物特征

---

### 第3轮优化（待测试）

**针对构图问题的优化**：

1. **中景视角**：
   - 明确要求：`Show approximately 60-70% of the plant (upper portion)`
   - 关键约束：`Pot is PARTIALLY visible - only the TOP EDGE or RIM`
   - 裁切说明：`The bottom of the pot and base are CUT OFF by the frame edge`
   - 比喻：`Think: "plant portrait" showing its personality`

2. **整体全景**：
   - 明确要求：`Show 100% of the plant AND 100% of the pot AND the surface/base`
   - 关键约束：`The COMPLETE pot must be visible from rim to bottom`
   - 对比说明：`CRITICAL DIFFERENCE from Mid-range: Mid-range crops the pot, Full Scene shows the complete pot and base`

3. **意境氛围**：
   - 新增最高优先级约束：`BOTANICAL ACCURACY (MOST IMPORTANT)`
   - 明确要求：`The plant MUST maintain its exact characteristics from the reference photo`
   - 关键说明：`The artistic interpretation is in the ENVIRONMENT, not in changing the plant itself`
   - 强调：`Only the environment is imagined, the plant itself is accurate`

**待验证**：API 连接问题，需要稍后重新生成测试

---

## 关键经验总结

### ✅ 正面经验（有效的 Prompt 策略）

1. **强调手绘质感**：
   - 使用 `HAND-DRAWN`, `VISIBLE PENCIL STROKES`, `paper texture` 等关键词
   - 明确说明 `This is NOT a photo filter`

2. **艺术家参考**：
   - 使用专业彩铅艺术家名字（Ann Swan, Janie Gildow）比通用描述更有效

3. **技法细节**：
   - 描述具体技法：`cross-hatching`, `layered color application`, `burnishing`
   - 强调质感：`paper tooth texture`, `natural variations in pressure`

4. **针对彩铅的特殊约束**：
   - 每张图都添加 `COLORED PENCIL SPECIFIC` 段落
   - 强调统一的彩铅质感（特别是意境氛围图）

### ❌ 反面经验（无效或有害的 Prompt 策略）

1. **过度强调写实**：
   - ❌ `photorealistic rendering` 导致照片转换效果
   - ❌ `polished finish` 失去手绘感
   - ❌ `minimal paper grain` 失去纸张质感

2. **构图描述不够具体**：
   - ❌ `Balanced composition` 太模糊
   - ❌ `Complete view` 不够明确
   - ✅ 需要具体的百分比和裁切说明

3. **缺少植物特征约束**：
   - ❌ 意境氛围图容易改变植物特征
   - ✅ 需要明确说明"保持参考图的植物特征"

---

## 待检查问题

1. **其他画风是否存在同样问题**：
   - 水彩（东方/西方）
   - 国画（东方/西方）
   - 彩铅（东方）
   - 油画（东方/西方）
   - 彩绘（东方/西方）

2. **通用问题**：
   - 构图差异是否在所有画风中都不够明显？
   - 意境氛围图是否在所有画风中都容易改变植物特征？

---

**下一步行动**：
1. 等待 API 恢复后重新生成第2、3、4张图片
2. 验证第3轮优化效果
3. 如果成功，将优化经验应用到其他画风
4. 更新所有画风的 Prompt 模板
