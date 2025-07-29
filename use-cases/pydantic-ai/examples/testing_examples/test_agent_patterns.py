"""全面的 PydanticAI 测试示例

演示 PydanticAI 代理的测试模式和最佳实践：
- 用于快速开发验证的 TestModel
- 用于自定义行为测试的 FunctionModel
- 用于测试隔离的 Agent.override()
- Pytest 夹具和异步测试
- 工具验证和错误处理测试
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock
from dataclasses import dataclass
from typing import Optional, List
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.test import TestModel, FunctionModel


@dataclass
class TestDependencies:
    """用于代理测试的测试依赖项。"""
    database: Mock
    api_client: Mock
    user_id: str = "test_user_123"


class TestResponse(BaseModel):
    """用于验证的测试响应模型。"""
    message: str
    confidence: float = 0.8
    actions: List[str] = []


# 创建用于演示的测试代理
test_agent = Agent(
    model="openai:gpt-4o-mini",  # 将在测试中被覆盖
    deps_type=TestDependencies,
    result_type=TestResponse,
    system_prompt="你是一个有用的测试助手。"
)


@test_agent.tool
async def mock_database_query(
    ctx: RunContext[TestDependencies], 
    query: str
) -> str:
    """用于测试的模拟数据库查询工具。"""
    try:
        # 模拟数据库调用
        result = await ctx.deps.database.execute_query(query)
        return f"数据库结果：{result}"
    except Exception as e:
        return f"数据库错误：{str(e)}"


@test_agent.tool
def mock_api_call(
    ctx: RunContext[TestDependencies],
    endpoint: str,
    data: Optional[dict] = None
) -> str:
    """用于测试的模拟 API 调用工具。"""
    try:
        # 模拟 API 调用
        response = ctx.deps.api_client.post(endpoint, json=data)
        return f"API 响应：{response}"
    except Exception as e:
        return f"API 错误：{str(e)}"


class TestAgentBasics:
    """使用 TestModel 测试基本代理功能。"""
    
    @pytest.fixture
    def test_dependencies(self):
        """创建用于测试的模拟依赖项。"""
        return TestDependencies(
            database=AsyncMock(),
            api_client=Mock(),
            user_id="test_user_123"
        )
    
    def test_agent_with_test_model(self, test_dependencies):
        """使用 TestModel 测试代理行为。"""
        test_model = TestModel()
        
        with test_agent.override(model=test_model):
            result = test_agent.run_sync(
                "你好，请帮我处理一个简单的任务。",
                deps=test_dependencies
            )
            
            # TestModel 默认返回 JSON 摘要
            assert result.data.message is not None
            assert isinstance(result.data.confidence, float)
            assert isinstance(result.data.actions, list)
    
    def test_agent_custom_test_model_output(self, test_dependencies):
        """使用自定义 TestModel 输出测试代理。"""
        test_model = TestModel(
            custom_output_text='{"message": "自定义测试响应", "confidence": 0.9, "actions": ["test_action"]}'
        )
        
        with test_agent.override(model=test_model):
            result = test_agent.run_sync(
                "测试消息",
                deps=test_dependencies
            )
            
            assert result.data.message == "自定义测试响应"
            assert result.data.confidence == 0.9
            assert result.data.actions == ["test_action"]
    
    @pytest.mark.asyncio
    async def test_agent_async_with_test_model(self, test_dependencies):
        """使用 TestModel 测试异步代理行为。"""
        test_model = TestModel()
        
        with test_agent.override(model=test_model):
            result = await test_agent.run(
                "异步测试消息",
                deps=test_dependencies
            )
            
            assert result.data.message is not None
            assert result.data.confidence >= 0.0


class TestAgentTools:
    """测试代理工具功能。"""
    
    @pytest.fixture
    def mock_dependencies(self):
        """创建配置了响应的模拟依赖项。"""
        database_mock = AsyncMock()
        database_mock.execute_query.return_value = "来自数据库的测试数据"
        
        api_mock = Mock()
        api_mock.post.return_value = {"status": "success", "data": "test_data"}
        
        return TestDependencies(
            database=database_mock,
            api_client=api_mock,
            user_id="test_user_456"
        )
    
    @pytest.mark.asyncio
    async def test_database_tool_success(self, mock_dependencies):
        """测试数据库工具的成功响应。"""
        test_model = TestModel(call_tools=['mock_database_query'])
        
        with test_agent.override(model=test_model):
            result = await test_agent.run(
                "请查询数据库获取用户数据",
                deps=mock_dependencies
            )
            
            # 验证数据库被调用
            mock_dependencies.database.execute_query.assert_called()
            
            # TestModel 应该包含工具结果
            assert "mock_database_query" in result.data.message
    
    @pytest.mark.asyncio
    async def test_database_tool_error(self, mock_dependencies):
        """测试数据库工具的错误处理。"""
        # 配置模拟对象抛出异常
        mock_dependencies.database.execute_query.side_effect = Exception("连接失败")
        
        test_model = TestModel(call_tools=['mock_database_query'])
        
        with test_agent.override(model=test_model):
            result = await test_agent.run(
                "查询数据库",
                deps=mock_dependencies
            )
            
            # 工具应该优雅地处理错误
            assert "mock_database_query" in result.data.message
    
    def test_api_tool_with_data(self, mock_dependencies):
        """测试带有 POST 数据的 API 工具。"""
        test_model = TestModel(call_tools=['mock_api_call'])
        
        with test_agent.override(model=test_model):
            result = test_agent.run_sync(
                "进行 API 调用以创建新记录",
                deps=mock_dependencies
            )
            
            # 验证 API 被调用
            mock_dependencies.api_client.post.assert_called()
            
            # 检查响应中的工具执行
            assert "mock_api_call" in result.data.message


class TestAgentWithFunctionModel:
    """使用 FunctionModel 测试代理行为以获得自定义响应。"""
    
    @pytest.fixture
    def test_dependencies(self):
        """创建基本测试依赖项。"""
        return TestDependencies(
            database=AsyncMock(),
            api_client=Mock()
        )
    
    def test_function_model_custom_behavior(self, test_dependencies):
        """使用 FunctionModel 测试代理的自定义行为。"""
        def custom_response_func(messages, tools):
            """生成特定响应的自定义函数。"""
            last_message = messages[-1].content if messages else ""
            
            if "error" in last_message.lower():
                return '{"message": "检测到错误并已处理", "confidence": 0.6, "actions": ["error_handling"]}'
            else:
                return '{"message": "正常操作", "confidence": 0.9, "actions": ["standard_response"]}'
        
        function_model = FunctionModel(function=custom_response_func)
        
        with test_agent.override(model=function_model):
            # 测试正常情况
            result1 = test_agent.run_sync(
                "请帮我处理一个正常请求",
                deps=test_dependencies
            )
            assert result1.data.message == "正常操作"
            assert result1.data.confidence == 0.9
            
            # 测试错误情况
            result2 = test_agent.run_sync(
                "系统中有一个错误",
                deps=test_dependencies
            )
            assert result2.data.message == "检测到错误并已处理"
            assert result2.data.confidence == 0.6
            assert "error_handling" in result2.data.actions


class TestAgentValidation:
    """测试代理输出验证和错误场景。"""
    
    @pytest.fixture
    def test_dependencies(self):
        """创建测试依赖项。"""
        return TestDependencies(
            database=AsyncMock(),
            api_client=Mock()
        )
    
    def test_invalid_output_handling(self, test_dependencies):
        """测试代理如何处理无效输出格式。"""
        # 带有无效 JSON 输出的 TestModel
        test_model = TestModel(
            custom_output_text='{"message": "test", "invalid_field": "should_not_exist"}'
        )
        
        with test_agent.override(model=test_model):
            # 这应该要么成功验证，要么抛出适当的错误
            try:
                result = test_agent.run_sync(
                    "测试无效输出",
                    deps=test_dependencies
                )
                # 如果成功，Pydantic 应该过滤掉无效字段
                assert hasattr(result.data, 'message')
                assert not hasattr(result.data, 'invalid_field')
            except Exception as e:
                # 或者可能抛出验证错误，这也是可以接受的
                assert "validation" in str(e).lower() or "error" in str(e).lower()
    
    def test_missing_required_fields(self, test_dependencies):
        """测试输出中缺少必需字段的处理。"""
        # 缺少必需消息字段的 TestModel
        test_model = TestModel(
            custom_output_text='{"confidence": 0.8}'
        )
        
        with test_agent.override(model=test_model):
            try:
                result = test_agent.run_sync(
                    "测试缺少字段",
                    deps=test_dependencies
                )
                # 应该提供默认值或抛出验证错误
                if hasattr(result.data, 'message'):
                    assert result.data.message is not None
            except Exception as e:
                # 对于缺少必需字段，预期会有验证错误
                assert any(keyword in str(e).lower() for keyword in ['validation', 'required', 'missing'])


class TestAgentIntegration:
    """完整代理工作流的集成测试。"""
    
    @pytest.fixture
    def full_mock_dependencies(self):
        """创建完全配置的模拟依赖项。"""
        database_mock = AsyncMock()
        database_mock.execute_query.return_value = {
            "user_id": "123",
            "name": "测试用户",
            "status": "active"
        }
        
        api_mock = Mock()
        api_mock.post.return_value = {
            "status": "success",
            "transaction_id": "txn_123456"
        }
        
        return TestDependencies(
            database=database_mock,
            api_client=api_mock,
            user_id="test_integration_user"
        )
    
    @pytest.mark.asyncio
    async def test_complete_workflow(self, full_mock_dependencies):
        """测试使用多个工具的完整代理工作流。"""
        test_model = TestModel(call_tools='all')  # 调用所有可用工具
        
        with test_agent.override(model=test_model):
            result = await test_agent.run(
                "请查找用户信息并创建新交易",
                deps=full_mock_dependencies
            )
            
            # 验证两个工具都可能被调用
            assert result.data.message is not None
            assert isinstance(result.data.actions, list)
            
            # 验证模拟对象被调用
            full_mock_dependencies.database.execute_query.assert_called()
            full_mock_dependencies.api_client.post.assert_called()


class TestAgentErrorRecovery:
    """测试代理错误处理和恢复模式。"""
    
    @pytest.fixture
    def failing_dependencies(self):
        """创建用于测试错误处理的失败依赖项。"""
        database_mock = AsyncMock()
        database_mock.execute_query.side_effect = Exception("数据库连接失败")
        
        api_mock = Mock()
        api_mock.post.side_effect = Exception("API 服务不可用")
        
        return TestDependencies(
            database=database_mock,
            api_client=api_mock,
            user_id="failing_test_user"
        )
    
    @pytest.mark.asyncio
    async def test_tool_error_recovery(self, failing_dependencies):
        """测试工具失败时的代理行为。"""
        test_model = TestModel(call_tools='all')
        
        with test_agent.override(model=test_model):
            # 代理应该优雅地处理工具失败
            result = await test_agent.run(
                "尝试访问数据库和 API",
                deps=failing_dependencies
            )
            
            # 即使工具失败，代理也应该返回有效响应
            assert result.data.message is not None
            assert isinstance(result.data.confidence, float)


# Pytest 配置和工具
@pytest.fixture(scope="session")
def event_loop():
    """为测试会话创建默认事件循环的实例。"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


def pytest_configure(config):
    """使用自定义标记配置 pytest。"""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


if __name__ == "__main__":
    # 直接运行测试
    pytest.main([__file__, "-v"])