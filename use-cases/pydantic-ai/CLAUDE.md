# PydanticAI 上下文工程 - AI 代理开发全局规则

本文件包含适用于所有 PydanticAI 代理开发工作的全局规则和原则。这些规则专门用于构建具有工具、记忆和结构化输出的生产级 AI 代理。

## 🔄 PydanticAI 核心原则

**重要：这些原则适用于所有 PydanticAI 代理开发：**

### 代理开发工作流
- **始终从 INITIAL.md 开始** - 在生成 PRP 之前定义代理需求
- **使用 PRP 模式**：INITIAL.md → `/generate-pydantic-ai-prp INITIAL.md` → `/execute-pydantic-ai-prp PRPs/filename.md`
- **遵循验证循环** - 每个 PRP 必须包含使用 TestModel/FunctionModel 的代理测试
- **上下文为王** - 包含所有必要的 PydanticAI 模式、示例和文档

### AI 代理研究方法论
- **广泛的网络搜索** - 始终研究 PydanticAI 模式和最佳实践
- **学习官方文档** - ai.pydantic.dev 是权威来源
- **模式提取** - 识别可重用的代理架构和工具模式
- **陷阱文档** - 记录异步模式、模型限制和上下文管理问题

## 📚 项目意识与上下文

- **使用虚拟环境** 运行所有代码和测试。如果代码库中还没有虚拟环境，请在需要时创建一个
- **使用一致的 PydanticAI 命名约定** 和代理结构模式
- **遵循既定的代理目录组织** 模式（agent.py、tools.py、models.py）
- **广泛利用 PydanticAI 示例** - 在创建新代理之前研究现有模式

## 🧱 代理结构与模块化

- **永远不要创建超过 500 行的文件** - 接近限制时拆分为模块
- **将代理代码组织为按职责明确分离的模块**：
  - `agent.py` - 主代理定义和执行逻辑
  - `tools.py` - 代理使用的工具函数
  - `models.py` - Pydantic 输出模型和依赖类
  - `dependencies.py` - 上下文依赖和外部服务集成
- **使用清晰、一致的导入** - 适当地从 pydantic_ai 包导入
- **使用 python-dotenv 和 load_dotenv()** 处理环境变量 - 遵循 examples/main_agent_reference/settings.py 模式
- **永远不要硬编码敏感信息** - 始终使用 .env 文件存储 API 密钥和配置

## 🤖 PydanticAI 开发标准

### 代理创建模式
- **使用模型无关设计** - 支持多个提供商（OpenAI、Anthropic、Gemini）
- **实现依赖注入** - 使用 deps_type 处理外部服务和上下文
- **定义结构化输出** - 使用 Pydantic 模型进行结果验证
- **包含全面的系统提示** - 静态和动态指令

### 工具集成标准
- **使用 @agent.tool 装饰器** 创建具有 RunContext[DepsType] 的上下文感知工具
- **使用 @agent.tool_plain 装饰器** 创建无上下文依赖的简单工具
- **实现适当的参数验证** - 使用 Pydantic 模型验证工具参数
- **优雅地处理工具错误** - 实现重试机制和错误恢复

### 使用 python-dotenv 的环境变量配置
```python
# 使用 python-dotenv 和 pydantic-settings 进行适当的配置管理
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from dotenv import load_dotenv
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel

class Settings(BaseSettings):
    """支持环境变量的应用程序设置。"""
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # LLM 配置
    llm_provider: str = Field(default="openai", description="LLM 提供商")
    llm_api_key: str = Field(..., description="LLM 提供商的 API 密钥")
    llm_model: str = Field(default="gpt-4", description="要使用的模型名称")
    llm_base_url: str = Field(
        default="https://api.openai.com/v1", 
        description="LLM API 的基础 URL"
    )

def load_settings() -> Settings:
    """加载设置，具有适当的错误处理和环境加载。"""
    # 从 .env 文件加载环境变量
    load_dotenv()
    
    try:
        return Settings()
    except Exception as e:
        error_msg = f"加载设置失败：{e}"
        if "llm_api_key" in str(e).lower():
            error_msg += "\n请确保在 .env 文件中设置 LLM_API_KEY"
        raise ValueError(error_msg) from e

def get_llm_model():
    """获取配置的 LLM 模型，具有适当的环境加载。"""
    settings = load_settings()
    provider = OpenAIProvider(
        base_url=settings.llm_base_url, 
        api_key=settings.llm_api_key
    )
    return OpenAIModel(settings.llm_model, provider=provider)
```

