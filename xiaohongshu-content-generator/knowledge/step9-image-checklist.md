# Step 9 配图生成检查清单

> 整合3个文档的核心要点
> 生成配图 prompt 前必须检查

---

## 一、强制执行流程（必须按顺序）

- [ ] **Step 1**: 读取正面案例库 `/Users/dj/Desktop/小静的skills/knowledge/xiaohongshu-mixed-style-image-case.md`
- [ ] **Step 2**: 读取反面案例库 `/Users/dj/Desktop/小静的skills/knowledge/image-generation-cases/anti-patterns.md`
- [ ] **Step 3**: 根据内容类型选择风格模板
- [ ] **Step 4**: 生成 prompt（按照模板）
- [ ] **Step 5**: 执行检查清单（15项）

**⚠️ 不得跳过任何一步，不得改变执行顺序**

---

## 二、配图规范

### 数量和尺寸
- [ ] 数量：12-15张（不得少于12张）
- [ ] 尺寸：1080x1440像素（3:4竖版）
- [ ] 命名：`序号_中文说明_风格标识.png`

### 风格选择（可混用）
- [ ] **dreamy-photo**（真实感）：场景类、生活类、细节特写
- [ ] **cozy-sketch**（手绘风）：教程类、步骤类、技巧类
- [ ] **infographic-sketch**（信息图）：科普类、知识类、对比类
- [ ] **soft-botanical**（水彩风）：情感类、心情类、治愈类
- [ ] **minimal-collage**（拼贴风）：产品类、推荐类、测评类

### 风格混用原则
- [ ] 封面：按通篇内容主题选择
- [ ] 正文：按对应段落内容类型选择
- [ ] 对比图 → infographic-sketch
- [ ] 步骤图 → cozy-sketch
- [ ] 细节图 → dreamy-photo
- [ ] 场景图 → dreamy-photo

---

## 三、小红书审美调性（强制约束）

### 颜色控制（必须严格遵守）
- [ ] 红色 → `dusty coral`, `muted rose`, `terracotta red`
- [ ] 粉色 → `blush pink`, `dusty pink`, `muted salmon`
- [ ] 橙色 → `burnt sienna`, `muted peach`, `soft terracotta`
- [ ] 绿色 → `sage green`, `eucalyptus`, `muted olive`

### 禁止的颜色表达
- [ ] 禁止：`bright red`, `vivid red`, `pure red`
- [ ] 禁止：`hot pink`, `neon pink`, `fuchsia`
- [ ] 禁止：`bright orange`, `vivid yellow`
- [ ] 禁止：`neon green`, `lime green`
- [ ] 禁止：任何 `bright`, `vivid`, `neon`, `pure` 颜色

### 真实感约束（每个 prompt 必须包含）
- [ ] `authentic home environment`
- [ ] `lived-in atmosphere`
- [ ] `natural imperfections`
- [ ] `realistic indoor lighting`
- [ ] `NOT overly stylized AI art`

### 颜色约束（每个 prompt 必须包含）
- [ ] `desaturated color palette`
- [ ] `muted tones throughout`
- [ ] `low saturation, high-end aesthetic`
- [ ] `Morandi color scheme`

### 现代家居风格约束（每个 prompt 必须包含）
- [ ] `modern home aesthetic`
- [ ] `clean and well-maintained interior`
- [ ] `NOT old or worn-out interior`
- [ ] `contemporary living space`

---

## 四、Prompt 生成检查清单（15项）

### 基础约束
- [ ] 是否包含饱和度控制词（`muted`, `desaturated`, `dusty`）？
- [ ] 是否避免了禁止词汇（`bright`, `vivid`, `neon`）？
- [ ] 是否包含真实感约束（`lived-in`, `natural light`）？
- [ ] 是否有生活化场景（不是纯白背景/棚拍）？
- [ ] 红色系是否使用替代词（`dusty coral`, `terracotta`）？

