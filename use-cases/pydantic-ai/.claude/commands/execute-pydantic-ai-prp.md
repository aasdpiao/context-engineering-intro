# 执行 Pydantic AI 智能体 PRP

使用 PRP 文件实现 Pydantic AI 智能体。

## PRP 文件: $ARGUMENTS

## 执行过程

1. **加载 PRP**
   - 读取指定的 Pydantic AI PRP 文件
   - 理解所有智能体需求和研究发现
   - 遵循 PRP 中的所有指令，必要时扩展研究
   - 查看 main_agent_reference 模式以获得实现指导
   - 根据需要进行更多网络搜索和 Pydantic AI 文档审查

2. **深度思考**
   - 在执行智能体实现计划之前深入思考
   - 使用待办事项工具将智能体开发分解为更小的步骤
   - 使用 TodoWrite 工具创建和跟踪智能体实现计划
   - 遵循 main_agent_reference 模式进行配置和结构设计
   - 规划 agent.py、tools.py、dependencies.py 和测试方法

3. **执行计划**
   - 按照 PRP 实现 Pydantic AI 智能体
   - 使用基于环境的配置创建智能体（settings.py、providers.py）
   - 默认使用字符串输出（除非需要结构化输出，否则不使用 result_type）
   - 使用 @agent.tool 装饰器和适当的错误处理实现工具
   - 使用 TestModel 和 FunctionModel 添加全面测试

4. **验证**
   - 测试智能体导入和实例化
   - 运行 TestModel 验证以进行快速开发测试
   - 测试工具注册和功能
   - 如果创建了测试套件，运行 pytest
   - 验证智能体遵循 main_agent_reference 模式

5. **完成**
   - 确保完成所有 PRP 检查清单项目
   - 使用示例查询测试智能体
   - 验证安全模式（环境变量、错误处理）
   - 报告完成状态
   - 再次阅读 PRP 以确保完整实现

6. **参考 PRP**
   - 如果需要，您可以随时再次参考 PRP

## 要遵循的 Pydantic AI 特定模式

- **配置**: 使用类似 main_agent_reference 的基于环境的设置
- **输出**: 默认使用字符串输出，仅在需要验证时使用 result_type
- **工具**: 使用 @agent.tool 和 RunContext 进行依赖注入
- **测试**: 包含用于开发的 TestModel 验证
- **安全**: API 密钥使用环境变量，适当的错误处理

注意：如果验证失败，使用 PRP 中的错误模式进行修复和重试。遵循 main_agent_reference 获得经过验证的 Pydantic AI 实现模式。