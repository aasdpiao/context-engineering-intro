"""带记忆和上下文的基础聊天代理

一个简单的对话代理，演示核心 PydanticAI 模式：
- 基于环境的模型配置
- 用于个性和行为的系统提示
- 带记忆的基础对话处理
- 字符串输出（默认，无需 result_type）
"""

import logging
from dataclasses import dataclass
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """聊天代理的配置设置。"""
    
    # LLM 配置
    llm_provider: str = Field(default="openai")
    llm_api_key: str = Field(...)
    llm_model: str = Field(default="gpt-4")
    llm_base_url: str = Field(default="https://api.openai.com/v1")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


def get_llm_model() -> OpenAIModel:
    """从环境设置获取配置的 LLM 模型。"""
    try:
        settings = Settings()
        provider = OpenAIProvider(
            base_url=settings.llm_base_url,
            api_key=settings.llm_api_key
        )
        return OpenAIModel(settings.llm_model, provider=provider)
    except Exception:
        # 用于在没有环境变量的情况下测试
        import os
        os.environ.setdefault("LLM_API_KEY", "test-key")
        settings = Settings()
        provider = OpenAIProvider(
            base_url=settings.llm_base_url,
            api_key="test-key"
        )
        return OpenAIModel(settings.llm_model, provider=provider)


@dataclass
class ConversationContext:
    """用于对话状态管理的简单上下文。"""
    user_name: Optional[str] = None
    conversation_count: int = 0
    preferred_language: str = "English"
    session_id: Optional[str] = None


SYSTEM_PROMPT = """
你是一个友好且乐于助人的 AI 助手。

你的个性：
- 温暖且平易近人
- 知识渊博但谦逊
- 耐心且理解
- 鼓励且支持

指导原则：
- 保持回应的对话性和自然性
- 乐于助人但不要过于强势
- 在适当时提出后续问题
- 记住对话中的上下文
- 调整你的语调以匹配用户的需求
"""


# 创建基础聊天代理 - 注意：没有 result_type，默认为字符串
chat_agent = Agent(
    get_llm_model(),
    deps_type=ConversationContext,
    system_prompt=SYSTEM_PROMPT
)


@chat_agent.system_prompt
def dynamic_context_prompt(ctx) -> str:
    """包含对话上下文的动态系统提示。"""
    prompt_parts = []
    
    if ctx.deps.user_name:
        prompt_parts.append(f"用户的名字是 {ctx.deps.user_name}。")
    
    if ctx.deps.conversation_count > 0:
        prompt_parts.append(f"这是你们对话中的第 #{ctx.deps.conversation_count + 1} 条消息。")
    
    if ctx.deps.preferred_language != "English":
        prompt_parts.append(f"用户偏好使用 {ctx.deps.preferred_language} 进行交流。")
    
    return " ".join(prompt_parts) if prompt_parts else ""


async def chat_with_agent(message: str, context: Optional[ConversationContext] = None) -> str:
    """
    与代理聊天的主要函数。
    
    Args:
        message: 用户发送给代理的消息
        context: 用于记忆的可选对话上下文
    
    Returns:
        来自代理的字符串响应
    """
    if context is None:
        context = ConversationContext()
    
    # 增加对话计数
    context.conversation_count += 1
    
    # 使用消息和上下文运行代理
    result = await chat_agent.run(message, deps=context)
    
    return result.data


def chat_with_agent_sync(message: str, context: Optional[ConversationContext] = None) -> str:
    """
    用于简单用例的 chat_with_agent 同步版本。
    
    Args:
        message: 用户发送给代理的消息
        context: 用于记忆的可选对话上下文
    
    Returns:
        来自代理的字符串响应
    """
    if context is None:
        context = ConversationContext()
    
    # 增加对话计数
    context.conversation_count += 1
    
    # 同步运行代理
    result = chat_agent.run_sync(message, deps=context)
    
    return result.data


# 示例使用和演示
if __name__ == "__main__":
    import asyncio
    
    async def demo_conversation():
        """通过简单对话演示基础聊天代理。"""
        print("=== 基础聊天代理演示 ===")
        
        # 创建对话上下文
        context = ConversationContext(
            user_name="Alex",
            preferred_language="English"
        )
        
        # 示例对话
        messages = [
            "你好！我的名字是 Alex，很高兴认识你。",
            "你能帮我理解什么是 PydanticAI 吗？",
            "很有趣！它与其他 AI 框架有什么不同？",
            "谢谢你的解释。你能推荐一些学习更多内容的好资源吗？"
        ]
        
        for message in messages:
            print(f"用户: {message}")
            
            response = await chat_with_agent(message, context)
            
            print(f"代理: {response}")
            print("-" * 50)
    
    # 运行演示
    asyncio.run(demo_conversation())