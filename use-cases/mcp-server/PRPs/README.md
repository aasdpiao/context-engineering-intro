# 产品需求提示（PRP）概念

"过度指定要构建什么，同时对上下文和如何构建指定不足，这就是为什么许多 AI 驱动的编码尝试在 80% 处停滞不前的原因。产品需求提示（PRP）通过将经典产品需求文档（PRD）的严格范围与现代提示工程的'上下文为王'思维相融合来解决这个问题。"

## 什么是 PRP？

产品需求提示（PRP）
PRP 是一个结构化提示，为 AI 编码代理提供交付工作软件垂直切片所需的一切——不多不少。

### 它与 PRD 的区别

传统的 PRD 阐明产品必须做什么以及客户为什么需要它，但故意避免如何构建它。

PRP 保留了 PRD 的目标和理由部分，但添加了三个对 AI 至关重要的层次：

### 上下文

- 精确的文件路径和内容、库版本和库上下文、代码片段示例。当给出直接的提示内参考而不是宽泛的描述时，LLM 会生成更高质量的代码。使用 ai_docs/ 目录来导入库和其他文档。

### 实现细节和策略

- 与传统 PRD 相比，PRP 明确说明产品将如何构建。这包括使用 API 端点、测试运行器或代理模式（ReAct、计划和执行）。使用类型提示、依赖项、架构模式和其他工具来确保代码正确构建。

### 验证门控

- 确定性检查，如 pytest、ruff 或静态类型检查，"左移"质量控制可以早期发现缺陷，比后期返工更便宜。
  示例：每个新函数都应该单独测试，验证门控 = 所有测试通过。

### PRP 层存在的原因

- PRP 文件夹用于准备和向代理编码器传输 PRP。

## 为什么上下文是不可协商的

大语言模型的输出受其上下文窗口限制；无关或缺失的上下文会字面上挤压有用的标记

行业格言"垃圾进→垃圾出"在提示工程中加倍适用，特别是在代理工程中：草率的输入产生脆弱的代码

## 简而言之

PRP 是 PRD + 精选代码库智能 + 代理/运行手册——AI 在第一次尝试中合理交付生产就绪代码所需的最小可行包。

PRP 可以很小并专注于单个任务，也可以很大并涵盖多个任务。
PRP 的真正力量在于能够在 PRP 中将任务链接在一起，以构建、自我验证和交付复杂功能。
