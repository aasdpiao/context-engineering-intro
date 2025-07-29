"""
多代理系统的核心数据模型。
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class ResearchQuery(BaseModel):
    """研究查询请求的模型。"""
    query: str = Field(..., description="要调查的研究主题")
    max_results: int = Field(10, ge=1, le=50, description="返回的最大结果数")
    include_summary: bool = Field(True, description="是否包含 AI 生成的摘要")


class BraveSearchResult(BaseModel):
    """单个 Brave 搜索结果的模型。"""
    title: str = Field(..., description="搜索结果的标题")
    url: str = Field(..., description="搜索结果的 URL")
    description: str = Field(..., description="搜索结果的描述/摘要")
    score: float = Field(0.0, ge=0.0, le=1.0, description="相关性评分")
    
    class Config:
        """Pydantic 配置。"""
        json_schema_extra = {
            "example": {
                "title": "Understanding AI Safety",
                "url": "https://example.com/ai-safety",
                "description": "A comprehensive guide to AI safety principles...",
                "score": 0.95
            }
        }


class EmailDraft(BaseModel):
    """邮件草稿创建的模型。"""
    to: List[str] = Field(..., min_length=1, description="收件人邮件地址列表")
    subject: str = Field(..., min_length=1, description="邮件主题行")
    body: str = Field(..., min_length=1, description="邮件正文内容")
    cc: Optional[List[str]] = Field(None, description="抄送收件人列表")
    bcc: Optional[List[str]] = Field(None, description="密送收件人列表")
    
    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "to": ["john@example.com"],
                "subject": "AI Research Summary",
                "body": "Dear John,\n\nHere's the latest research on AI safety...",
                "cc": ["team@example.com"]
            }
        }


class EmailDraftResponse(BaseModel):
    """邮件草稿创建的响应模型。"""
    draft_id: str = Field(..., description="Gmail 草稿 ID")
    message_id: str = Field(..., description="消息 ID")
    thread_id: Optional[str] = Field(None, description="如果是线程的一部分，则为线程 ID")
    created_at: datetime = Field(default_factory=datetime.now, description="草稿创建时间戳")


class ResearchEmailRequest(BaseModel):
    """研究 + 邮件草稿请求的模型。"""
    research_query: str = Field(..., description="要研究的主题")
    email_context: str = Field(..., description="邮件生成的上下文")
    recipient_email: str = Field(..., description="邮件收件人")
    email_subject: Optional[str] = Field(None, description="可选的邮件主题")


class ResearchResponse(BaseModel):
    """研究查询的响应模型。"""
    query: str = Field(..., description="原始研究查询")
    results: List[BraveSearchResult] = Field(..., description="搜索结果")
    summary: Optional[str] = Field(None, description="AI 生成的结果摘要")
    total_results: int = Field(..., description="找到的结果总数")
    timestamp: datetime = Field(default_factory=datetime.now, description="查询时间戳")


class AgentResponse(BaseModel):
    """通用代理响应模型。"""
    success: bool = Field(..., description="操作是否成功")
    data: Optional[Dict[str, Any]] = Field(None, description="响应数据")
    error: Optional[str] = Field(None, description="失败时的错误消息")
    tools_used: List[str] = Field(default_factory=list, description="使用的工具列表")


class ChatMessage(BaseModel):
    """CLI 中聊天消息的模型。"""
    role: str = Field(..., description="消息角色（用户/助手）")
    content: str = Field(..., description="消息内容")
    timestamp: datetime = Field(default_factory=datetime.now, description="消息时间戳")
    tools_used: Optional[List[Dict[str, Any]]] = Field(None, description="响应中使用的工具")


class SessionState(BaseModel):
    """维护会话状态的模型。"""
    session_id: str = Field(..., description="唯一会话标识符")
    user_id: Optional[str] = Field(None, description="用户标识符")
    messages: List[ChatMessage] = Field(default_factory=list, description="对话历史")
    created_at: datetime = Field(default_factory=datetime.now, description="会话创建时间")
    last_activity: datetime = Field(default_factory=datetime.now, description="最后活动时间戳")