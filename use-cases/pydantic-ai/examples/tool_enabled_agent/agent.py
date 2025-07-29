"""带网络搜索和计算器的工具启用代理

演示 PydanticAI 工具集成模式：
- 基于环境的模型配置
- 使用 @agent.tool 装饰器注册工具
- 用于依赖注入的 RunContext
- 使用类型提示进行参数验证
- 错误处理和重试机制
- 字符串输出（默认，无需 result_type）
"""

import logging
import math
import json
import asyncio
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime
import aiohttp
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
    """工具启用代理的配置设置。"""
    
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
class ToolDependencies:
    """工具启用代理的依赖项。"""
    session: Optional[aiohttp.ClientSession] = None
    api_timeout: int = 10
    max_search_results: int = 5
    calculation_precision: int = 6
    session_id: Optional[str] = None


SYSTEM_PROMPT = """
你是一个有用的研究助手，可以访问网络搜索和计算工具。

你的能力：
- 网络搜索获取当前信息和事实
- 数学计算和数据分析
- 数据处理和格式化
- 来源验证和引用

指导原则：
- 当你需要当前信息或计算时，始终使用工具
- 提供事实信息时引用来源
- 展示数学计算的工作过程
- 在回应中保持精确和准确
- 如果工具失败，解释限制并提供你能提供的内容
"""


# 创建工具启用代理 - 注意：没有 result_type，默认为字符串
tool_agent = Agent(
    get_llm_model(),
    deps_type=ToolDependencies,
    system_prompt=SYSTEM_PROMPT
)


@tool_agent.tool
async def web_search(
    ctx: RunContext[ToolDependencies], 
    query: str,
    max_results: Optional[int] = None
) -> str:
    """
    搜索网络获取当前信息。
    
    Args:
        query: 搜索查询字符串
        max_results: 返回的最大结果数（默认：5）
    
    Returns:
        包含标题、摘要和 URL 的格式化搜索结果
    """
    if not ctx.deps.session:
        return "网络搜索不可用：未配置 HTTP 会话"
    
    max_results = max_results or ctx.deps.max_search_results
    
    try:
        # 使用 DuckDuckGo 即时回答 API 作为简单示例
        # 在生产环境中，使用适当的搜索 API，如 Google、Bing 或 DuckDuckGo
        search_url = "https://api.duckduckgo.com/"
        params = {
            "q": query,
            "format": "json",
            "pretty": "1",
            "no_redirect": "1"
        }
        
        async with ctx.deps.session.get(
            search_url, 
            params=params, 
            timeout=ctx.deps.api_timeout
        ) as response:
            if response.status == 200:
                data = await response.json()
                
                results = []
                
                # 如果可用，处理即时回答
                if data.get("AbstractText"):
                    results.append({
                        "title": "即时回答",
                        "snippet": data["AbstractText"],
                        "url": data.get("AbstractURL", "")
                    })
                
                # 处理相关主题
                for topic in data.get("RelatedTopics", [])[:max_results-len(results)]:
                    if isinstance(topic, dict) and "Text" in topic:
                        results.append({
                            "title": topic.get("FirstURL", "").split("/")[-1].replace("_", " "),
                            "snippet": topic["Text"],
                            "url": topic.get("FirstURL", "")
                        })
                
                if not results:
                    return f"未找到查询结果：{query}"
                
                # 格式化结果
                formatted_results = []
                for i, result in enumerate(results, 1):
                    formatted_results.append(
                        f"{i}. **{result['title']}**\n"
                        f"   {result['snippet']}\n"
                        f"   Source: {result['url']}"
                    )
                
                return "\n\n".join(formatted_results)
            else:
                return f"搜索失败，状态码：{response.status}"
                
    except asyncio.TimeoutError:
        return f"搜索超时，等待时间：{ctx.deps.api_timeout} 秒"
    except Exception as e:
        return f"搜索错误：{str(e)}"


