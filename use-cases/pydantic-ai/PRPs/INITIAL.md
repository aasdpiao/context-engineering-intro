## 功能特性：

[用您自己的上下文替换括号中的所有内容]
[提供您想要构建的代理的概述。细节越多越好！]
[过于简单的示例：使用 Pydantic AI 构建一个简单的研究代理，可以使用 Brave API 研究主题并通过 Gmail 起草电子邮件来分享见解。]

## 工具：

[描述您希望代理拥有的工具 - 功能、参数、返回内容等。尽可能具体 - 越具体越好。]

## 依赖项

[描述代理工具所需的依赖项（用于 Pydantic AI RunContext）- 例如 API 密钥、数据库连接、HTTP 客户端等。]

## 系统提示词

[在此描述代理的指令 - 您可以在此创建完整的系统提示词，或提供一般描述来指导编码助手]

## 示例：

[将过去项目或在线资源中的任何其他示例代理/工具实现添加到 examples/ 文件夹中，并在此处引用它们。]
[模板已经为 Pydantic AI 包含以下内容：]

- examples/basic_chat_agent - 具有对话记忆的基本聊天代理
- examples/tool_enabled_agent - 具有网络搜索功能的工具启用代理
- examples/structured_output_agent - 用于数据验证的结构化输出代理
- examples/testing_examples - 使用 TestModel 和 FunctionModel 的测试示例
- examples/main_agent_reference - 构建 Pydantic AI 代理的最佳实践

## 文档：

[添加您希望它引用的任何其他文档 - 这可以是您放在 PRPs/ai_docs 中的精选文档、URL 等。]

- Pydantic AI 官方文档：https://ai.pydantic.dev/
- 代理创建指南：https://ai.pydantic.dev/agents/
- 工具集成：https://ai.pydantic.dev/tools/
- 测试模式：https://ai.pydantic.dev/testing/
- 模型提供商：https://ai.pydantic.dev/models/

## 其他考虑事项：

- 使用环境变量进行 API 密钥配置，而不是硬编码的模型字符串
- 保持代理简单 - 除非特别需要结构化输出，否则默认使用字符串输出
- 遵循 main_agent_reference 的配置和提供商模式
- 始终包含使用 TestModel 进行开发的全面测试

[为编码助手添加任何其他考虑事项，特别是您希望它记住的"陷阱"。]