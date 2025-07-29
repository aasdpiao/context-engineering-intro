---
name: "PydanticAI 代理 PRP 模板"
description: "用于生成 PydanticAI 代理开发项目综合 PRP 的模板"
---

## 目的

[简要描述要构建的 PydanticAI 代理及其主要目的]

## 核心原则

1. **PydanticAI 最佳实践**: 深度集成 PydanticAI 模式，用于代理创建、工具和结构化输出
2. **生产就绪**: 包含安全性、测试和监控，用于生产部署
3. **类型安全优先**: 在整个过程中利用 PydanticAI 的类型安全设计和 Pydantic 验证
4. **上下文工程集成**: 将经过验证的上下文工程工作流应用于 AI 代理开发
5. **全面测试**: 使用 TestModel 和 FunctionModel 进行彻底的代理验证

## ⚠️ 实施指南：不要过度工程化

**重要提示**: 保持代理实施的专注性和实用性。不要构建不必要的复杂性。

### 不要做的事情：
- ❌ **不要创建数十个工具** - 只构建代理实际需要的工具
- ❌ **不要过度复杂化依赖关系** - 保持依赖注入简单且专注
- ❌ **不要添加不必要的抽象** - 直接遵循 main_agent_reference 模式
- ❌ **不要构建复杂的工作流** 除非特别需要
- ❌ **不要添加结构化输出** 除非特别需要验证（默认使用字符串）
- ❌ **不要在 examples/ 文件夹中构建**

### 要做的事情：
- ✅ **从简单开始** - 构建满足要求的最小可行代理
- ✅ **逐步添加工具** - 只实现代理运行所需的功能
- ✅ **遵循 main_agent_reference** - 使用经过验证的模式，不要重新发明
- ✅ **默认使用字符串输出** - 只有在需要验证时才添加 result_type
- ✅ **早期且频繁测试** - 在构建过程中使用 TestModel 进行验证

### 关键问题：
**"这个代理真的需要这个功能来完成其核心目的吗？"**

如果答案是否定的，就不要构建它。保持简单、专注和实用。

---

## 目标

[详细描述代理应该完成的任务]

## 原因

[解释为什么需要这个代理以及它解决什么问题]

## 内容

### 代理类型分类
- [ ] **聊天代理**: 具有记忆和上下文的对话界面
- [ ] **工具增强代理**: 具有外部工具集成能力的代理
- [ ] **工作流代理**: 多步骤任务处理和编排
- [ ] **结构化输出代理**: 复杂数据验证和格式化

### 模型提供商要求
- [ ] **OpenAI**: `openai:gpt-4o` 或 `openai:gpt-4o-mini`
- [ ] **Anthropic**: `anthropic:claude-3-5-sonnet-20241022` 或 `anthropic:claude-3-5-haiku-20241022`
- [ ] **Google**: `gemini-1.5-flash` 或 `gemini-1.5-pro`
- [ ] **回退策略**: 支持多个提供商的自动故障转移

### 外部集成
- [ ] 数据库连接（指定类型：PostgreSQL、MongoDB 等）
- [ ] REST API 集成（列出所需服务）
- [ ] 文件系统操作
- [ ] 网页抓取或搜索功能
- [ ] 实时数据源

### 成功标准

#### 技术成功
- [ ] 代理使用正确的 PydanticAI 模式成功实例化
- [ ] 所有工具正确注册并正常运行
- [ ] 使用 Pydantic 实现类型安全的数据模型
- [ ] 全面的测试覆盖率（>90%）
- [ ] 安全措施已实施并验证
- [ ] 性能基准达标

#### 实施成功
- [ ] 遵循 PydanticAI 最佳实践的清洁、可维护代码
- [ ] 正确的错误处理和日志记录
- [ ] 文档完整且准确
- [ ] 生产就绪的配置
- [ ] 监控和可观测性已实施

#### 验证成功
- [ ] 所有验证级别通过
- [ ] 代理行为符合要求
- [ ] 集成测试成功
- [ ] 安全审计完成
- [ ] 性能测试完成