@tool_agent.tool
def calculate(
    ctx: RunContext[ToolDependencies],
    expression: str,
    description: Optional[str] = None
) -> str:
    """
    安全地执行数学计算。
    
    Args:
        expression: 要计算的数学表达式
        description: 计算内容的可选描述
    
    Returns:
        带格式化输出的计算结果
    """
    try:
        # 安全计算 - 仅允许数学运算
        allowed_names = {
            "abs": abs, "round": round, "min": min, "max": max,
            "sum": sum, "pow": pow, "sqrt": math.sqrt,
            "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "log": math.log, "log10": math.log10, "exp": math.exp,
            "pi": math.pi, "e": math.e
        }
        
        # 移除任何潜在的危险操作
        safe_expression = expression.replace("__", "").replace("import", "")
        
        # 计算表达式
        result = eval(safe_expression, {"__builtins__": {}}, allowed_names)
        
        # 使用适当的精度格式化结果
        if isinstance(result, float):
            result = round(result, ctx.deps.calculation_precision)
        
        output = f"计算：{expression} = {result}"
        if description:
            output = f"{description}\n{output}"
        
        return output
        
    except Exception as e:
        return f"计算错误：{str(e)}\n表达式：{expression}"


@tool_agent.tool
def format_data(
    ctx: RunContext[ToolDependencies],
    data: str,
    format_type: str = "table"
) -> str:
    """
    将数据格式化为结构化输出。
    
    Args:
        data: 要格式化的原始数据
        format_type: 格式化类型（table、list、json）
    
    Returns:
        格式化的数据字符串
    """
    try:
        lines = data.strip().split('\n')
        
        if format_type == "table":
            # 简单表格格式化
            if len(lines) > 1:
                header = lines[0]
                rows = lines[1:]
                
                # 基本表格格式化
                formatted = f"| {header} |\n"
                formatted += f"|{'-' * (len(header) + 2)}|\n"
                for row in rows[:10]:  # 限制为 10 行
                    formatted += f"| {row} |\n"
                
                return formatted
            else:
                return data
                
        elif format_type == "list":
            # 项目符号列表
            formatted_lines = [f"• {line.strip()}" for line in lines if line.strip()]
            return "\n".join(formatted_lines)
            
        elif format_type == "json":
            # 尝试解析并格式化为 JSON
            try:
                parsed = json.loads(data)
                return json.dumps(parsed, indent=2)
            except json.JSONDecodeError:
                # 如果不是有效的 JSON，创建简单的键值结构
                items = {}
                for i, line in enumerate(lines):
                    items[f"item_{i+1}"] = line.strip()
                return json.dumps(items, indent=2)
        
        return data
        
    except Exception as e:
        return f"格式化错误：{str(e)}"


@tool_agent.tool
def get_current_time(ctx: RunContext[ToolDependencies]) -> str:
    """
    获取当前日期和时间。
    
    Returns:
        可读格式的当前时间戳
    """
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S UTC")


async def ask_agent(
    question: str, 
    dependencies: Optional[ToolDependencies] = None
) -> str:
    """
    向工具启用代理提问。
    
    Args:
        question: 向代理提出的问题或请求
        dependencies: 可选的工具依赖项
    
    Returns:
        来自代理的字符串响应
    """
    if dependencies is None:
        # 为网络搜索创建 HTTP 会话
        session = aiohttp.ClientSession()
        dependencies = ToolDependencies(session=session)
    
    try:
        result = await tool_agent.run(question, deps=dependencies)
        return result.data
    finally:
        # 如果是我们创建的会话，则清理它
        if dependencies.session and not dependencies.session.closed:
            await dependencies.session.close()


def ask_agent_sync(question: str) -> str:
    """
    ask_agent 的同步版本。
    
    Args:
        question: 向代理提出的问题或请求
    
    Returns:
        来自代理的字符串响应
    """
    return asyncio.run(ask_agent(question))


# 示例使用和演示
if __name__ == "__main__":
    async def demo_tools():
        """演示工具启用代理的能力。"""
        print("=== 工具启用代理演示 ===")
        
        # 使用 HTTP 会话创建依赖项
        session = aiohttp.ClientSession()
        dependencies = ToolDependencies(session=session)
        
        try:
            # 练习不同工具的示例问题
            questions = [
                "现在几点了？",
                "计算 144 的平方根加上 200 的 25%",
                "搜索关于人工智能的最新新闻",
                "将此数据格式化为表格：Name,Age\nAlice,25\nBob,30\nCharlie,35"
            ]
            
            for question in questions:
                print(f"问题：{question}")
                
                response = await ask_agent(question, dependencies)
                
                print(f"回答：{response}")
                print("-" * 60)
                
        finally:
            await session.close()
    
    # 运行演示
    asyncio.run(demo_tools())