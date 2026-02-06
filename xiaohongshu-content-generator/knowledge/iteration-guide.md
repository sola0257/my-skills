# 迭代实施指南

如何安全、高效地迭代 Prompt Optimizer Integration 系统。

---

## 迭代原则

### 1. 向后兼容优先
- 所有 v1.x.x 版本必须保持 API 兼容
- 不能改变现有函数的签名和返回值
- 新功能通过可选参数添加

### 2. 测试先行
- 每次修改前先运行测试套件
- 添加新功能时同步添加测试用例
- 修改后再次运行测试确保无回归

### 3. 文档同步更新
- 代码修改后立即更新文档
- 保持 VERSION.md 和 ITERATION_LOG.md 同步
- 更新使用指南中的示例

---

## 迭代流程（10步）

### Step 1: 发现问题/需求
- 来源：用户反馈、使用过程中发现的问题、新的需求
- 记录：在 ITERATION_LOG.md 的"待处理"部分添加记录
- 评估：标注优先级（高/中/低）和预期收益

### Step 2: 设计方案
- 分析：问题的根本原因是什么？
- 方案：有哪些可能的解决方案？
- 选择：哪个方案最优（考虑成本、收益、兼容性）？
- 文档：在 ITERATION_LOG.md 中记录设计思路

### Step 3: 运行现有测试
```bash
cd /Users/dj/Desktop/小静的skills/xiaohongshu-content-generator/scripts
python3 test_prompt_optimizer_integration.py
```
- 确保所有测试通过
- 如果有失败，先修复再继续

### Step 4: 实现功能
- 修改 `prompt_optimizer_integration.py`
- 遵循现有代码风格
- 添加必要的注释和文档字符串

### Step 5: 添加测试用例
- 在 `test_prompt_optimizer_integration.py` 中添加新的测试
- 测试新功能的正常情况
- 测试边界情况和异常情况

### Step 6: 运行测试
```bash
python3 test_prompt_optimizer_integration.py
```
- 确保所有测试（包括新测试）通过
- 如果失败，修复后重新测试

### Step 7: 更新文档
- 更新 `prompt-optimizer-integration-guide.md`
- 添加新功能的使用示例
- 更新 API 文档

### Step 8: 更新版本信息
- 根据修改类型确定版本号：
  - Bug 修复 → Patch 版本（v1.0.0 → v1.0.1）
  - 新功能 → Minor 版本（v1.0.0 → v1.1.0）
  - 重大改动 → Major 版本（v1.0.0 → v2.0.0）
- 更新 VERSION.md
- 更新 ITERATION_LOG.md（移到"已完成"）

### Step 9: 提交变更
- 如果使用 Git，创建有意义的 commit message
- 示例：`feat: 添加质量评分机制 (v1.1.0)`

### Step 10: 通知用户
- 如果是重要更新，通知使用者
- 提供升级指南（如果需要）

---

## 常见迭代场景

### 场景1: 修复 Bug

**示例**：发现某个函数在特定情况下返回错误结果

```bash
# 1. 记录问题
# 在 ITERATION_LOG.md 添加记录

# 2. 运行测试（应该能复现问题）
python3 test_prompt_optimizer_integration.py

# 3. 修复代码
# 编辑 prompt_optimizer_integration.py

# 4. 添加测试用例（防止回归）
# 编辑 test_prompt_optimizer_integration.py

# 5. 运行测试（确保修复）
python3 test_prompt_optimizer_integration.py

# 6. 更新版本（Patch）
# v1.0.0 → v1.0.1
```

### 场景2: 添加新功能

**示例**：添加质量评分机制

