# 跨画风问题分析报告

**日期**：2026-02-01
**分析目的**：检查其他画风是否存在与"细腻彩铅（西方）"相同的问题

---

## 问题清单（基于彩铅西方的经验）

### 问题1：风格特征不明显
**表现**：生成的图片不像该画风，更像照片转换
**原因**：Prompt 缺少该画风的核心特征关键词

### 问题2：构图差异不明显
**表现**：中景视角和整体全景看起来像同一张图
**原因**：构图描述不够具体，缺少明确的裁切和百分比说明

### 问题3：意境氛围图改变植物特征
**表现**：第4张图的植物与参考图差异较大
**原因**：缺少"保持植物特征"的约束

---

## 各画风当前 Prompt 分析

### 1. 清新水彩（东方）- watercolor_oriental

**当前 Prompt 特征**：
- 艺术家参考：Qi Baishi (齐白石)
- 风格关键词：`Chinese freehand brushwork, expressive simplicity, poetic composition`
- 构图：`Subject occupies 40-50% of frame with intentional negative space`
- 技法：`Wet-on-wet washes, transparent layering, visible brushstrokes`

**潜在问题评估**：
- ✅ **风格特征**：有明确的水彩技法描述（wet-on-wet, transparent layering）
- ⚠️ **构图差异**：可能存在问题，构图描述不够具体
- ⚠️ **意境氛围**：可能存在问题，缺少植物特征约束

**建议优化**：
1. 在 `generate_series()` 中为水彩添加特殊约束（类似彩铅）
2. 强化构图差异描述
3. 意境氛围图添加植物特征约束

---

### 2. 清新水彩（西方）- watercolor_western

**当前 Prompt 特征**：
- 艺术家参考：John Singer Sargent
- 风格关键词：`gestural brushwork, delicate layering, luminous washes`
- 构图：`Subject occupies 60-70% of frame, dynamic composition`
- 技法：`Wet-on-dry for controlled edges, multiple transparent layers`

**潜在问题评估**：
- ✅ **风格特征**：有明确的水彩技法描述
- ⚠️ **构图差异**：可能存在问题，构图描述不够具体
- ⚠️ **意境氛围**：可能存在问题，缺少植物特征约束

**建议优化**：同水彩东方

---

### 3. 水墨国画（东方）- ink_oriental

**当前 Prompt 特征**：
- 艺术家参考：Bada Shanren (八大山人), Song Dynasty masters
- 风格关键词：`Gongbi: meticulous line work. Xieyi: minimalist ink, expressive freedom`
- 构图：`Gongbi: 60-70% of frame. Xieyi: 30-40% of frame`
- 技法：`Baimiao outline (白描), Fenran separation (分染), Zhaoyan glazing (罩染)`

**潜在问题评估**：
- ✅ **风格特征**：有非常详细的国画技法描述（工笔/写意）
- ⚠️ **构图差异**：可能存在问题，构图描述不够具体
- ⚠️ **意境氛围**：可能存在问题，缺少植物特征约束

**建议优化**：
1. 国画的意境氛围图尤其需要植物特征约束（因为写意风格容易过度发挥）
2. 强化构图差异描述

---

### 4. 细腻彩铅（东方）- pencil_oriental

**当前 Prompt 特征**：
- 艺术家参考：Japanese botanical illustration tradition
- 风格关键词：`botanical illustration, delicate shading, soft transitions`
- 构图：`Subject occupies 70-80% of frame, specimen-style`
- 技法：`Light to dark layering, gentle pressure, soft blending`

**潜在问题评估**：
- ⚠️ **风格特征**：可能存在问题，缺少"visible pencil strokes"等关键词
- ⚠️ **构图差异**：可能存在问题，构图描述不够具体
- ⚠️ **意境氛围**：可能存在问题，缺少植物特征约束

**建议优化**：
1. 参考彩铅西方的优化，添加"visible pencil strokes", "paper texture"
2. 强调手绘感，避免过度光滑
3. 强化构图差异描述
4. 意境氛围图添加植物特征约束

---

### 5. 细腻彩铅（西方）- pencil_western

**当前状态**：✅ 已优化（第3轮）

**优化内容**：
- 强化彩铅特征：`HAND-DRAWN`, `VISIBLE PENCIL STROKES`, `paper texture`
- 艺术家参考更新：Ann Swan, Janie Gildow
- 构图差异明确化：中景60-70%裁切，整体100%完整
- 意境氛围约束：`BOTANICAL ACCURACY (MOST IMPORTANT)`

**待验证**：API 恢复后测试

---

### 6. 质感油画（东方）- oil_oriental

**当前 Prompt 特征**：
- 艺术家参考：Classical oil painting with Eastern aesthetic
- 风格关键词：`poetic atmosphere, soft edges, subtle mood`
- 构图：`Subject occupies 70-80% of frame, classical arrangement`
- 技法：`Dark to light progression (从暗到明), transparent glazing`

