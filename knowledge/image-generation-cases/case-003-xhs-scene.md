# 案例 003：小红书真实场景图（3:4 竖版，手写文字）

> **返回索引**：[案例库索引](./README.md)

---

## 📋 基本信息

- **来源平台**：小红书
- **适用平台**：小红书（优先）、其他竖版平台需调整比例
- **验证状态**：✅ 已验证（2026-01-30）
- **文章主题**：多肉养护避坑指南
- **图片类型**：正文配图（dreamy-photo 风格 + 手写文字）
- **迭代次数**：多次优化
- **最终文件**：07_徒长就是缺光照.png 等

### ✅ 最终确认的 Prompt 结构

```
A 3:4 photograph in dreamy realistic style.

Scene: [具体场景描述，如：A succulent plant showing signs of etiolation (徒长) on a windowsill]

Lighting: Soft natural window light, warm golden hour glow, gentle shadows.

Details: [具体细节，如：The succulent has elongated stems and sparse leaves, demonstrating light deficiency, in a simple ceramic pot]

Mood: [情绪关键词，如：Educational, realistic, natural home environment]

Color palette: Muted Morandi colors, desaturated tones, cream and sage.

Style: Realistic lifestyle photography, soft focus, film-like quality.

Text overlay: Add Chinese text "[文字内容]" in a natural handwritten style, positioned in the [position], using a soft cream or dusty rose color.

Image size: 1080x1440 pixels (3:4 vertical format).

NO ENGLISH TEXT. NO PEOPLE. NO STUDIO LIGHTING.
```

### 🔒 固定部分（不要修改）

#### 1. 手写文字设计规范（真实场景图特征）

```
Text overlay: Add Chinese text "[文字内容]" in a natural handwritten style, positioned in the [position], using a soft cream or dusty rose color.
```

**关键要素**：
- ✅ `natural handwritten style` - 手写风格（不是粗体）
- ✅ `soft cream or dusty rose color` - 柔和的奶油色或灰粉色
- ✅ `positioned in the [position]` - 灵活定位（根据画面构图）
- ✅ 文字融入画面，不抢眼

**与封面文字的区别**：

| 维度 | 封面文字 | 真实场景图文字 |
|------|---------|--------------|
| **字体** | Bold, thick, chunky | Natural handwritten style |
| **颜色** | Pure white + black stroke | Soft cream or dusty rose |
| **位置** | Top center（固定） | Flexible（根据构图） |
| **大小** | Large and prominent | Medium, integrated |
| **效果** | SHARP, CLEAR, BOLD | Natural, soft, blended |

**为什么这些重要**：
- 封面需要吸引点击，文字要醒目
- 正文配图需要传达信息，文字要自然融入
- 手写风格更有亲和力和真实感

#### 2. 文字位置灵活选择原则

**根据画面构图选择位置**：

| 画面构图 | 推荐文字位置 | 原因 |
|---------|-------------|------|
| 主体在中下部 | upper left / upper right | 不遮挡主体 |
| 主体在左侧 | upper right / lower right | 平衡构图 |
| 主体在右侧 | upper left / lower left | 平衡构图 |
| 主体居中 | top center / bottom center | 对称美感 |
| 留白较多 | 留白区域 | 自然融入 |

**位置表达方式**：
- `upper left corner` - 左上角
- `upper right corner` - 右上角
- `lower left corner` - 左下角
- `lower right corner` - 右下角
- `top center` - 顶部居中
- `bottom center` - 底部居中

**实际案例**：
```
# 案例1：主体在中下部
Text overlay: Add Chinese text "我的多肉小花园" in a natural handwritten style, positioned in the lower left corner, using a soft cream or dusty rose color.

# 案例2：主体在左侧
Text overlay: Add Chinese text "叶片积水要注意" in a natural handwritten style, positioned in the upper right corner, using a soft cream or dusty rose color.

# 案例3：主体在右侧
Text overlay: Add Chinese text "这就是烂根的样子" in a natural handwritten style, positioned in the upper left corner, using a soft cream or dusty rose color.
```

#### 3. 光线和色调（保持真实感）

```
Lighting: Soft natural window light, warm golden hour glow, gentle shadows.
Color palette: Muted Morandi colors, desaturated tones, cream and sage.
Style: Realistic lifestyle photography, soft focus, film-like quality.
```

**关键词**：
- ✅ `Soft natural window light` - 柔和自然窗光
- ✅ `Muted Morandi colors` - 莫兰迪色系
- ✅ `desaturated tones` - 降低饱和度
- ✅ `film-like quality` - 胶片质感

### 🔄 可调整部分（根据具体内容修改）

#### 1. 场景描述

```
Scene: A succulent plant showing signs of etiolation (徒长) on a windowsill
```

**可替换**：
- 植物状态：健康/徒长/烂根/缺水等
- 场景位置：windowsill / table / shelf / balcony
- 具体植物：succulent / pothos / monstera 等

