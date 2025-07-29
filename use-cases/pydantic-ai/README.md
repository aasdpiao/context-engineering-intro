# Pydantic AI 上下文工程模板

一个全面的模板，用于使用 Pydantic AI 构建生产级 AI 代理，结合上下文工程最佳实践、工具集成、结构化输出和全面的测试模式。

## 🚀 快速开始 - 复制模板

**2分钟内开始使用：**

```bash
# 克隆上下文工程仓库
git clone https://github.com/coleam00/Context-Engineering-Intro.git
cd Context-Engineering-Intro/use-cases/pydantic-ai

# 1. 将此模板复制到您的新项目
python copy_template.py /path/to/my-agent-project

# 2. 导航到您的项目
cd /path/to/my-agent-project

# 3. 使用 PRP 工作流开始构建
# 在 PRPs/INITIAL.md 中填写您想要创建的代理

# 4. 根据您的详细需求生成 PRP（生成后验证 PRP！）
/generate-pydantic-ai-prp PRPs/INITIAL.md

# 5. 执行 PRP 以创建您的 Pydantic AI 代理
/execute-pydantic-ai-prp PRPs/generated_prp.md
```

如果您没有使用 Claude Code，您可以简单地告诉您的 AI 编码助手使用 .claude/commands 中的 generate-pydantic-ai-prp 和 execute-pydantic-ai-prp 斜杠命令作为提示。

## 📖 这个模板是什么？

此模板提供了使用经过验证的上下文工程工作流构建复杂 Pydantic AI 代理所需的一切。它结合了：

- **Pydantic AI 最佳实践**：具有工具、结构化输出和依赖注入的类型安全代理
- **上下文工程工作流**：经过验证的 PRP（产品需求提示）方法论
- **工作示例**：您可以学习和扩展的完整代理实现

## 🎯 PRP 框架工作流

此模板使用 3 步上下文工程工作流来构建 AI 代理：

### 1. **定义需求** (`PRPs/INITIAL.md`)
首先清楚地定义您的代理需要做什么：
```markdown
# 客户支持代理 - 初始需求

## 概述
构建一个智能客户支持代理，可以处理询问、
访问客户数据，并适当地升级问题。

## 核心需求
- 具有上下文和记忆的多轮对话
- 客户认证和账户访问
- 账户余额和交易查询
- 支付处理和退款处理
...
```

### 2. **生成实现计划** 
```bash
/generate-pydantic-ai-prp PRPs/INITIAL.md
```
这将创建一个全面的"产品需求提示"文档，包括：
- Pydantic AI 技术研究和最佳实践
- 具有工具和依赖项的代理架构设计
- 带有验证循环的实现路线图
- 安全模式和生产考虑因素

### 3. **执行实现**
```bash
/execute-pydantic-ai-prp PRPs/your_agent.md
```
这将基于 PRP 实现完整的代理，包括：
- 使用适当的模型提供商配置创建代理
- 具有错误处理和验证的工具集成
- 使用 Pydantic 验证的结构化输出模型
- 使用 TestModel 和 FunctionModel 进行全面测试

## 📂 模板结构

```
pydantic-ai/
├── CLAUDE.md                           # Pydantic AI 全局开发规则
├── copy_template.py                    # 模板部署脚本
├── .claude/commands/
│   ├── generate-pydantic-ai-prp.md     # 代理的 PRP 生成
│   └── execute-pydantic-ai-prp.md      # 代理的 PRP 执行
├── PRPs/
│   ├── templates/
│   │   └── prp_pydantic_ai_base.md     # 代理的基础 PRP 模板
│   └── INITIAL.md                      # 示例代理需求
├── examples/
│   ├── basic_chat_agent/               # 简单对话代理
│   │   ├── agent.py                    # 具有记忆和上下文的代理
│   │   └── README.md                   # 使用指南
│   ├── tool_enabled_agent/             # 具有外部工具的代理
│   │   ├── agent.py                    # 网络搜索 + 计算器工具
│   │   └── requirements.txt            # 依赖项
│   └── testing_examples/               # 全面的测试模式
│       ├── test_agent_patterns.py      # TestModel、FunctionModel 示例
│       └── pytest.ini                  # 测试配置
└── README.md                           # 此文件
```

## 🤖 包含的代理示例

### 1. 主代理参考 (`examples/main_agent_reference/`)
**规范的参考实现**，展示了正确的 Pydantic AI 模式：
- 使用 `settings.py` 和 `providers.py` 的基于环境的配置
- 邮件和研究代理之间的清晰关注点分离
- 适当的文件结构来分离提示、工具、代理和 Pydantic 模型
- 与外部 API（Gmail、Brave Search）的工具集成

**关键文件：**
- `settings.py`：使用 pydantic-settings 的环境配置
- `providers.py`：使用 `get_llm_model()` 的模型提供商抽象
- `research_agent.py`：具有网络搜索和邮件集成的多工具代理
- `email_agent.py`：用于 Gmail 草稿创建的专用代理

### 2. 基础聊天代理 (`examples/basic_chat_agent/`)
一个演示核心模式的简单对话代理：
- **基于环境的模型配置**（遵循 main_agent_reference）
- **默认字符串输出**（除非需要，否则不使用 `result_type`）
- 系统提示（静态和动态）
- 具有依赖注入的对话记忆

**关键特性：**
- 简单的字符串响应（非结构化输出）
- 基于设置的配置模式
- 对话上下文跟踪
- 清洁、最小化的实现

### 3. 工具启用代理 (`examples/tool_enabled_agent/`)
具有工具集成能力的代理：
- **基于环境的配置**（遵循 main_agent_reference）
- **默认字符串输出**（无不必要的结构）
- 网络搜索和计算工具
- 错误处理和重试机制

**关键特性：**
- `@agent.tool` 装饰器模式
- 用于依赖注入的 RunContext
- 工具错误处理和恢复
- 来自工具的简单字符串响应

### 4. 结构化输出代理 (`examples/structured_output_agent/`)
**新增**：展示何时使用 `result_type` 进行数据验证：
- **基于环境的配置**（遵循 main_agent_reference）
- **使用 Pydantic 验证的结构化输出**（在特别需要时）
- 使用统计工具进行数据分析
- 专业报告生成

**关键特性：**
- 演示 `result_type` 的正确使用
- 用于业务报告的 Pydantic 验证
- 具有数值统计的数据分析工具
- 关于何时使用结构化与字符串输出的清晰文档

### 5. 测试示例 (`examples/testing_examples/`)
Pydantic AI 代理的全面测试模式：
- 用于快速开发验证的 TestModel
- 用于自定义行为测试的 FunctionModel
- 用于测试隔离的 Agent.override()
- Pytest 夹具和异步测试

**关键特性：**
- 无 API 成本的单元测试
- 模拟依赖注入
- 工具验证和错误场景测试
- 集成测试模式

## 📚 其他资源

- **官方 Pydantic AI 文档**：https://ai.pydantic.dev/
- **上下文工程方法论**：请参阅主仓库 README

## 🆘 支持与贡献

- **问题**：报告模板或示例的问题
- **改进**：贡献额外的示例或模式
- **疑问**：询问 Pydantic AI 集成或上下文工程相关问题

此模板是更大的上下文工程框架的一部分。请参阅主仓库了解更多上下文工程模板和方法论。

---

**准备好构建生产级 AI 代理了吗？** 从 `python copy_template.py my-agent-project` 开始，并遵循 PRP 工作流！🚀