## 所需的全部上下文

### PydanticAI 文档和研究

```yaml
# MCP 服务器
- mcp: Archon
  query: "PydanticAI agent creation model providers tools dependencies"
  why: 核心框架理解和最新模式

# 必要的 PYDANTIC AI 文档 - 必须研究
- url: https://ai.pydantic.dev/
  why: 官方 PydanticAI 文档和入门指南
  content: 代理创建、模型提供商、依赖注入模式

- url: https://ai.pydantic.dev/agents/
  why: 全面的代理架构和配置模式
  content: 系统提示、输出类型、执行方法、代理组合

- url: https://ai.pydantic.dev/tools/
  why: 工具集成模式和函数注册
  content: @agent.tool 装饰器、RunContext 使用、参数验证

- url: https://ai.pydantic.dev/testing/
  why: PydanticAI 代理特定的测试策略
  content: TestModel、FunctionModel、Agent.override()、pytest 模式

- url: https://ai.pydantic.dev/models/
  why: 模型提供商配置和身份验证
  content: OpenAI、Anthropic、Gemini 设置、API 密钥管理、回退模型

# 预构建示例
- path: examples/
  why: Pydantic AI 代理的参考实现
  content: 一系列已构建的简单 Pydantic AI 示例，包括如何设置模型和提供商

- path: examples/cli.py
  why: 展示与 Pydantic AI 代理的真实世界交互
  content: 具有流式传输、工具调用可见性和对话处理的对话式 CLI - 演示用户如何实际与代理交互
```

### 代理架构研究

```yaml
# PydanticAI 架构模式（遵循 main_agent_reference）
agent_structure:
  configuration:
    - settings.py: 基于环境的配置，使用 pydantic-settings
    - providers.py: 模型提供商抽象，使用 get_llm_model()
    - API 密钥和模型选择的环境变量
    - 永远不要硬编码模型字符串，如 "openai:gpt-4o"
  
  agent_definition:
    - 默认字符串输出（除非需要结构化输出，否则不使用 result_type）
    - 使用 providers.py 中的 get_llm_model() 进行模型配置
    - 系统提示作为字符串常量或函数
    - 外部服务的数据类依赖
  
  tool_integration:
    - @agent.tool 用于具有 RunContext[DepsType] 的上下文感知工具
    - 工具函数作为可独立调用的纯函数
    - 工具实现中的适当错误处理和日志记录
    - 通过 RunContext.deps 进行依赖注入
  
  testing_strategy:
    - TestModel 用于快速开发验证
    - FunctionModel 用于自定义行为测试
    - Agent.override() 用于测试隔离
    - 使用模拟进行全面的工具测试
```

### 安全和生产考虑

```yaml
# PydanticAI 安全模式（需要研究）
security_requirements:
  api_management:
    environment_variables: ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY"]
    secure_storage: "永远不要将 API 密钥提交到版本控制"
    rotation_strategy: "规划密钥轮换和管理"
  
  input_validation:
    sanitization: "使用 Pydantic 模型验证所有用户输入"
    prompt_injection: "实施提示注入防护策略"
    rate_limiting: "通过适当的限流防止滥用"
  
  output_security:
    data_filtering: "确保代理响应中没有敏感数据"
    content_validation: "验证输出结构和内容"
    logging_safety: "安全日志记录，不暴露机密信息"
```

### 常见 PydanticAI 陷阱（研究和记录）

```yaml
# 需要研究和解决的代理特定陷阱
implementation_gotchas:
  async_patterns:
    issue: "不一致地混合同步和异步代理调用"
    research: "PydanticAI async/await 最佳实践"
    solution: "[基于研究待记录]"
  
  model_limits:
    issue: "不同模型具有不同的能力和令牌限制"
    research: "模型提供商比较和能力"
    solution: "[基于研究待记录]"
  
  dependency_complexity:
    issue: "复杂的依赖图可能难以调试"
    research: "PydanticAI 中的依赖注入最佳实践"
    solution: "[基于研究待记录]"
  
  tool_error_handling:
    issue: "工具故障可能导致整个代理运行崩溃"
    research: "工具的错误处理和重试模式"
    solution: "[基于研究待记录]"
```