**保持**：
- 真实家居环境
- 自然状态（不是摆拍）

#### 2. 文字内容和位置

```
Text overlay: Add Chinese text "徒长就是缺光照" in a natural handwritten style, positioned in the upper right corner, using a soft cream or dusty rose color.
```

**可替换**：
- 文字内容：根据图片要传达的信息
- 位置：根据画面构图选择（参考位置选择原则）

**保持**：
- 手写风格
- 柔和颜色
- 自然融入

#### 3. 细节描述

```
Details: The succulent has elongated stems and sparse leaves, demonstrating light deficiency, in a simple ceramic pot
```

**可替换**：
- 植物特征：根据具体状态描述
- 容器类型：ceramic pot / plastic pot / wooden box
- 环境细节：根据场景添加

### 📊 真实场景图文字设计检查清单

生成小红书正文配图后，检查：

- [ ] 文字是否使用手写风格（不是粗体）
- [ ] 文字颜色是否柔和（奶油色或灰粉色）
- [ ] 文字位置是否根据构图灵活选择
- [ ] 文字是否自然融入画面（不抢眼）
- [ ] 文字是否清晰可读
- [ ] 背景是否真实（不是棚拍）
- [ ] 光线是否自然（窗光）
- [ ] 色调是否温馨（莫兰迪色系）

### 🎓 关键经验

#### 1. 封面 vs 正文配图的文字策略

**封面文字**：
- 目的：吸引点击
- 策略：醒目、大、粗体、白色+黑边
- 位置：固定（顶部居中）

**正文配图文字**：
- 目的：传达信息
- 策略：自然、融入、手写、柔和颜色
- 位置：灵活（根据构图）

#### 2. 文字位置的决策逻辑

```
读取画面构图 → 识别主体位置 → 选择不遮挡主体的位置 → 确保文字区域有足够留白
```

**错误示例**：
- ❌ 所有图片文字都在左下角（固定位置）
- ❌ 文字遮挡了主体
- ❌ 文字区域背景太复杂，看不清

**正确示例**：
- ✅ 根据每张图的构图灵活调整位置
- ✅ 文字在留白区域
- ✅ 文字不遮挡关键信息

#### 3. 手写风格的自然感

**为什么选择手写风格**：
- 更有亲和力
- 更真实（像手机拍照后加的标注）
- 不抢眼（不影响主体）
- 符合小红书生活化调性

**颜色选择原则**：
- ✅ `soft cream` - 适合深色背景
- ✅ `dusty rose` - 适合浅色背景
- ❌ 避免纯白色（太刺眼）
- ❌ 避免纯黑色（太重）

### 🔧 使用建议

1. **生成真实场景配图时**：
   - 先确定画面构图和主体位置
   - 根据构图选择文字位置
   - 使用手写风格和柔和颜色
   - 确保文字清晰但不抢眼

2. **文字位置决策流程**：
   ```
   Step 1: 分析画面构图（主体在哪里？）
   Step 2: 识别留白区域（哪里有空间？）
   Step 3: 选择合适位置（不遮挡主体）
   Step 4: 在 prompt 中指定位置
   ```

3. **验证清单**：
   - [ ] 是否使用 `natural handwritten style`？
   - [ ] 是否使用 `soft cream or dusty rose color`？
   - [ ] 是否根据构图灵活选择位置？
   - [ ] 是否避免了粗体和黑边（那是封面用的）？
   - [ ] 文字是否清晰可读但不抢眼？

### 📝 快速生成模板

```
A 3:4 photograph in dreamy realistic style.

Scene: [具体场景，如：A healthy pothos plant on a windowsill]

Lighting: Soft natural window light, warm golden hour glow, gentle shadows.

Details: [具体细节，如：The pothos has vibrant green leaves, in a cream ceramic pot, natural home environment]

Mood: [情绪，如：Calm, educational, natural]

Color palette: Muted Morandi colors, desaturated tones, cream and sage.

Style: Realistic lifestyle photography, soft focus, film-like quality.

Text overlay: Add Chinese text "[文字内容]" in a natural handwritten style, positioned in the [根据构图选择：upper left/upper right/lower left/lower right], using a soft cream or dusty rose color.

Image size: 1080x1440 pixels (3:4 vertical format).

NO ENGLISH TEXT. NO PEOPLE. NO STUDIO LIGHTING.
```

**填空说明**：
- `[具体场景]`：描述植物状态和环境
- `[具体细节]`：植物特征、容器、环境细节
- `[情绪]`：Calm, educational, natural, realistic 等
- `[文字内容]`：要显示的中文文字（5-8个字）
- `[位置]`：根据画面构图选择（参考位置选择原则）

---

**相关案例**：
- [案例 001：微信公众号君子兰封面](./case-001-wechat-cover.md)
- [案例 002：小红书多肉养护封面（带文字）](./case-002-xhs-cover.md)

**返回**：[案例库索引](./README.md)
