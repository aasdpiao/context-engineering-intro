"""多代理系统的纯工具函数。
这些是独立的函数，可以被任何代理导入和使用。"""

import os
import base64
import logging
import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime

from agents.models import BraveSearchResult

logger = logging.getLogger(__name__)


# Brave 搜索工具函数
async def search_web_tool(
    api_key: str,
    query: str,
    count: int = 10,
    offset: int = 0,
    country: Optional[str] = None,
    lang: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    使用 Brave 搜索 API 搜索网络的纯函数。
    
    Args:
        api_key: Brave 搜索 API 密钥
        query: 搜索查询
        count: 返回的结果数（1-20）
        offset: 分页偏移量
        country: 本地化结果的国家代码
        lang: 结果的语言代码
        
    Returns:
        搜索结果的字典列表
        
    Raises:
        ValueError: 如果查询为空或缺少 API 密钥
        Exception: 如果 API 请求失败
    """
    if not api_key or not api_key.strip():
        raise ValueError("Brave API key is required")
    
    if not query or not query.strip():
        raise ValueError("Query cannot be empty")
    
    # 确保 count 在有效范围内
    count = min(max(count, 1), 20)
    
    headers = {
        "X-Subscription-Token": api_key,
        "Accept": "application/json"
    }
    
    params = {
        "q": query,
        "count": count,
        "offset": offset
    }
    
    if country:
        params["country"] = country
    if lang:
        params["lang"] = lang
    
    logger.info(f"Searching Brave for: {query}")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "https://api.search.brave.com/res/v1/web/search",
                headers=headers,
                params=params,
                timeout=30.0
            )
            
            # 处理速率限制
            if response.status_code == 429:
                raise Exception("Rate limit exceeded. Check your Brave API quota.")
            
            # 处理身份验证错误
            if response.status_code == 401:
                raise Exception("Invalid Brave API key")
            
            # 处理其他错误
            if response.status_code != 200:
                raise Exception(f"Brave API returned {response.status_code}: {response.text}")
            
            data = response.json()
            
            # 提取网络结果
            web_results = data.get("web", {}).get("results", [])
            
            # 转换为我们的格式
            results = []
            for idx, result in enumerate(web_results):
                # 基于位置计算简单的相关性评分
                score = 1.0 - (idx * 0.05)  # 每个位置减少 0.05
                score = max(score, 0.1)  # 最低评分为 0.1
                
                results.append({
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "description": result.get("description", ""),
                    "score": score
                })
            
            logger.info(f"Found {len(results)} results for query: {query}")
            return results
            
        except httpx.RequestError as e:
            logger.error(f"Request error during Brave search: {e}")
            raise Exception(f"Request failed: {str(e)}")
        except Exception as e:
            logger.error(f"Error during Brave search: {e}")
            raise