## 实施蓝图

### 技术研究阶段

**需要研究 - 在实施前完成：**

✅ **PydanticAI 框架深入研究：**
- [ ] 代理创建模式和最佳实践
- [ ] 模型提供商配置和回退策略
- [ ] 工具集成模式（@agent.tool vs @agent.tool_plain）
- [ ] 依赖注入系统和类型安全
- [ ] 使用 TestModel 和 FunctionModel 的测试策略

✅ **代理架构调研：**
- [ ] 项目结构约定（agent.py、tools.py、models.py、dependencies.py）
- [ ] 系统提示设计（静态 vs 动态）
- [ ] 使用 Pydantic 模型的结构化输出验证
- [ ] 异步/同步模式和流式支持
- [ ] 错误处理和重试机制

✅ **安全和生产模式：**
- [ ] API 密钥管理和安全配置
- [ ] 输入验证和提示注入防护
- [ ] 速率限制和监控策略
- [ ] 日志记录和可观测性模式
- [ ] 部署和扩展考虑

### 代理实施计划

```yaml
实施任务 1 - 代理架构设置（遵循 main_agent_reference）：
  创建代理项目结构：
    - settings.py: 基于环境的配置，使用 pydantic-settings
    - providers.py: 模型提供商抽象，使用 get_llm_model()
    - agent.py: 主代理定义（默认字符串输出）
    - tools.py: 具有适当装饰器的工具函数
    - dependencies.py: 外部服务集成（数据类）
    - tests/: 全面的测试套件

实施任务 2 - 核心代理开发：
  实现 agent.py，遵循 main_agent_reference 模式：
    - 使用 providers.py 中的 get_llm_model() 进行模型配置
    - 系统提示作为字符串常量或函数
    - 使用数据类进行依赖注入
    - 除非特别需要结构化输出，否则不使用 result_type
    - 错误处理和日志记录

实施任务 3 - 工具集成：
  开发 tools.py：
    - 使用 @agent.tool 装饰器的工具函数
    - RunContext[DepsType] 集成以访问依赖
    - 使用适当类型提示的参数验证
    - 错误处理和重试机制
    - 工具文档和模式生成

实施任务 4 - 数据模型和依赖：
  创建 models.py 和 dependencies.py：
    - 结构化输出的 Pydantic 模型
    - 外部服务的依赖类
    - 工具的输入验证模型
    - 自定义验证器和约束

实施任务 5 - 全面测试：
  实现测试套件：
    - TestModel 集成用于快速开发
    - FunctionModel 测试用于自定义行为
    - Agent.override() 模式用于隔离
    - 与真实提供商的集成测试
    - 工具验证和错误场景测试

实施任务 6 - 安全和配置：
  设置安全模式：
    - API 密钥的环境变量管理
    - 输入清理和验证
    - 速率限制实现
    - 安全日志记录和监控
    - 生产部署配置
```

## 验证循环

### 级别 1：代理结构验证

```bash
# 验证完整的代理项目结构
find agent_project -name "*.py" | sort
test -f agent_project/agent.py && echo "代理定义存在"
test -f agent_project/tools.py && echo "工具模块存在"
test -f agent_project/models.py && echo "模型模块存在"
test -f agent_project/dependencies.py && echo "依赖模块存在"

# 验证正确的 PydanticAI 导入
grep -q "from pydantic_ai import Agent" agent_project/agent.py
grep -q "@agent.tool" agent_project/tools.py
grep -q "from pydantic import BaseModel" agent_project/models.py

# 预期：所有必需的文件都具有正确的 PydanticAI 模式
# 如果缺失：生成具有正确模式的缺失组件
```

### 级别 2：代理功能验证

