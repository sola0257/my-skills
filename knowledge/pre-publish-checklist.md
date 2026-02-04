# 推送前检查清单（微信公众号）

> **适用范围**: wechat-content-generator
> **更新日期**: 2026-02-04
> **版本**: v1.0

---

## 一、核心原则

**推送前必须进行全面检查,确保内容、配图、参数都符合规范**

**执行时机**: 保存文件后、推送前

**强制停止机制**: 如果检查失败 → 不推送,输出失败原因

---

## 二、检查项目

### 检查1: 文件完整性

**检查内容**:
- [ ] 内容文件存在且可读
- [ ] 配图文件全部存在
- [ ] 配图数量符合要求
- [ ] 文件路径正确

**检查方法**:
```python
# 伪代码
def check_file_integrity(content_dir):
    # 检查内容文件
    content_file = f"{content_dir}/content.md"
    if not os.path.exists(content_file):
        return False, "内容文件不存在"

    # 检查配图文件
    images_dir = f"{content_dir}/images"
    if not os.path.exists(images_dir):
        return False, "配图目录不存在"

    images = os.listdir(images_dir)
    if len(images) == 0:
        return False, "没有配图文件"

    return True, "文件完整性检查通过"
```

**失败处理**:
- 输出具体的缺失文件
- 不推送
- 提示用户检查文件

---

### 检查2: 配图规范

**检查内容**:
- [ ] 封面图尺寸正确
- [ ] 正文配图尺寸正确
- [ ] 配图格式正确（PNG/JPG）
- [ ] 配图文件大小合理（<2MB）

**尺寸要求**:
- 长文格式封面: 900×383像素 (2.35:1)
- 长文格式正文: 900×506像素 (16:9)
- 图文格式: 1080×1440像素 (3:4)

**检查方法**:
```python
# 伪代码
from PIL import Image

def check_image_specs(image_path, expected_size):
    img = Image.open(image_path)
    width, height = img.size

    if (width, height) != expected_size:
        return False, f"尺寸不符: {width}×{height}, 期望: {expected_size}"

    if img.format not in ['PNG', 'JPEG']:
        return False, f"格式不符: {img.format}, 期望: PNG/JPEG"

    file_size = os.path.getsize(image_path)
    if file_size > 2 * 1024 * 1024:  # 2MB
        return False, f"文件过大: {file_size / 1024 / 1024:.2f}MB"

    return True, "配图规范检查通过"
```

**失败处理**:
- 输出不符合规范的配图
- 不推送
- 提示用户重新生成配图

---

### 检查3: 推送参数

**检查内容**:
- [ ] 标题不为空
- [ ] 标题长度合理（<64字符）
- [ ] 作者信息正确
- [ ] 摘要不为空（如果有）
- [ ] 内容不为空

**检查方法**:
```python
# 伪代码
def check_publish_params(params):
    if not params.get('title'):
        return False, "标题不能为空"

    if len(params['title']) > 64:
        return False, f"标题过长: {len(params['title'])}字符, 最多64字符"

    if not params.get('content'):
        return False, "内容不能为空"

    if not params.get('author'):
        return False, "作者信息不能为空"

    return True, "推送参数检查通过"
```

**失败处理**:
- 输出不符合要求的参数
- 不推送
- 提示用户修正参数

---

### 检查4: 推送脚本验证

**检查内容**:
- [ ] 推送脚本存在
- [ ] 推送脚本可执行
- [ ] 环境变量配置正确
- [ ] API 凭证有效

**检查方法**:
```python
# 伪代码
def check_publish_script():
    script_path = "/Users/dj/Desktop/小静的skills/wechat-content-generator/scripts/wechat_publish.py"

    if not os.path.exists(script_path):
        return False, "推送脚本不存在"

    if not os.access(script_path, os.X_OK):
        return False, "推送脚本不可执行"

    # 检查环境变量
    if not os.getenv('WECHAT_APP_ID'):
        return False, "缺少环境变量: WECHAT_APP_ID"

    if not os.getenv('WECHAT_APP_SECRET'):
        return False, "缺少环境变量: WECHAT_APP_SECRET"

    return True, "推送脚本验证通过"
```

**失败处理**:
- 输出具体的问题
- 不推送
- 提示用户配置环境

---

### 检查5: 内容质量（快速检查）

