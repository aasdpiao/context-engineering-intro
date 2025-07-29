"""用于数据验证的结构化输出代理

演示何时在 PydanticAI 中使用结构化输出：
- 基于环境的模型配置（遵循 main_agent_reference）
- 使用 Pydantic 模型进行结构化输出验证（指定 result_type）
- 数据提取和验证用例
- 具有一致格式的专业报告生成
"""

import logging
from dataclasses import dataclass
from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """结构化输出代理的配置设置。"""
    
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
class AnalysisDependencies:
    """分析代理的依赖项。"""
    report_format: str = "business"  # business, technical, academic
    include_recommendations: bool = True
    session_id: Optional[str] = None


class DataInsight(BaseModel):
    """从数据中提取的单个洞察。"""
    insight: str = Field(description="关键洞察或发现")
    confidence: float = Field(ge=0.0, le=1.0, description="对此洞察的置信度")
    data_points: List[str] = Field(description="支持的数据点")


class DataAnalysisReport(BaseModel):
    """带验证的数据分析结构化输出。"""
    
    # 必需字段
    summary: str = Field(description="分析的执行摘要")
    key_insights: List[DataInsight] = Field(
        min_items=1, 
        max_items=10,
        description="在数据中发现的关键洞察"
    )
    
    # 验证字段
    confidence_score: float = Field(
        ge=0.0, le=1.0,
        description="分析的整体置信度"
    )
    data_quality: str = Field(
        pattern="^(excellent|good|fair|poor)$",
        description="数据质量评估"
    )
    
    # 可选结构化字段
    recommendations: Optional[List[str]] = Field(
        default=None,
        description="基于发现的可行建议"
    )
    limitations: Optional[List[str]] = Field(
        default=None,
        description="分析中的限制或注意事项"
    )
    
    # 元数据
    analysis_type: str = Field(description="执行的分析类型")
    data_sources: List[str] = Field(description="分析的数据源")


SYSTEM_PROMPT = """
您是一位专业的数据分析师，专门从各种数据源中提取结构化洞察。

您的职责：
- 以统计严谨性分析提供的数据
- 提取有意义的洞察和模式
- 评估数据质量和可靠性
- 提供可行的建议
- 以一致、专业的格式构建发现

指导原则：
- 在分析中保持客观和基于证据
- 清楚区分事实和解释
- 为您的洞察提供置信度
- 突出数据的优势和局限性
- 确保所有输出遵循所需的结构化格式
"""


# 创建结构化输出代理 - 注意：为数据验证指定了 result_type
structured_agent = Agent(
    get_llm_model(),
    deps_type=AnalysisDependencies,
    result_type=DataAnalysisReport,  # 这是我们确实需要结构化输出的时候
    system_prompt=SYSTEM_PROMPT
)


@structured_agent.tool
def analyze_numerical_data(
    ctx: RunContext[AnalysisDependencies],
    data_description: str,
    numbers: List[float]
) -> str:
    """
    分析数值数据并提供统计洞察。
    
    Args:
        data_description: 数字代表什么的描述
        numbers: 要分析的数值列表
    
    Returns:
        统计分析摘要
    """
    try:
        if not numbers:
            return "未提供数值数据进行分析。"
        
        # 基本统计计算
        count = len(numbers)
        total = sum(numbers)
        average = total / count
        minimum = min(numbers)
        maximum = max(numbers)
        
        # 计算方差和标准差
        variance = sum((x - average) ** 2 for x in numbers) / count
        std_dev = variance ** 0.5
        
        # 简单趋势分析
        if count > 1:
            trend = "递增" if numbers[-1] > numbers[0] else "递减"
        else:
            trend = "数据不足"
        
        analysis = f"""
{data_description} 的统计分析：
- 计数：{count} 个数据点
- 平均值：{average:.2f}
- 范围：{minimum:.2f} 到 {maximum:.2f}  
- 标准差：{std_dev:.2f}
- 整体趋势：{trend}
- 数据质量：{'良好' if std_dev < average * 0.5 else '变化较大'}
"""
        
        logger.info(f"已分析 {count} 个数据点，用于：{data_description}")
        return analysis.strip()
        
    except Exception as e:
        logger.error(f"数值分析错误：{e}")
        return f"分析数值数据时出错：{str(e)}"


async def analyze_data(
    data_input: str,
    dependencies: Optional[AnalysisDependencies] = None
) -> DataAnalysisReport:
    """
    分析数据并返回结构化报告。
    
    Args:
        data_input: 要分析的原始数据或描述
        dependencies: 可选的分析配置
    
    Returns:
        带验证的结构化 DataAnalysisReport
    """
    if dependencies is None:
        dependencies = AnalysisDependencies()
    
    result = await structured_agent.run(data_input, deps=dependencies)
    return result.data


def analyze_data_sync(
    data_input: str,
    dependencies: Optional[AnalysisDependencies] = None
) -> DataAnalysisReport:
    """
    analyze_data 的同步版本。
    
    Args:
        data_input: 要分析的原始数据或描述
        dependencies: 可选的分析配置
    
    Returns:
        带验证的结构化 DataAnalysisReport
    """
    import asyncio
    return asyncio.run(analyze_data(data_input, dependencies))


# 示例使用和演示
if __name__ == "__main__":
    import asyncio
    
    async def demo_structured_output():
        """演示结构化输出验证。"""
        print("=== 结构化输出代理演示 ===\n")
        
        # 示例数据场景
        scenarios = [
            {
                "title": "销售业绩数据",
                "data": """
                2024年第四季度月度销售数据：
                十月：$125,000
                十一月：$142,000  
                十二月：$158,000
                
                客户满意度评分：4.2, 4.5, 4.1, 4.6, 4.3
                退货率：3.2%
                """
            },
            {
                "title": "网站分析",
                "data": """
                网站流量分析：
                - 日均访客：5,200
                - 跳出率：35%
                - 页面加载时间：2.1秒
                - 转化率：3.8%
                - 移动端流量：68%
                """
            }
        ]
        
        for scenario in scenarios:
            print(f"分析：{scenario['title']}")
            print(f"输入数据：{scenario['data'][:100]}...")
            
            # 配置为商业报告
            deps = AnalysisDependencies(
                report_format="business",
                include_recommendations=True
            )
            
            try:
                report = await analyze_data(scenario['data'], deps)
                
                print(f"摘要：{report.summary}")
                print(f"置信度：{report.confidence_score}")
                print(f"数据质量：{report.data_quality}")
                print(f"关键洞察：发现 {len(report.key_insights)} 个")
                
                for i, insight in enumerate(report.key_insights, 1):
                    print(f"  {i}. {insight.insight} (置信度: {insight.confidence})")
                
                if report.recommendations:
                    print(f"建议：{len(report.recommendations)} 条")
                    for i, rec in enumerate(report.recommendations, 1):
                        print(f"  {i}. {rec}")
                
                print("=" * 60)
                
            except Exception as e:
                print(f"分析失败：{e}")
                print("=" * 60)
    
    # 运行演示
    asyncio.run(demo_structured_output())