```python
# 1. 在 prompt_optimizer_integration.py 中添加新方法
class PromptOptimizerIntegration:
    def evaluate_quality(self, optimized_prompt: str) -> int:
        """
        评估优化后提示词的质量（0-100分）

        Args:
            optimized_prompt: 优化后的提示词

        Returns:
            质量分数（0-100）
        """
        score = 0

        # 检查是否包含三层内容
        if "Role:" in optimized_prompt:
            score += 30
        if "执行规则与检查清单" in optimized_prompt:
            score += 40
        if "个性化要求" in optimized_prompt:
            score += 30

        return score

# 2. 添加测试用例
def test_evaluate_quality(self):
    """测试质量评分"""
    print("\n📋 测试7: 质量评分")

    optimized = self.optimizer.optimize_content_prompt(
        "测试",
        include_checklists=['step0', 'step5']
    )

    score = self.optimizer.evaluate_quality(optimized)
    self.assert_true(score >= 90, f"质量分数应该 >= 90，实际: {score}")

# 3. 更新版本（Minor）
# v1.0.0 → v1.1.0
```

### 场景3: 扩展到新平台

**示例**：支持微信公众号

```python
# 1. 添加微信相关的检查清单路径
class PromptOptimizerIntegration:
    def __init__(self, skill_path: str = None):
        # ... 现有代码 ...

        # 微信公众号检查清单
        self.wechat_checklist_path = self.skill_path / "knowledge/wechat-checklist.md"

# 2. 添加微信优化方法
    def optimize_wechat_content_prompt(
        self,
        original_prompt: str
    ) -> str:
        """优化微信公众号内容提示词"""
        return self.optimize_content_prompt(
            original_prompt,
            include_checklists=['wechat']
        )

# 3. 更新版本（Minor）
# v1.1.0 → v1.2.0
```

### 场景4: 重大架构调整

**示例**：插件化架构

```python
# 1. 设计新的插件系统
class ChecklistPlugin:
    """检查清单插件基类"""
    def load(self) -> str:
        raise NotImplementedError

class PromptOptimizerIntegration:
    def __init__(self):
        self.plugins = {}

    def register_plugin(self, name: str, plugin: ChecklistPlugin):
        """注册插件"""
        self.plugins[name] = plugin

# 2. 提供迁移指南
# 在 VERSION.md 中添加从 v1.x.x 到 v2.0.0 的迁移步骤

# 3. 更新版本（Major）
# v1.2.0 → v2.0.0
```

---

## 质量检查清单

每次迭代完成后，检查以下项目：

- [ ] 所有测试通过
- [ ] 代码有适当的注释
- [ ] 文档已更新
- [ ] VERSION.md 已更新
- [ ] ITERATION_LOG.md 已更新
- [ ] 向后兼容性已验证（v1.x.x）
- [ ] 新功能有使用示例
- [ ] 边界情况已测试

---

## 回滚机制

如果新版本出现问题：

### 方法1: 使用 Git 回滚
```bash
git log  # 查看历史
git revert <commit-hash>  # 回滚到指定版本
```

### 方法2: 手动恢复
1. 从备份中恢复旧版本文件
2. 更新 VERSION.md 标注回滚
3. 在 ITERATION_LOG.md 记录回滚原因

---

## 性能优化建议

### 1. 缓存机制
```python
from functools import lru_cache

class PromptOptimizerIntegration:
    @lru_cache(maxsize=10)
    def _load_template_cached(self, template_path: str) -> str:
        """带缓存的模板加载"""
        return self._load_template(Path(template_path))
```

### 2. 延迟加载
```python
class PromptOptimizerIntegration:
    def __init__(self):
        self._text_template = None  # 延迟加载

    def get_text_template(self):
        if self._text_template is None:
            self._text_template = self._load_template(...)
        return self._text_template
```

### 3. 批量处理
```python
def optimize_batch(self, prompts: List[str]) -> List[str]:
    """批量优化提示词"""
    # 一次性加载模板和检查清单
    # 然后批量处理
    pass
```

---

## 常见问题

### Q: 如何确保向后兼容？
A:
1. 不修改现有函数签名
2. 新参数使用默认值
3. 运行完整测试套件
4. 保持 v1.x.x 系列的 API 稳定

### Q: 什么时候升级 Major 版本？
A:
- API 不兼容的修改
- 重大架构调整
- 删除已废弃的功能

### Q: 如何处理用户反馈？
A:
1. 记录到 ITERATION_LOG.md
2. 评估优先级和影响
3. 设计方案并征求意见
4. 按照迭代流程实施

---

**维护者**: Claude Code
**最后更新**: 2026-02-05
