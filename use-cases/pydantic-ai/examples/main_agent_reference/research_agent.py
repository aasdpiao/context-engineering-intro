"""使用 Brave 搜索并可以调用邮件代理的研究代理。"""

import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from pydantic_ai import Agent, RunContext

from .providers import get_llm_model
from .email_agent import email_agent, EmailAgentDependencies
from .tools import search_web_tool

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = """
你是一个专业的研究助手，具有搜索网络和创建邮件草稿的能力。你的主要目标是帮助用户找到相关信息并有效地传达研究结果。

你的能力：
1. **网络搜索**：使用 Brave 搜索查找任何主题的当前相关信息
2. **邮件创建**：在请求时通过 Gmail 创建专业的邮件草稿

进行研究时：
- 使用具体、有针对性的搜索查询
- 分析搜索结果的相关性和可信度
- 综合来自多个来源的信息
- 提供清晰、组织良好的摘要
- 包含来源 URL 以供参考

创建邮件时：
- 使用研究结果创建有根据的专业内容
- 根据预期收件人调整语调和详细程度
- 在适当时包含相关来源和引用
- 确保邮件清晰、简洁且可操作

始终努力提供准确、有用且可操作的信息。
"""


@dataclass
class ResearchAgentDependencies:
    """研究代理的依赖项 - 仅配置，无工具实例。"""
    brave_api_key: str
    gmail_credentials_path: str
    gmail_token_path: str
    session_id: Optional[str] = None


# 初始化研究代理
research_agent = Agent(
    get_llm_model(),
    deps_type=ResearchAgentDependencies,
    system_prompt=SYSTEM_PROMPT
)


@research_agent.tool
async def search_web(
    ctx: RunContext[ResearchAgentDependencies],
    query: str,
    max_results: int = 10
) -> List[Dict[str, Any]]:
    """
    使用 Brave 搜索 API 搜索网络。
    
    Args:
        query: 搜索查询
        max_results: 返回的最大结果数（1-20）
    
    Returns:
        包含标题、URL、描述和评分的搜索结果列表
    """
    try:        
        # 确保 max_results 在有效范围内
        max_results = min(max(max_results, 1), 20)
        
        results = await search_web_tool(
            api_key=ctx.deps.brave_api_key,
            query=query,
            count=max_results
        )
        
        logger.info(f"Found {len(results)} results for query: {query}")
        return results
        
    except Exception as e:
        logger.error(f"Web search failed: {e}")
        return [{"error": f"Search failed: {str(e)}"}]


@research_agent.tool
async def create_email_draft(
    ctx: RunContext[ResearchAgentDependencies],
    recipient_email: str,
    subject: str,
    context: str,
    research_summary: Optional[str] = None
) -> Dict[str, Any]:
    """
    使用邮件代理基于研究上下文创建邮件草稿。
    
    Args:
        recipient_email: 收件人的邮件地址
        subject: 邮件主题行
        context: 邮件的上下文或目的
        research_summary: 可选的研究结果包含
    
    Returns:
        包含草稿创建结果的字典
    """
    try:
        # 准备邮件内容提示
        if research_summary:
            email_prompt = f"""
Create a professional email to {recipient_email} with the subject "{subject}".

Context: {context}

Research Summary:
{research_summary}

Please create a well-structured email that:
1. Has an appropriate greeting
2. Provides clear context
3. Summarizes the key research findings professionally
4. Includes actionable next steps if appropriate
5. Ends with a professional closing

The email should be informative but concise, and maintain a professional yet friendly tone.
"""
        else:
            email_prompt = f"""
Create a professional email to {recipient_email} with the subject "{subject}".

Context: {context}

Please create a well-structured email that addresses the context provided.
"""
        
        # 为邮件代理创建依赖项
        email_deps = EmailAgentDependencies(
            gmail_credentials_path=ctx.deps.gmail_credentials_path,
            gmail_token_path=ctx.deps.gmail_token_path,
            session_id=ctx.deps.session_id
        )
        
        # 运行邮件代理
        result = await email_agent.run(
            email_prompt,
            deps=email_deps,
            usage=ctx.usage  # 传递使用情况以进行令牌跟踪
        )
        
        logger.info(f"Email agent invoked for recipient: {recipient_email}")
        
        return {
            "success": True,
            "agent_response": result.data,
            "recipient": recipient_email,
            "subject": subject,
            "context": context
        }
        
    except Exception as e:
        logger.error(f"Failed to create email draft via Email Agent: {e}")
        return {
            "success": False,
            "error": str(e),
            "recipient": recipient_email,
            "subject": subject
        }


@research_agent.tool
async def summarize_research(
    ctx: RunContext[ResearchAgentDependencies],
    search_results: List[Dict[str, Any]],
    topic: str,
    focus_areas: Optional[str] = None
) -> Dict[str, Any]:
    """
    创建研究结果的综合摘要。
    
    Args:
        search_results: 搜索结果字典列表
        topic: 主要研究主题
        focus_areas: 可选的特定关注领域
    
    Returns:
        包含研究摘要的字典
    """
    try:
        if not search_results:
            return {
                "summary": "No search results provided for summarization.",
                "key_points": [],
                "sources": []
            }
        
        # 提取关键信息
        sources = []
        descriptions = []
        
        for result in search_results:
            if "title" in result and "url" in result:
                sources.append(f"- {result['title']}: {result['url']}")
                if "description" in result:
                    descriptions.append(result["description"])
        
        # 创建摘要内容
        content_summary = "\n".join(descriptions[:5])  # 限制为前 5 个描述
        sources_list = "\n".join(sources[:10])  # 限制为前 10 个来源
        
        focus_text = f"\nSpecific focus areas: {focus_areas}" if focus_areas else ""
        
        summary = f"""
Research Summary: {topic}{focus_text}

Key Findings:
{content_summary}

Sources:
{sources_list}
"""
        
        return {
            "summary": summary,
            "topic": topic,
            "sources_count": len(sources),
            "key_points": descriptions[:5]
        }
        
    except Exception as e:
        logger.error(f"Failed to summarize research: {e}")
        return {
            "summary": f"Failed to summarize research: {str(e)}",
            "key_points": [],
            "sources": []
        }


# 创建带有依赖项的研究代理的便利函数
def create_research_agent(
    brave_api_key: str,
    gmail_credentials_path: str,
    gmail_token_path: str,
    session_id: Optional[str] = None
) -> Agent:
    """
    创建具有指定依赖项的研究代理。
    
    Args:
        brave_api_key: Brave 搜索 API 密钥
        gmail_credentials_path: Gmail credentials.json 的路径
        gmail_token_path: Gmail token.json 的路径
        session_id: 可选的会话标识符
        
    Returns:
        配置的研究代理
    """
    return research_agent