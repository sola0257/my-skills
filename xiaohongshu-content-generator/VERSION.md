# Prompt Optimizer Integration - 版本管理

## 当前版本

**v1.0.0** (2026-02-05)

---

## 版本号规则（语义化版本）

- **主版本号 (Major)**: 不兼容的 API 修改
- **次版本号 (Minor)**: 向下兼容的功能性新增
- **修订号 (Patch)**: 向下兼容的问题修正

示例：
- v1.0.0 → v1.0.1: 修复 bug
- v1.0.0 → v1.1.0: 新增功能（兼容旧版）
- v1.0.0 → v2.0.0: 重大改动（可能不兼容）

---

## 版本历史

### v1.0.0 (2026-02-05) - 初始版本

**新增功能**:
- ✅ 三层架构整合（结构层 + 约束层 + 价值层）
- ✅ 文本提示词优化（`optimize_content_prompt`）
- ✅ 图像提示词优化（`optimize_image_prompt`）
- ✅ 便捷函数（`optimize_xiaohongshu_content_prompt`, `optimize_xiaohongshu_image_prompt`）
- ✅ 完整的使用指南和测试代码

**依赖**:
- Prompt Templates: text-optimize v1.3.0, image-optimize v1.3.0
- Checklists: step0, step5, step9 (2026-02-05)

**已知问题**:
- 无

---

## 迭代计划

### v1.1.0 (计划中) - 功能增强
- [ ] 添加质量评分机制
- [ ] 支持自定义检查清单
- [ ] 添加缓存机制提升性能

### v1.2.0 (计划中) - 多平台支持
- [ ] 扩展到微信公众号
- [ ] 扩展到视频号
- [ ] 统一的平台配置管理

### v2.0.0 (计划中) - 架构升级
- [ ] 插件化架构
- [ ] 动态加载检查清单
- [ ] API 重构

---

## 向后兼容性保证

**v1.x.x 系列承诺**:
- 所有 v1.x.x 版本保持 API 兼容
- 函数签名不会改变
- 返回值格式不会改变
- 配置文件格式不会改变

**升级到 v2.0.0 时**:
- 提供迁移指南
- 保留 v1.x.x 兼容模式
- 至少提前1个月通知

---

## 如何查看当前版本

```python
from prompt_optimizer_integration import PromptOptimizerIntegration

optimizer = PromptOptimizerIntegration()
print(optimizer.__version__)  # 输出: 1.0.0
```

---

**维护者**: Claude Code
**最后更新**: 2026-02-05
