# 🏭 智能内容生产流水线

## 概述

这是一个混合模式的内容生产自动化系统，结合了 **组合 Skill** 和 **Sub-agent** 的优势。

## 核心特性

### ✅ 已实现（v1.0）
- 选题发现 → 小红书内容生成
- 批量处理（最多10个选题）
- 进度追踪（TodoWrite）
- 错误恢复和日志
- 执行报告生成

### 🚧 待实现
- 公众号内容生成集成
- 视频脚本生成集成
- 并发优化
- 智能选题筛选

## 快速开始

### 基础用法
```bash
# 在 Claude Code 中
/content-production-pipeline 家居绿植
```

### 高级用法
```bash
# 指定平台
/content-production-pipeline 办公室绿植 --platforms xhs,wechat

# 指定数量
/content-production-pipeline 懒人养花 --count 3

# 全平台
/content-production-pipeline 送礼推荐 --platforms all
```

## 工作流程

```
用户输入关键词
    ↓
Phase 1: 选题发现 (topic-discovery skill)
    ↓
Phase 2: 小红书内容生成 (xiaohongshu-content-generator skill)
    ↓ [可选]
Phase 3: 公众号内容生成 (wechat-content-generator skill)
    ↓ [可选]
Phase 4: 视频脚本生成 (video-script skill)
    ↓
生成执行报告
```

## 混合模式说明

### 组合 Skill 部分
- 主流程控制
- Skill 之间的协调
- 数据传递和转换
- 进度追踪和报告

### Sub-agent 部分（未来扩展）
- 资料搜索和分析
- 趋势洞察
- 内容质量评估
- 智能优化建议

## 输出结构

```
/Users/dj/Documents/slowseasons AI工厂/
├── 选题库/
│   └── 2026-01-14_家居绿植_选题报告.md
├── 内容发布/发布记录/2026/
│   ├── 小红书/
│   │   ├── 2026-01-14_选题1/
│   │   │   ├── 文案.md
│   │   │   ├── 封面.png
│   │   │   └── 配图_01-05.png
│   │   └── ...
│   ├── 订阅号/
│   │   └── ...
│   └── pipeline_report_20260114.md
```

## 依赖

- topic-discovery (v3.0+)
- xiaohongshu-content-generator (v4.0+)
- wechat-content-generator (v3.0+)
- 视频脚本 skill（待集成）

## 性能指标

- **执行时间**：30-60分钟（10个选题）
- **成功率目标**：>90%
- **并发能力**：串行执行（避免API限流）
- **存储需求**：约 100-200MB（10个选题）

## 错误处理

- 单个选题失败不影响整体
- 自动重试机制（最多3次）
- 详细错误日志
- 执行报告包含失败原因

## 版本历史

### v1.0 (2026-01-14)
- 初始版本
- 支持选题发现 + 小红书内容生成
- 支持批量处理和进度追踪

## 路线图

### v1.1（计划中）
- [ ] 集成公众号内容生成
- [ ] 智能选题筛选
- [ ] 执行时间优化

### v1.2（计划中）
- [ ] 集成视频脚本生成
- [ ] 并发优化
- [ ] Sub-agent 集成（资料搜索）

### v2.0（未来）
- [ ] 内容质量评估
- [ ] 智能优化建议
- [ ] 多账号管理
- [ ] 定时发布

## 贡献

欢迎提出改进建议和功能需求！

## 许可

MIT License
