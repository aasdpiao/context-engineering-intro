"""LLM 模型的灵活提供者配置。
基于 examples/agent/providers.py 模式。"""

from typing import Optional
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel
from .settings import settings


def get_llm_model(model_choice: Optional[str] = None) -> OpenAIModel:
    """
    基于环境变量获取 LLM 模型配置。
    
    Args:
        model_choice: 模型选择的可选覆盖
    
    Returns:
        配置好的 OpenAI 兼容模型
    """
    llm_choice = model_choice or settings.llm_model
    base_url = settings.llm_base_url
    api_key = settings.llm_api_key
    
    # 基于配置创建提供者
    provider = OpenAIProvider(base_url=base_url, api_key=api_key)
    
    return OpenAIModel(llm_choice, provider=provider)


def get_model_info() -> dict:
    """
    获取当前模型配置的信息。
    
    Returns:
        包含模型配置信息的字典
    """
    return {
        "llm_provider": settings.llm_provider,
        "llm_model": settings.llm_model,
        "llm_base_url": settings.llm_base_url,
        "app_env": settings.app_env,
        "debug": settings.debug,
    }


def validate_llm_configuration() -> bool:
    """
    验证 LLM 配置是否正确设置。
    
    Returns:
        如果配置有效则返回 True
    """
    try:
        # 检查是否可以创建模型实例
        get_llm_model()
        return True
    except Exception as e:
        print(f"LLM configuration validation failed: {e}")
        return False