### 强制约束
- [ ] 是否包含 `NO ENGLISH TEXT` 约束？（强制）
- [ ] 是否包含 `NO PEOPLE` 约束？（如果不需要人物）
- [ ] 是否包含 `NO STUDIO LIGHTING` 约束？（真实感要求）
- [ ] 是否包含现代家居风格约束？（`modern home aesthetic`, `clean and well-maintained interior`, `NOT old or worn-out interior`）
- [ ] 是否包含 `NOT overly stylized AI art` 约束？（减少AI感）

### 内容逻辑
- [ ] 信息图/手绘图的中文内容是否直接写在 prompt 中？（不能只写英文描述）
- [ ] 内容是否与主题直接相关？（如"光照管理"必须展示植物与光照的关系）
- [ ] 如果展示植物的某个部分（如根、叶），植物本体是否可见？（避免只看到局部）
- [ ] 对比图的对比点是否准确？（如"风格搭配"不是"位置选择"）
- [ ] 场景细节是否合理？（如地板无异常脚印、家具摆放合理）

---

## 五、文字处理规范

### 真实感图片（dreamy-photo）
- [ ] 使用 Gemini 模型，在 prompt 中添加 `Text overlay` 指令
- [ ] 文字风格：自然手写风格，柔和的奶油色或淡玫瑰色
- [ ] 文字位置：`upper left corner`, `upper right corner`, `lower left corner`, `lower right corner`, `lower center`
- [ ] 命名格式：`序号_图片上的文字_真实图.png`（中文说明必须与图片上叠加的文字内容一致）

### 信息图（infographic-sketch）
- [ ] 使用 Gemini 模型，在 prompt 中直接包含中文内容
- [ ] 文字样式：清晰的手写风格字体（类似马克笔或毛笔字）
- [ ] 文字要求：笔画清晰、易读
- [ ] 命名格式：`序号_内容描述_信息图.png`（中文说明是图片内容的简短描述）

### 手绘教程（cozy-sketch）
- [ ] 使用 Gemini 模型，在 prompt 中直接包含中文内容
- [ ] 文字样式：清晰的手写风格字体
- [ ] 文字要求：笔画清晰、易读
- [ ] 命名格式：`序号_内容描述_手绘图.png`（中文说明是图片内容的简短描述）

---

## 六、反面案例（必须避免）

### 坚决不要生成的效果
- [ ] 英文标注（如 "Healthy" "Unhealthy"）
- [ ] AI感太重（过于完美、不真实）
- [ ] 逻辑错误（如只看到根部，看不到植物本体）
- [ ] 家居风格破旧（老旧、磨损的家具）
- [ ] 场景细节不合理（如地板有异常脚印）
- [ ] 对比图对比点不准确（如"风格搭配"变成"位置选择"）

### 商品展示风（必须避免）
- [ ] 避免：`bright studio lighting`（商品图质感）
- [ ] 避免：`product photography`（不是生活图）
- [ ] 避免：`vibrant red`（颜色过饱和）
- [ ] 避免：`clean white background`（缺少生活场景）

---

## 七、技术参数

### API 配置
- [ ] API 端点：`https://yunwu.ai/v1`
- [ ] 默认模型：`gemini-3-pro-image-preview`（适用于90%的场景）
- [ ] 响应格式：Base64（需要正则提取）

### 模型选择规则
- [ ] 真实感照片 → `gemini-3-pro-image-preview`
- [ ] 手绘风格 → `gemini-3-pro-image-preview`
- [ ] 信息图表 → `gemini-3-pro-image-preview`
- [ ] 艺术风格 → `dall-e-3`（特殊场景）

---

## 八、执行检查（生成后）

- [ ] 是否读取了正面案例库？
- [ ] 是否读取了反面案例库？
- [ ] 是否按照模板生成 prompt？
- [ ] 是否完成了15项检查清单？
- [ ] 是否符合小红书审美调性？
- [ ] 是否避免了反面案例中的错误？
- [ ] 文件命名是否符合规范？
- [ ] 配图数量是否≥12张？
