# 反面案例：第四张"意境氛围"图偏离参考

## 📅 基本信息
- **日期**：2026-02-01
- **风格**：清新水彩（东方美感）
- **植物**：垂吊多肉植物
- **问题图片**：04_意境氛围.png

## ❌ 问题描述

第四张图（意境氛围）的植物形态与参考图不一致，前三张图都保持了同一植物的不同角度，但第四张图的植物发生了变化。

## 🔍 根本原因分析

### Prompt 设计问题

**第4张图的 Prompt**：
```
Details: Simplified form of succulent rosettes, emphasis on negative space,
soft color washes, dreamlike quality
Composition: Artistic interpretation with maximum white space, single rosette
or small cluster, asymmetric placement
```

**问题关键词**：
- `Simplified form` - 给了AI"简化形态"的权限
- `dreamlike quality` - 鼓励了艺术化偏离
- `Artistic interpretation` - 允许了创意发挥

**对比前三张图的 Prompt**：
- 第1-3张都明确保留了参考图的具体特征：
  - `cascading form`（垂吊形态）
  - `rosette formations`（莲座结构）
  - `pink-tipped leaves`（粉色叶尖）
  - `jade-green leaves with coral-pink edges`（翠绿叶片+珊瑚粉边缘）

### AI 理解偏差

AI 将"意境氛围"理解为可以"艺术化简化"植物特征，导致：
1. 植物形态发生变化
2. 失去了与前三张图的视觉连贯性
3. 不再是同一株植物的不同表现

## ✅ 正确做法

### 改进后的 Prompt

```
Details: Same cascading succulent with jade-green plump leaves and coral-pink tips,
rosette formations clearly visible, maintaining the plant's characteristic features.
Composition: Minimalist presentation with maximum white space, single rosette cluster
in gentle focus, soft ethereal atmosphere, asymmetric placement.
Mood: Poetic and ethereal, zen-like tranquility, but keeping the plant recognizable.
```

### 关键改变

**保留**：
- ✅ 具体植物特征描述（`cascading succulent`, `jade-green`, `coral-pink tips`）
- ✅ 结构特征（`rosette formations`）
- ✅ 可识别性（`keeping the plant recognizable`）

**调整**：
- ✅ 只在构图和氛围上做"意境化"处理
- ✅ 用"minimalist presentation"替代"simplified form"
- ✅ 强调"maintaining the plant's characteristic features"

## 📊 核心原则

### 系列图生成的一致性原则

1. **植物特征必须一致**
   - 所有系列图必须是同一株植物
   - 只改变角度、构图、氛围
   - 不改变植物本身的形态特征

2. **Prompt 设计规范**
   - 每张图都要包含具体的植物特征描述
   - "意境化"只体现在构图和氛围上
   - 避免使用"simplified form"、"artistic interpretation"等给AI过多自由度的词汇

3. **检查清单**
   - [ ] Prompt 中是否包含具体植物特征？
   - [ ] 是否明确要求保持植物可识别性？
   - [ ] 是否避免了过度抽象化的描述？

## 🎯 应用场景

**适用于**：
- 所有需要生成系列图的场景
- 特别是第4张"意境氛围"图
- 任何强调"艺术化"、"意境"的图片

**检查时机**：
- Prompt 构建阶段（Step 3）
- 生成前的最后检查

## 📝 记录信息

- **发现者**：用户反馈
- **记录日期**：2026-02-01
- **影响范围**：系列图生成的视觉一致性
- **优先级**：高（影响用户满意度）

---

**更新日志**：
- 2026-02-01：初次记录，已更新到 SKILL.md 的 Prompt 模板指导中