**潜在问题评估**：
- ✅ **风格特征**：有明确的油画技法描述（glazing, underpainting）
- ⚠️ **构图差异**：可能存在问题，构图描述不够具体
- ⚠️ **意境氛围**：可能存在问题，缺少植物特征约束

**建议优化**：
1. 强化构图差异描述
2. 意境氛围图添加植物特征约束

---

### 7. 质感油画（西方）- oil_western

**当前 Prompt 特征**：
- 艺术家参考：Classical oil painting masters
- 风格关键词：`dramatic chiaroscuro, rich impasto, bold brushwork`
- 构图：`Subject occupies 70-80% of frame, dramatic lighting`
- 技法：`Dark to light progression, impasto technique, visible brushstrokes`

**潜在问题评估**：
- ✅ **风格特征**：有明确的油画技法描述
- ⚠️ **构图差异**：可能存在问题，构图描述不够具体
- ⚠️ **意境氛围**：可能存在问题，缺少植物特征约束

**建议优化**：同油画东方

---

### 8. 装饰彩绘（东方）- gouache_oriental

**当前 Prompt 特征**：
- 艺术家参考：Chinese folk art tradition
- 风格关键词：`decorative patterns, flat color blocks, folk art charm`
- 构图：`Subject occupies 60-70% of frame, decorative arrangement`
- 技法：`Flat color application, decorative patterns, opaque gouache`

**潜在问题评估**：
- ✅ **风格特征**：有明确的彩绘技法描述
- ⚠️ **构图差异**：可能存在问题，构图描述不够具体
- ⚠️ **意境氛围**：可能存在问题，缺少植物特征约束

**建议优化**：
1. 强化构图差异描述
2. 意境氛围图添加植物特征约束

---

### 9. 装饰彩绘（西方）- gouache_western

**当前 Prompt 特征**：
- 艺术家参考：Modern illustration tradition
- 风格关键词：`graphic design, bold colors, contemporary illustration`
- 构图：`Subject occupies 60-70% of frame, modern composition`
- 技法：`Flat color application, clean edges, opaque gouache`

**潜在问题评估**：
- ✅ **风格特征**：有明确的彩绘技法描述
- ⚠️ **构图差异**：可能存在问题，构图描述不够具体
- ⚠️ **意境氛围**：可能存在问题，缺少植物特征约束

**建议优化**：同彩绘东方

---

## 通用问题总结

### 问题1：构图差异不明显（所有画风）

**当前状态**：
- 所有画风的构图描述都比较模糊
- 只有彩铅西方（第3轮优化）有明确的裁切和百分比说明

**建议统一优化**：
1. **中景视角**：
   - 明确：`Show 60-70% of the plant (upper portion)`
   - 明确：`Pot is PARTIALLY visible - only the TOP EDGE`
   - 明确：`The bottom of the pot is CUT OFF`

2. **整体全景**：
   - 明确：`Show 100% of the plant AND 100% of the pot AND the surface`
   - 明确：`The COMPLETE pot must be visible from rim to bottom`
   - 对比：`CRITICAL DIFFERENCE from Mid-range`

---

### 问题2：意境氛围图改变植物特征（所有画风）

**当前状态**：
- 所有画风都缺少"保持植物特征"的约束
- 只有彩铅西方（第3轮优化）添加了 `BOTANICAL ACCURACY` 约束

**建议统一优化**：
在所有画风的意境氛围图 Prompt 中添加：
```
BOTANICAL ACCURACY (MOST IMPORTANT):
- The plant MUST maintain its exact characteristics from the reference photo
- Flower shape, color, and structure must match the reference
- Do NOT change the plant species or significantly alter its appearance
- The artistic interpretation is in the ENVIRONMENT, not in changing the plant itself
```

---

### 问题3：风格特征不明显（部分画风）

**高风险画风**：
- 细腻彩铅（东方）：缺少"visible pencil strokes"等关键词
- 可能还有其他画风需要测试后确认

**建议**：
1. 先完成彩铅西方的验证
2. 如果成功，逐一测试其他画风
3. 根据测试结果针对性优化

---

## 优化优先级

### 高优先级（立即优化）
1. ✅ 细腻彩铅（西方）- 已完成第3轮优化，待验证
2. ⚠️ 细腻彩铅（东方）- 可能存在与西方相同的风格问题

### 中优先级（彩铅验证成功后）
3. 所有画风的构图差异优化（统一应用彩铅的构图策略）
4. 所有画风的意境氛围图植物特征约束（统一添加 BOTANICAL ACCURACY）

### 低优先级（根据测试结果）
5. 其他画风的风格特征优化（如果测试发现问题）

---

## 下一步行动计划

1. **等待 API 恢复**
2. **验证彩铅西方第3轮优化**
3. **如果成功**：
   - 将构图优化应用到所有画风
   - 将意境氛围约束应用到所有画风
   - 优化彩铅东方的风格特征
4. **如果失败**：
   - 继续调整彩铅西方的 Prompt
   - 记录新的问题和解决方案
5. **逐一测试其他画风**
6. **更新 style-prompt-templates.md**
