# 模板生成请求

## 技术/框架：

**示例：** Pydantic AI 代理  
**示例：** Supabase 前端应用程序  
**示例：** CrewAI 多代理系统  

**您的技术：** [指定您想要为其创建上下文工程模板的确切框架、库或技术]

---

## 模板目的：

**此模板应针对哪个特定用例进行优化？**

**Pydantic AI 示例：** "使用 Pydantic AI 框架构建具有工具集成、对话处理和结构化数据验证的智能 AI 代理"

**Supabase 示例：** "使用 Supabase 作为后端创建具有实时数据、身份验证和无服务器函数的全栈 Web 应用程序"

**您的目的：** [非常具体地说明开发人员应该能够使用此模板轻松构建什么]

---

## 核心功能：

**此模板应帮助开发人员实现哪些基本功能？**

**Pydantic AI 示例：**
- 使用不同模型提供商（OpenAI、Anthropic、Gemini）创建代理
- 工具集成模式（网络搜索、文件操作、API 调用）
- 对话记忆和上下文管理
- 使用 Pydantic 模型进行结构化输出验证
- 错误处理和重试机制
- AI 代理行为的测试模式

**Supabase 示例：**
- 数据库架构设计和迁移
- 实时订阅和实时数据更新
- 行级安全（RLS）策略实现
- 身份验证流程（电子邮件、OAuth、魔法链接）
- 后端逻辑的无服务器边缘函数
- 文件存储和 CDN 集成

**您的核心功能：** [列出开发人员应该能够轻松实现的具体功能]

---

## 包含的示例：

**模板中应提供哪些工作示例？**

**Pydantic AI 示例：**
- 具有记忆功能的基本聊天代理
- 启用工具的代理（网络搜索 + 计算器）
- 多步骤工作流代理
- 具有自定义 Pydantic 模型的结构化输出代理
- 代理响应和工具使用的测试示例

**Supabase 示例：**
- 用户身份验证和配置文件管理
- 实时聊天或消息系统
- 文件上传和共享功能
- 多租户应用程序模式
- 数据库触发器和函数

**您的示例：** [指定应包含的具体工作示例]

---

## 需要研究的文档：

**应该彻底研究和引用哪些特定文档？**

**Pydantic AI 示例：**
- https://ai.pydantic.dev/ - 官方 Pydantic AI 文档
- https://docs.pydantic.dev/ - Pydantic 数据验证库
- 模型提供商 API（OpenAI、Anthropic）的集成模式
- 工具集成最佳实践和示例
- AI 应用程序的测试框架

**Supabase 示例：**
- https://supabase.com/docs - 完整的 Supabase 文档
- https://supabase.com/docs/guides/auth - 身份验证指南
- https://supabase.com/docs/guides/realtime - 实时功能
- 数据库设计模式和 RLS 策略
- 边缘函数开发和部署

**您的文档：** [列出需要深入研究的特定 URL 和文档部分]

---

## 开发模式：

**应该研究和包含哪些特定的开发模式、项目结构或工作流程？**

**Pydantic AI 示例：**
- 如何构建代理模块和工具定义
- 不同模型提供商的配置管理
- 开发与生产环境设置
- AI 代理的日志记录和监控模式
- 提示和代理配置的版本控制模式

**Supabase 示例：**
- 前端 + Supabase 项目结构模式
- 使用 Supabase CLI 的本地开发工作流程
- 数据库迁移和版本控制策略
- 环境管理（本地、暂存、生产）
- 全栈 Supabase 应用程序的测试策略

**您的开发模式：** [指定要研究的工作流程和组织模式]

---

## 安全和最佳实践：

**对于此技术，哪些安全考虑和最佳实践是关键的？**

**Pydantic AI 示例：**
- API 密钥管理和轮换
- 代理输入的输入验证和清理
- 速率限制和使用监控
- 提示注入防护
- 模型使用的成本控制和监控

**Supabase 示例：**
- 行级安全（RLS）策略设计
- API 密钥与 JWT 身份验证模式
- 数据库安全和访问控制
- 文件上传安全和病毒扫描
- 速率限制和滥用防护

**您的安全考虑：** [列出要研究和记录的技术特定安全模式]

---

## 常见陷阱：

**开发人员在使用此技术时面临的典型陷阱、边缘情况或复杂问题是什么？**

**Pydantic AI 示例：**
- 模型上下文长度限制和管理
- 处理模型提供商速率限制和错误
- 令牌计数和成本优化
- 跨请求管理对话状态
- 工具执行错误处理和重试

**Supabase 示例：**
- RLS 策略调试和测试
- 大数据集的实时订阅性能
- 边缘函数冷启动和优化
- 无服务器环境中的数据库连接池
- 不同域的 CORS 配置

**您的陷阱：** [识别开发人员常见面临的具体挑战]

---

## 验证要求：

**模板中应包含哪些特定的验证、测试或质量检查？**

**Pydantic AI 示例：**
- 代理响应质量测试
- 工具集成测试
- 模型提供商故障转移测试
- 成本和性能基准测试
- 对话流程验证

**Supabase 示例：**
- 数据库迁移测试
- RLS 策略验证
- 实时功能测试
- 身份验证流程测试
- 边缘函数集成测试

**您的验证要求：** [指定所需的测试和验证模式]

---

## 集成焦点：

**此技术通常与哪些特定集成或第三方服务一起使用？**

**Pydantic AI 示例：**
- 与向量数据库集成（Pinecone、Weaviate）
- 网络抓取工具和 API
- 工具的外部 API 集成
- 监控服务（Weights & Biases、LangSmith）
- 部署平台（Modal、Replicate）

**Supabase 示例：**
- 前端框架（Next.js、React、Vue）
- 支付处理（Stripe）
- 电子邮件服务（SendGrid、Resend）
- 文件处理（图像优化、文档解析）
- 分析和监控工具

**您的集成焦点：** [列出要研究和包含的关键集成]

---

## ADDITIONAL NOTES:

**Any other specific requirements, constraints, or considerations for this template?**

**Example:** "Focus on TypeScript patterns and include comprehensive type definitions"  
**Example:** "Emphasize serverless deployment patterns and cost optimization"  
**Example:** "Include patterns for both beginner and advanced use cases"

**Your additional notes:** [Any other important considerations]

---

## TEMPLATE COMPLEXITY LEVEL:

**What level of complexity should this template target?**

- [ ] **Beginner-friendly** - Simple getting started patterns
- [ ] **Intermediate** - Production-ready patterns with common features  
- [ ] **Advanced** - Comprehensive patterns including complex scenarios
- [ ] **Enterprise** - Full enterprise patterns with monitoring, scaling, security

**Your choice:** [Select the appropriate complexity level and explain why]

---

**REMINDER: Be as specific as possible in each section. The more detailed you are here, the better the generated template will be. This INITIAL.md file is where you should put all your requirements, not just basic information.**