```bash
# 测试代理可以被导入和实例化
python -c "
from agent_project.agent import agent
print('代理创建成功')
print(f'模型: {agent.model}')
print(f'工具: {len(agent.tools)}')
"

# 使用 TestModel 进行验证测试
python -c "
from pydantic_ai.models.test import TestModel
from agent_project.agent import agent
test_model = TestModel()
with agent.override(model=test_model):
    result = agent.run_sync('测试消息')
    print(f'代理响应: {result.output}')
"

# 预期：代理实例化工作正常，工具已注册，TestModel 验证通过
# 如果失败：调试代理配置和工具注册
```

### 级别 3：全面测试验证

```bash
# 运行完整的测试套件
cd agent_project
python -m pytest tests/ -v

# 测试特定的代理行为
python -m pytest tests/test_agent.py::test_agent_response -v
python -m pytest tests/test_tools.py::test_tool_validation -v
python -m pytest tests/test_models.py::test_output_validation -v

# 预期：所有测试通过，实现全面覆盖
# 如果失败：根据测试失败修复实现
```

### 级别 4：生产就绪验证

```bash
# 验证安全模式
grep -r "API_KEY" agent_project/ | grep -v ".py:" # 不应暴露密钥
test -f agent_project/.env.example && echo "环境模板存在"

# 检查错误处理
grep -r "try:" agent_project/ | wc -l  # 应该有错误处理
grep -r "except" agent_project/ | wc -l  # 应该有异常处理

# 验证日志设置
grep -r "logging\|logger" agent_project/ | wc -l  # 应该有日志记录

# 预期：安全措施到位，错误处理全面，日志记录已配置
# 如果有问题：实施缺失的安全和生产模式
```

## 最终验证清单

### 代理实施完整性

- [ ] 完整的代理项目结构：`agent.py`、`tools.py`、`models.py`、`dependencies.py`
- [ ] 使用正确的模型提供商配置实例化代理
- [ ] 使用 @agent.tool 装饰器和 RunContext 集成注册工具
- [ ] 使用 Pydantic 模型验证的结构化输出
- [ ] 依赖注入正确配置和测试
- [ ] 使用 TestModel 和 FunctionModel 的全面测试套件

### PydanticAI 最佳实践

- [ ] 全程类型安全，具有正确的类型提示和验证
- [ ] 实施安全模式（API 密钥、输入验证、速率限制）
- [ ] 用于稳健操作的错误处理和重试机制
- [ ] 异步/同步模式一致且适当
- [ ] 可维护性的文档和代码注释

### 生产就绪

- [ ] 使用 .env 文件和验证的环境配置
- [ ] 用于可观测性的日志记录和监控设置
- [ ] 性能优化和资源管理
- [ ] 具有正确配置管理的部署就绪
- [ ] 维护和更新策略已记录

---

## 要避免的反模式

### PydanticAI 代理开发

- ❌ 不要跳过 TestModel 验证 - 在开发过程中始终使用 TestModel 测试
- ❌ 不要硬编码 API 密钥 - 对所有凭据使用环境变量
- ❌ 不要忽略异步模式 - PydanticAI 有特定的异步/同步要求
- ❌ 不要创建复杂的工具链 - 保持工具专注和可组合
- ❌ 不要跳过错误处理 - 实施全面的重试和回退机制

### 代理架构

- ❌ 不要混合代理类型 - 清楚地分离聊天、工具、工作流和结构化输出模式
- ❌ 不要忽略依赖注入 - 使用正确的类型安全依赖管理
- ❌ 不要跳过输出验证 - 始终对结构化响应使用 Pydantic 模型
- ❌ 不要忘记工具文档 - 确保所有工具都有正确的描述和模式

### 安全和生产

- ❌ 不要暴露敏感数据 - 验证所有输出和日志的安全性
- ❌ 不要跳过输入验证 - 清理和验证所有用户输入
- ❌ 不要忽略速率限制 - 对外部服务实施适当的限流
- ❌ 不要在没有监控的情况下部署 - 从一开始就包含适当的可观测性

**研究状态：[待完成]** - 在实施开始前完成全面的 PydanticAI 研究。