### AI 代理测试标准
- **使用 TestModel 进行开发** - 无需 API 调用的快速验证
- **使用 FunctionModel 进行自定义行为** - 在测试中控制代理响应
- **使用 Agent.override() 进行测试** - 在测试上下文中替换模型
- **测试同步和异步模式** - 确保与不同执行模式的兼容性
- **测试工具验证** - 验证工具参数模式和错误处理

## ✅ AI 开发任务管理

- **将代理开发分解为明确的步骤** 具有特定的完成标准
- **完成代理实现后立即标记任务完成**
- **实时更新任务状态** 随着代理开发的进展
- **在标记实现任务完成之前测试代理行为**

## 📎 PydanticAI 编码标准

### 代理架构
```python
# 遵循 main_agent_reference 模式 - 除非需要结构化输出，否则不使用 result_type
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
from .settings import load_settings

@dataclass
class AgentDependencies:
    """代理执行的依赖项"""
    api_key: str
    session_id: str = None

# 使用适当的 dotenv 处理加载设置
settings = load_settings()

# 具有字符串输出的简单代理（默认）
agent = Agent(
    get_llm_model(),  # 内部使用 load_settings()
    deps_type=AgentDependencies,
    system_prompt="你是一个有用的助手..."
)

@agent.tool
async def example_tool(
    ctx: RunContext[AgentDependencies], 
    query: str
) -> str:
    """具有适当上下文访问的工具"""
    return await external_api_call(ctx.deps.api_key, query)
```

### 安全最佳实践
- **API 密钥管理** - 使用 python-dotenv 和 .env 文件，永远不要将密钥提交到版本控制
- **环境变量加载** - 始终使用 load_dotenv()，遵循 examples/main_agent_reference/settings.py
- **输入验证** - 对所有工具参数使用 Pydantic 模型
- **速率限制** - 为外部 API 实现适当的请求节流
- **提示注入防护** - 验证和清理用户输入
- **错误处理** - 永远不要在错误消息中暴露敏感信息

### 常见 PydanticAI 陷阱
- **异步/同步混合问题** - 在整个过程中保持 async/await 模式的一致性
- **模型令牌限制** - 不同模型有不同的上下文限制，需要相应规划
- **依赖注入复杂性** - 保持依赖图简单且类型良好
- **工具错误处理失败** - 始终实现适当的重试和回退机制
- **上下文状态管理** - 为了可靠性，尽可能设计无状态工具

## 🔍 AI 代理研究标准

- **使用 Archon MCP 服务器** - 通过 RAG 利用可用的 PydanticAI 文档
- **学习官方示例** - ai.pydantic.dev/examples 有可工作的实现
- **研究模型能力** - 了解提供商特定的功能和限制
- **记录集成模式** - 包含外部服务集成示例

## 🎯 AI 代理实施标准

- **严格遵循 PRP 工作流** - 不要跳过代理验证步骤
- **始终首先使用 TestModel 测试** - 在使用真实模型之前验证代理逻辑
- **使用现有代理模式** 而不是从头创建
- **包含全面的错误处理** 用于工具失败和模型错误
- **测试流式模式** 在实施实时代理交互时

## 🚫 始终避免的反模式

- ❌ 不要跳过代理测试 - 始终使用 TestModel/FunctionModel 进行验证
- ❌ 不要硬编码模型字符串 - 使用像 main_agent_reference 这样的基于环境的配置
- ❌ 除非特别需要结构化输出，否则不要使用 result_type - 默认使用字符串
- ❌ 不要忽略异步模式 - PydanticAI 有特定的异步/同步考虑
- ❌ 不要创建复杂的依赖图 - 保持依赖简单且可测试
- ❌ 不要忘记工具错误处理 - 实施适当的重试和优雅降级
- ❌ 不要跳过输入验证 - 对所有外部输入使用 Pydantic 模型

## 🔧 AI 开发工具使用标准

- **广泛使用网络搜索** 进行 PydanticAI 研究和文档查阅
- **遵循 PydanticAI 命令模式** 用于斜杠命令和代理工作流
- **使用代理验证循环** 确保每个开发步骤的质量
- **使用多个模型提供商测试** 确保代理兼容性

## 🧪 AI 代理测试与可靠性

- **使用 TestModel 进行单元测试** - 无 API 成本，可预测的响应
- **使用 FunctionModel 进行集成测试** - 在不调用 LLM 的情况下测试工具交互
- **使用 Agent.override() 进行依赖测试** - 模拟外部服务和 API
- **测试同步和异步模式** - 确保跨执行模式的兼容性
- **验证工具错误场景** - 测试失败情况和恢复机制
- **使用不同模型提供商测试** - 确保跨提供商兼容性

这些全局规则专门适用于 PydanticAI 代理开发，确保生产就绪的 AI 应用程序具有适当的错误处理、测试和安全实践。