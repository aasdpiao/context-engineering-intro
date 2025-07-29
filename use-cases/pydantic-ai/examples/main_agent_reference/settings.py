"""
使用 pydantic-settings 进行配置管理。
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator, ConfigDict
from dotenv import load_dotenv

# 从 .env 文件加载环境变量
load_dotenv()


class Settings(BaseSettings):
    """支持环境变量的应用程序设置。"""
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    # LLM 配置
    llm_provider: str = Field(default="openai")
    llm_api_key: str = Field(...)
    llm_model: str = Field(default="gpt-4")
    llm_base_url: Optional[str] = Field(default="https://api.openai.com/v1")
    
    # Brave 搜索配置
    brave_api_key: str = Field(...)
    brave_search_url: str = Field(
        default="https://api.search.brave.com/res/v1/web/search"
    )
    
    # 应用程序配置
    app_env: str = Field(default="development")
    log_level: str = Field(default="INFO")
    debug: bool = Field(default=False)
    
    @field_validator("llm_api_key", "brave_api_key")
    @classmethod
    def validate_api_keys(cls, v):
        """确保 API 密钥不为空。"""
        if not v or v.strip() == "":
            raise ValueError("API key cannot be empty")
        return v


# 全局设置实例
try:
    settings = Settings()
except Exception:
    # 用于测试，使用虚拟值创建设置
    import os
    os.environ.setdefault("LLM_API_KEY", "test_key")
    os.environ.setdefault("BRAVE_API_KEY", "test_key")
    settings = Settings()