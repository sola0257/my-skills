# 通用项目迭代机制模板

**适用范围**: 任何需要持续迭代的项目（Skills、可视化平台、工具脚本等）

---

## 快速部署（5分钟）

### Step 1: 复制4个核心文件

```bash
# 在你的项目目录下创建这4个文件
touch VERSION.md
touch ITERATION_LOG.md
touch tests/test_main.py  # 或 scripts/test_xxx.py
touch docs/iteration-guide.md
```

### Step 2: 填充模板内容

#### VERSION.md 模板
```markdown
# [项目名称] - 版本管理

## 当前版本
**v1.0.0** (YYYY-MM-DD)

## 版本号规则
- Major: 不兼容的重大改动
- Minor: 向下兼容的新功能
- Patch: 向下兼容的问题修复

## 版本历史
### v1.0.0 (YYYY-MM-DD) - 初始版本
- ✅ 核心功能1
- ✅ 核心功能2
```

#### ITERATION_LOG.md 模板
```markdown
# 迭代日志

## 待处理 (Backlog)
*记录所有想法和需求*

## 进行中 (In Progress)
*当前正在开发的功能*

## 已完成 (Completed)
### v1.0.0 (YYYY-MM-DD)
- ✅ 初始版本发布
```

#### test_main.py 模板
```python
#!/usr/bin/env python3
"""自动化测试套件"""

class TestProject:
    def __init__(self):
        self.passed = 0
        self.failed = 0

    def test_basic_functionality(self):
        """测试基本功能"""
        print("📋 测试1: 基本功能")
        # 添加你的测试逻辑
        assert True, "基本功能正常"
        self.passed += 1

    def run_all_tests(self):
        """运行所有测试"""
        print("=" * 80)
        print("🧪 自动化测试")
        print("=" * 80)

        self.test_basic_functionality()

        print(f"\n✅ 通过: {self.passed}")
        print(f"❌ 失败: {self.failed}")

        return self.failed == 0

if __name__ == "__main__":
    tester = TestProject()
    success = tester.run_all_tests()
    exit(0 if success else 1)
```

#### iteration-guide.md 模板
```markdown
# 迭代实施指南

## 10步迭代流程

1. 发现问题/需求 → 记录到 ITERATION_LOG.md
2. 设计方案
3. 运行现有测试
4. 实现功能
5. 添加测试用例
6. 运行测试
7. 更新文档
8. 更新版本信息
9. 提交变更（如果使用Git）
10. 通知用户

## 常见场景

### 场景1: 修复Bug
- 记录问题 → 修复 → 测试 → 更新版本（Patch）

### 场景2: 添加功能
- 设计方案 → 实现 → 测试 → 更新版本（Minor）

### 场景3: 重大改动
- 设计方案 → 征求意见 → 实现 → 测试 → 更新版本（Major）
```

---

## 项目类型适配

### 类型1: Python 项目（如 Skills）
```
project/
├── VERSION.md
├── ITERATION_LOG.md
├── scripts/
│   ├── main.py
│   └── test_main.py
└── docs/
    └── iteration-guide.md
```

### 类型2: Web 项目（如可视化平台）
```
project/
├── VERSION.md
├── ITERATION_LOG.md
├── backend/
│   └── tests/
│       └── test_api.py
├── frontend/
│   └── tests/
│       └── test_components.js
└── docs/
    └── iteration-guide.md
```

### 类型3: 文档项目
```
project/
├── VERSION.md
├── ITERATION_LOG.md
└── docs/
    ├── content.md
    └── iteration-guide.md
```

---

## 核心原则（适用所有项目）

### 1. 版本管理
- 使用语义化版本号
- 记录每个版本的变更

### 2. 测试保障
- 每次修改前后都运行测试
- 新功能必须有测试用例

### 3. 文档同步
- 代码改了，文档也要改
- 保持 VERSION.md 和 ITERATION_LOG.md 同步

### 4. 向后兼容
- v1.x.x 系列保持兼容
- 重大改动升级 Major 版本

---

## 快速检查清单

每次迭代完成后检查：
- [ ] 测试通过
- [ ] 文档更新
- [ ] VERSION.md 更新
- [ ] ITERATION_LOG.md 更新
- [ ] 向后兼容性验证（如果是 v1.x.x）

---

## 示例项目

### 示例1: xiaohongshu-content-generator
- 已实现完整的迭代机制
- 参考路径：`/Users/dj/Desktop/小静的skills/xiaohongshu-content-generator/`

### 示例2: 可视化管理平台（即将实现）
- 将使用相同的迭代机制
- 适配 Web 项目的特点

---

## AI 辅助

当你说以下内容时，我会自动帮你：
- "我想添加XX功能" → 引导你完成10步流程
- "我发现了一个问题" → 帮你记录到 ITERATION_LOG.md
- "帮我整理迭代日志" → 整理和分类你的想法
- "运行测试" → 执行测试并分析结果

---

**维护者**: Claude Code
**最后更新**: 2026-02-05
