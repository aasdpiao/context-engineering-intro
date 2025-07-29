#!/usr/bin/env python3
"""具有实时流式传输和工具调用可见性的 Pydantic AI 代理对话式 CLI。"""

import asyncio
import sys
import os
from typing import List

# 将父目录添加到 Python 路径以进行导入
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.live import Live
from rich.text import Text

from pydantic_ai import Agent
from agents.research_agent import research_agent
from agents.dependencies import ResearchAgentDependencies
from agents.settings import settings

console = Console()


async def stream_agent_interaction(user_input: str, conversation_history: List[str]) -> tuple[str, str]:
    """流式传输代理交互，实时显示工具调用。"""
    
    try:
        # 设置依赖项
        research_deps = ResearchAgentDependencies(brave_api_key=settings.brave_api_key)
        
        # 使用对话历史构建上下文
        context = "\n".join(conversation_history[-6:]) if conversation_history else ""
        
        prompt = f"""Previous conversation:
{context}

User: {user_input}

Respond naturally and helpfully."""

        # 流式传输代理执行
        async with research_agent.iter(prompt, deps=research_deps) as run:
            
            async for node in run:
                
                # 处理用户提示节点
                if Agent.is_user_prompt_node(node):
                    pass  # 干净的开始 - 无处理消息
                
                # 处理模型请求节点 - 流式传输思考过程
                elif Agent.is_model_request_node(node):
                    # 在开始时显示助手前缀
                    console.print("[bold blue]Assistant:[/bold blue] ", end="")
                    
                    # 流式传输模型请求事件以获取实时文本
                    response_text = ""
                    async with node.stream(run.ctx) as request_stream:
                        async for event in request_stream:
                            # 根据事件类型处理不同的事件类型
                            event_type = type(event).__name__
                            
                            if event_type == "PartDeltaEvent":
                                # 从增量中提取内容
                                if hasattr(event, 'delta') and hasattr(event.delta, 'content_delta'):
                                    delta_text = event.delta.content_delta
                                    if delta_text:
                                        console.print(delta_text, end="")
                                        response_text += delta_text
                            elif event_type == "FinalResultEvent":
                                console.print()  # 流式传输后换行
                
                # 处理工具调用 - 这是关键部分
                elif Agent.is_call_tools_node(node):
                    # 流式传输工具执行事件
                    async with node.stream(run.ctx) as tool_stream:
                        async for event in tool_stream:
                            event_type = type(event).__name__
                            
                            if event_type == "FunctionToolCallEvent":
                                # 从 part 属性中提取工具名称  
                                tool_name = "Unknown Tool"
                                args = None
                                
                                # 检查 part 属性是否包含工具调用
                                if hasattr(event, 'part'):
                                    part = event.part
                                    
                                    # 检查 part 是否直接有 tool_name
                                    if hasattr(part, 'tool_name'):
                                        tool_name = part.tool_name
                                    elif hasattr(part, 'function_name'):
                                        tool_name = part.function_name
                                    elif hasattr(part, 'name'):
                                        tool_name = part.name
                                    
                                    # 检查 part 中的参数
                                    if hasattr(part, 'args'):
                                        args = part.args
                                    elif hasattr(part, 'arguments'):
                                        args = part.arguments
                                
                                # 调试：打印 part 属性以了解结构
                                if tool_name == "Unknown Tool" and hasattr(event, 'part'):
                                    part_attrs = [attr for attr in dir(event.part) if not attr.startswith('_')]
                                    console.print(f"    [dim red]Debug - Part attributes: {part_attrs}[/dim red]")
                                    
                                    # 尝试获取有关 part 的更多详细信息
                                    if hasattr(event.part, '__dict__'):
                                        console.print(f"    [dim red]Part dict: {event.part.__dict__}[/dim red]")
                                
                                console.print(f"  🔹 [cyan]Calling tool:[/cyan] [bold]{tool_name}[/bold]")
                                
                                # 如果可用，显示工具参数
                                if args and isinstance(args, dict):
                                    # 显示每个参数的前几个字符
                                    arg_preview = []
                                    for key, value in list(args.items())[:3]:
                                        val_str = str(value)
                                        if len(val_str) > 50:
                                            val_str = val_str[:47] + "..."
                                        arg_preview.append(f"{key}={val_str}")
                                    console.print(f"    [dim]Args: {', '.join(arg_preview)}[/dim]")
                                elif args:
                                    args_str = str(args)
                                    if len(args_str) > 100:
                                        args_str = args_str[:97] + "..."
                                    console.print(f"    [dim]Args: {args_str}[/dim]")
                            
                            elif event_type == "FunctionToolResultEvent":
                                # 显示工具结果
                                result = str(event.tool_return) if hasattr(event, 'tool_return') else "No result"
                                if len(result) > 100:
                                    result = result[:97] + "..."
                                console.print(f"  ✅ [green]Tool result:[/green] [dim]{result}[/dim]")
                
                # 处理结束节点  
                elif Agent.is_end_node(node):
                    # 不显示"处理完成" - 保持简洁
                    pass
        
        # 获取最终结果
        final_result = run.result
        final_output = final_result.output if hasattr(final_result, 'output') else str(final_result)
        
        # 返回流式传输和最终内容
        return (response_text.strip(), final_output)
        
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        return ("", f"Error: {e}")


async def main():
    """主对话循环。"""
    
    # 显示欢迎信息
    welcome = Panel(
        "[bold blue]🤖 Pydantic AI Research Assistant[/bold blue]\n\n"
        "[green]Real-time tool execution visibility[/green]\n"
        "[dim]Type 'exit' to quit[/dim]",
        style="blue",
        padding=(1, 2)
    )
    console.print(welcome)
    console.print()
    
    conversation_history = []
    
    while True:
        try:
            # 获取用户输入
            user_input = Prompt.ask("[bold green]You").strip()
            
            # 处理退出
            if user_input.lower() in ['exit', 'quit']:
                console.print("\n[yellow]👋 Goodbye![/yellow]")
                break
                
            if not user_input:
                continue
            
            # 添加到历史记录
            conversation_history.append(f"User: {user_input}")
            
            # 流式传输交互并获取响应
            streamed_text, final_response = await stream_agent_interaction(user_input, conversation_history)
            
            # 处理响应显示
            if streamed_text:
                # 响应已流式传输，只需添加间距
                console.print()
                conversation_history.append(f"Assistant: {streamed_text}")
            elif final_response and final_response.strip():
                # 响应未流式传输，使用适当的格式显示
                console.print(f"[bold blue]Assistant:[/bold blue] {final_response}")
                console.print()
                conversation_history.append(f"Assistant: {final_response}")
            else:
                # 无响应
                console.print()
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Use 'exit' to quit[/yellow]")
            continue
            
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            continue


if __name__ == "__main__":
    asyncio.run(main())