**检查内容**:
- [ ] 内容长度合理（>500字）
- [ ] 没有明显的格式错误
- [ ] 没有未替换的占位符
- [ ] 违禁词检查通过（应该在之前已完成）

**检查方法**:
```python
# 伪代码
def check_content_quality(content):
    if len(content) < 500:
        return False, f"内容过短: {len(content)}字符, 建议>500字"

    # 检查占位符
    placeholders = ['[TODO]', '[待补充]', '[XXX]', '{{', '}}']
    for placeholder in placeholders:
        if placeholder in content:
            return False, f"发现未替换的占位符: {placeholder}"

    return True, "内容质量检查通过"
```

**失败处理**:
- 输出具体的问题
- 不推送
- 提示用户修正内容

---

## 三、执行流程

### Step 1: 执行所有检查

**顺序**:
1. 文件完整性检查
2. 配图规范检查
3. 推送参数检查
4. 推送脚本验证
5. 内容质量检查

**逻辑**:
- 所有检查都通过 → 继续推送
- 任何一个检查失败 → 停止,输出失败原因

### Step 2: 输出检查结果

**格式**:
```markdown
## 推送前检查

✅ 文件完整性: 通过
✅ 配图规范: 通过
✅ 推送参数: 通过
✅ 推送脚本: 通过
✅ 内容质量: 通过

所有检查通过,可以推送。
```

**如果有失败**:
```markdown
## 推送前检查

✅ 文件完整性: 通过
❌ 配图规范: 失败
   - 封面图尺寸不符: 1080×1440, 期望: 900×383
✅ 推送参数: 通过
✅ 推送脚本: 通过
✅ 内容质量: 通过

检查失败,无法推送。请修正后重试。
```

### Step 3: 决定是否推送

**通过**: 继续执行推送

**失败**: 停止,不推送

---

## 四、执行检查清单

执行 Step 11 前,确认:
- [ ] 已保存所有文件
- [ ] 已准备好推送参数
- [ ] 已执行所有检查项目
- [ ] 已输出检查结果
- [ ] 如果检查失败,已停止推送

---

## 五、常见问题

**Q: 如果只有一个检查项失败,其他都通过,可以推送吗?**
A: 不可以。所有检查项都必须通过才能推送。

**Q: 检查失败后,修正问题,需要重新执行所有检查吗?**
A: 是的。修正后需要重新执行 Step 11,确保所有检查都通过。

**Q: 违禁词检查应该在哪里执行?**
A: 违禁词检查应该在 Step 7 执行,不是在 Step 11。Step 11 只是快速检查是否有明显的问题。

**Q: 如果推送脚本验证失败,是不是说明环境配置有问题?**
A: 是的。需要检查环境变量配置,确保 API 凭证正确。

---

## 六、与其他步骤的关系

**Step 10: 保存文件** → **Step 11: 推送前检查** → **Step 12: 推送草稿箱**

**依赖关系**:
- Step 11 依赖 Step 10 (需要文件已保存)
- Step 12 依赖 Step 11 (需要检查通过)

**如果 Step 11 失败**:
- 不执行 Step 12
- 返回到相应的步骤修正问题
- 重新执行 Step 11

---

## 七、检查脚本

**脚本路径**: `/Users/dj/Desktop/小静的skills/wechat-content-generator/scripts/pre_publish_check.py`

**功能**:
- 执行所有检查项目
- 输出检查结果
- 返回通过/失败状态

**使用方法**:
```bash
python pre_publish_check.py --content-dir /path/to/content
```

**输出**:
```json
{
  "status": "pass",  // or "fail"
  "checks": {
    "file_integrity": {"pass": true, "message": "文件完整性检查通过"},
    "image_specs": {"pass": true, "message": "配图规范检查通过"},
    "publish_params": {"pass": true, "message": "推送参数检查通过"},
    "script_validation": {"pass": true, "message": "推送脚本验证通过"},
    "content_quality": {"pass": true, "message": "内容质量检查通过"}
  }
}
```

---

## 八、相关文件

- 推送脚本: `/Users/dj/Desktop/小静的skills/wechat-content-generator/scripts/wechat_publish.py`
- 检查脚本: `/Users/dj/Desktop/小静的skills/wechat-content-generator/scripts/pre_publish_check.py`
- 配图规范: `/Users/dj/Desktop/小静的skills/wechat-content-generator/knowledge/wechat-image-prompt-guide.md`
- 违禁词检查: 使用 `compliance-checker` skill
