---
name: "PydanticAI 模板生成器 PRP"
description: "为 PydanticAI 代理开发生成综合上下文工程模板，包含工具、内存和结构化输出"
---

## 目的

为 **PydanticAI** 生成完整的上下文工程模板包，使开发者能够使用 PydanticAI 框架快速构建具有工具集成、对话处理和结构化数据验证的智能 AI 代理。

## 核心原则

1. **PydanticAI 专业化**：深度集成 PydanticAI 模式，用于代理创建、工具和结构化输出
2. **完整包生成**：创建包含工作示例和验证的完整模板生态系统
3. **类型安全优先**：在整个过程中利用 PydanticAI 的类型安全设计和 Pydantic 验证
4. **生产就绪**：包含安全性、测试和生产部署的最佳实践
5. **上下文工程集成**：将经过验证的上下文工程工作流应用于 AI 代理开发

---

## 目标

为 **PydanticAI** 生成完整的上下文工程模板包，包括：

- PydanticAI 特定的 CLAUDE.md 实现指南，包含代理模式
- 专门用于 AI 代理的 PRP 生成和执行命令
- 具有代理架构模式的领域特定基础 PRP 模板
- 综合工作示例（聊天代理、工具集成、多步骤工作流）
- PydanticAI 特定的验证循环和测试模式

## 为什么

- **AI 开发加速**：实现生产级 PydanticAI 代理的快速开发
- **模式一致性**：维护已建立的 AI 代理架构模式和最佳实践
- **质量保证**：确保对代理行为、工具和输出进行全面测试
- **知识捕获**：记录 PydanticAI 特定的模式、陷阱和集成策略
- **可扩展 AI 框架**：为各种 AI 代理用例创建可重用模板

## 什么

### 模板包组件

**完整目录结构：**
```
use-cases/pydantic-ai/
├── CLAUDE.md                           # PydanticAI implementation guide
├── .claude/commands/
│   ├── generate-pydantic-ai-prp.md     # Agent PRP generation
│   └── execute-pydantic-ai-prp.md      # Agent PRP execution  
├── PRPs/
│   ├── templates/
│   │   └── prp_pydantic_ai_base.md     # PydanticAI base PRP template
│   ├── ai_docs/                        # PydanticAI documentation
│   └── INITIAL.md                      # Example agent feature request
├── examples/
│   ├── basic_chat_agent/               # Simple chat agent with memory
│   ├── tool_enabled_agent/             # Web search + calculator tools
│   ├── workflow_agent/                 # Multi-step workflow processing
│   ├── structured_output_agent/        # Custom Pydantic models
│   └── testing_examples/               # Agent testing patterns
├── copy_template.py                    # Template deployment script
└── README.md                           # Comprehensive usage guide
```

**PydanticAI 集成：**
- 使用多个模型提供商（OpenAI、Anthropic、Gemini）创建代理
- 工具集成模式和函数注册
- 使用依赖项进行对话内存和上下文管理
- 使用 Pydantic 模型进行结构化输出验证
- 使用 TestModel 和 FunctionModel 的测试模式
- API 密钥管理和输入验证的安全模式

**上下文工程适配：**
- PydanticAI 特定的研究流程和文档引用
- 适合代理的验证循环和测试策略
- AI 框架专业化的实现蓝图
- 与 AI 开发的基础上下文工程原则集成

### 成功标准

- [ ] 生成完整的 PydanticAI 模板包结构
- [ ] 所有必需文件都包含 PydanticAI 特定内容
- [ ] 代理模式准确代表 PydanticAI 最佳实践
- [ ] 上下文工程原则适配于 AI 代理开发
- [ ] 适合测试 AI 代理和工具的验证循环
- [ ] 模板可立即用于创建 PydanticAI 项目
- [ ] 与基础上下文工程框架的集成得到维护
- [ ] 包含全面的示例和测试文档

## 所需的所有上下文

### 文档和参考资料（已研究）

```yaml
# IMPORTANT - use the Archon MCP server to get more Pydantic AI documentation!
- mcp: Archon
  why: Official Pydantic AI documentation ready for RAG lookup
  content: All Pydantic AI documentation
# PYDANTIC AI CORE DOCUMENTATION - Essential framework understanding
- url: https://ai.pydantic.dev/
  why: Official PydanticAI documentation with core concepts and getting started
  content: Agent creation, model providers, type safety, dependency injection

- url: https://ai.pydantic.dev/agents/
  why: Comprehensive agent architecture, system prompts, tools, structured outputs
  content: Agent components, execution methods, configuration options

- url: https://ai.pydantic.dev/models/
  why: Model provider configuration, API key management, fallback models
  content: OpenAI, Anthropic, Gemini integration patterns and authentication

- url: https://ai.pydantic.dev/tools/
  why: Function tool registration, context usage, rich returns, dynamic tools
  content: Tool decorators, parameter validation, documentation patterns

- url: https://ai.pydantic.dev/testing/
  why: Testing strategies, TestModel, FunctionModel, pytest patterns
  content: Unit testing, agent behavior validation, mock model usage

- url: https://ai.pydantic.dev/examples/
  why: Working examples for various PydanticAI use cases
  content: Chat apps, RAG systems, SQL generation, FastAPI integration

# CONTEXT ENGINEERING FOUNDATION - Base framework to adapt
- file: ../../../README.md
  why: Core context engineering principles and workflow to adapt for AI agents

- file: ../../../.claude/commands/generate-prp.md
  why: Base PRP generation patterns to specialize for PydanticAI development

- file: ../../../.claude/commands/execute-prp.md  
  why: Base PRP execution patterns to adapt for AI agent validation

- file: ../../../PRPs/templates/prp_base.md
  why: Base PRP template structure to specialize for PydanticAI domain

# MCP SERVER EXAMPLE - Reference implementation
- file: ../mcp-server/CLAUDE.md
  why: Example of domain-specific implementation guide patterns
  
- file: ../mcp-server/.claude/commands/prp-mcp-create.md
  why: Example of specialized PRP generation command structure
```

### PydanticAI 框架分析（来自研究）

```typescript
// PydanticAI Architecture Patterns (from official docs)
interface PydanticAIPatterns {
  // Core agent patterns
  agent_creation: {
    model_providers: ["openai:gpt-4o", "anthropic:claude-3-sonnet", "google:gemini-1.5-flash"];
    configuration: ["system_prompt", "deps_type", "output_type", "instructions"];
    execution_methods: ["run()", "run_sync()", "run_stream()", "iter()"];
  };
  
  // Tool integration patterns
  tool_system: {
    registration: ["@agent.tool", "@agent.tool_plain", "tools=[]"];
    context_access: ["RunContext[DepsType]", "ctx.deps", "dependency_injection"];
    return_types: ["str", "ToolReturn", "structured_data", "rich_content"];
    validation: ["parameter_schemas", "docstring_extraction", "type_hints"];
  };
  
  // Testing and validation
  testing_patterns: {
    unit_testing: ["TestModel", "FunctionModel", "Agent.override()"];
    validation: ["capture_run_messages()", "pytest_fixtures", "mock_dependencies"];
    evals: ["model_performance", "agent_behavior", "production_monitoring"];
  };
  
  // Production considerations
  security: {
    api_keys: ["environment_variables", "secure_storage", "key_rotation"];
    input_validation: ["pydantic_models", "parameter_validation", "sanitization"];
    monitoring: ["logfire_integration", "usage_tracking", "error_handling"];
  };
}
```

### 开发工作流分析（来自研究）

```yaml
# PydanticAI Development Patterns (researched from docs and examples)
project_structure:
  basic_pattern: |
    my_agent/
    ├── agent.py          # Main agent definition
    ├── tools.py          # Tool functions
    ├── models.py         # Pydantic output models
    ├── dependencies.py   # Context dependencies
    └── tests/
        ├── test_agent.py
        └── test_tools.py

  advanced_pattern: |
    agents_project/
    ├── agents/
    │   ├── __init__.py
    │   ├── chat_agent.py
    │   └── workflow_agent.py
    ├── tools/
    │   ├── __init__.py
    │   ├── web_search.py
    │   └── calculator.py
    ├── models/
    │   ├── __init__.py
    │   └── outputs.py
    ├── dependencies/
    │   ├── __init__.py
    │   └── database.py
    ├── tests/
    └── examples/

package_management:
  installation: "pip install pydantic-ai"
  optional_deps: "pip install 'pydantic-ai[examples]'"
  dev_deps: "pip install pytest pytest-asyncio inline-snapshot dirty-equals"

testing_workflow:
  unit_tests: "pytest tests/ -v"
  agent_testing: "Use TestModel for fast validation"
  integration_tests: "Use real models with rate limiting"
  evals: "Run performance benchmarks separately"

environment_setup:
  api_keys: ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY"]
  development: "Set ALLOW_MODEL_REQUESTS=False for testing"
  production: "Configure proper logging and monitoring"
```

### 安全性和最佳实践（来自研究）

```typescript
// Security patterns specific to PydanticAI (from research)
interface PydanticAISecurity {
  // API key management
  api_security: {
    storage: "environment_variables_only";
    access_control: "minimal_required_permissions";
    monitoring: "usage_tracking_and_alerts";
  };
  
  // Input validation and sanitization
  input_security: {
    validation: "pydantic_models_for_all_inputs";
    sanitization: "escape_user_content";
    rate_limiting: "prevent_abuse_patterns";
    content_filtering: "block_malicious_prompts";
  };
  
  // Prompt injection prevention
  prompt_security: {
    system_prompts: "clear_instruction_boundaries";
    user_input: "validate_and_sanitize";
    tool_calls: "parameter_validation";
    output_filtering: "structured_response_validation";
  };
  
  // Production considerations
  production_security: {
    monitoring: "logfire_integration_recommended";
    error_handling: "no_sensitive_data_in_logs";
    dependency_injection: "secure_context_management";
    testing: "security_focused_unit_tests";
  };
}
```

### 常见陷阱和边缘情况（来自研究）

```yaml
# PydanticAI-specific gotchas discovered through research
agent_gotchas:
  model_limits:
    issue: "Different models have different token limits and capabilities"
    solution: "Use FallbackModel for automatic model switching"
    validation: "Test with multiple model providers"
  
  async_patterns:
    issue: "Mixing sync and async agent calls can cause issues"
    solution: "Consistent async/await patterns throughout"
    validation: "Test both sync and async execution paths"
  
  dependency_injection:
    issue: "Complex dependency graphs can be hard to debug"
    solution: "Keep dependencies simple and well-typed"
    validation: "Unit test dependencies in isolation"

tool_integration_gotchas:
  parameter_validation:
    issue: "Tools may receive unexpected parameter types"
    solution: "Use strict Pydantic models for tool parameters"
    validation: "Test tools with invalid inputs"
  
  context_management:
    issue: "RunContext state can become inconsistent"
    solution: "Design stateless tools when possible"
    validation: "Test context isolation between runs"
  
  error_handling:
    issue: "Tool errors can crash entire agent runs"
    solution: "Implement retry mechanisms and graceful degradation"
    validation: "Test error scenarios and recovery"

testing_gotchas:
  model_costs:
    issue: "Real model testing can be expensive"
    solution: "Use TestModel and FunctionModel for development"
    validation: "Separate unit tests from expensive eval runs"
  
  async_testing:
    issue: "Async agent testing requires special setup"
    solution: "Use pytest-asyncio and proper fixtures"
    validation: "Test both sync and async code paths"
  
  deterministic_behavior:
    issue: "AI responses are inherently non-deterministic"
    solution: "Focus on testing tool calls and structured outputs"
    validation: "Use inline-snapshot for complex assertions"
```

## 实现蓝图

### 技术研究阶段（已完成）

**全面的 PydanticAI 分析已完成：**

✅ **Core Framework Analysis:** 
- PydanticAI architecture, agent creation patterns, model provider integration
- Project structure conventions from official docs and examples
- Dependency injection system and type-safe design principles
- Development workflow with async/sync patterns and streaming support

✅ **Tool System Investigation:**
- Function tool registration patterns (@agent.tool vs @agent.tool_plain)
- Context management with RunContext and dependency injection
- Parameter validation, docstring extraction, and schema generation
- Rich return types and multi-modal content support

✅ **Testing Framework Analysis:**
- TestModel and FunctionModel for unit testing without API calls
- Agent.override() patterns for test isolation
- Pytest integration with async testing and fixtures
- Evaluation strategies for model performance vs unit testing

✅ **Security and Production Patterns:**
- API key management with environment variables and secure storage
- Input validation using Pydantic models and parameter schemas
- Rate limiting, monitoring, and Logfire integration
- Common security vulnerabilities and prevention strategies

### 模板包生成

基于研究结果创建完整的 PydanticAI 上下文工程模板：

```yaml
Generation Task 1 - Create PydanticAI Template Directory Structure:
  CREATE complete use case directory structure:
    - use-cases/pydantic-ai/
    - .claude/commands/ with PydanticAI-specific slash commands
    - PRPs/templates/ with agent-focused base template
    - examples/ with working agent implementations
    - All subdirectories per template package requirements

Generation Task 2 - Generate PydanticAI-Specific CLAUDE.md:
  CREATE PydanticAI global rules file including:
    - PydanticAI agent creation and tool integration patterns
    - Model provider configuration and API key management
    - Agent architecture patterns (chat, workflow, tool-enabled)
    - Testing strategies with TestModel/FunctionModel
    - Security best practices for AI agents and tool integration
    - Common gotchas: async patterns, context management, model limits

Generation Task 3 - Create PydanticAI PRP Commands:
  GENERATE domain-specific slash commands:
    - generate-pydantic-ai-prp.md with agent research patterns
    - execute-pydantic-ai-prp.md with AI agent validation loops
    - Include PydanticAI documentation references and research strategies
    - Agent-specific success criteria and testing requirements

Generation Task 4 - Develop PydanticAI Base PRP Template:
  CREATE specialized prp_pydantic_ai_base.md template:
    - Pre-filled with agent architecture patterns from research
    - PydanticAI-specific success criteria and validation gates
    - Official documentation references and model provider guides
    - Agent testing patterns with TestModel and validation strategies

Generation Task 5 - Create Working PydanticAI Examples:
  GENERATE comprehensive example agents:
    - basic_chat_agent: Simple conversation with memory
    - tool_enabled_agent: Web search and calculator integration
    - workflow_agent: Multi-step task processing
    - structured_output_agent: Custom Pydantic models
    - testing_examples: Unit tests and validation patterns
    - Include configuration files and environment setup

Generation Task 6 - Create Template Copy Script:
  CREATE Python script for template deployment:
    - copy_template.py with command-line interface
    - Copies entire PydanticAI template structure to target location
    - Handles all files: CLAUDE.md, commands, PRPs, examples, etc.
    - Error handling and success feedback with next steps

Generation Task 7 - Generate Comprehensive README:
  CREATE PydanticAI-specific README.md:
    - Clear description: "PydanticAI Context Engineering Template"
    - Template copy script usage (prominently at top)
    - PRP framework workflow for AI agent development
    - Template structure with PydanticAI-specific explanations
    - Quick start guide with agent creation examples
    - Working examples overview and testing patterns
```

### PydanticAI 专业化详情

```typescript
// Template specialization for PydanticAI
const pydantic_ai_specialization = {
  agent_patterns: [
    "chat_agent_with_memory",
    "tool_integrated_agent", 
    "workflow_processing_agent",
    "structured_output_agent"
  ],
  
  validation: [
    "agent_behavior_testing",
    "tool_function_validation", 
    "output_schema_verification",
    "model_provider_compatibility"
  ],
  
  examples: [
    "basic_conversation_agent",
    "web_search_calculator_tools",
    "multi_step_workflow_processing",
    "custom_pydantic_output_models",
    "comprehensive_testing_suite"
  ],
  
  gotchas: [
    "async_sync_mixing_issues",
    "model_token_limits",
    "dependency_injection_complexity",
    "tool_error_handling_failures",
    "context_state_management"
  ],
  
  security: [
    "api_key_environment_management",
    "input_validation_pydantic_models",
    "prompt_injection_prevention",
    "rate_limiting_implementation",
    "secure_tool_parameter_handling"
  ]
};
```

### 集成点

```yaml
CONTEXT_ENGINEERING_FRAMEWORK:
  - base_workflow: Inherit PRP generation/execution, adapt for AI agent development
  - validation_principles: Extend with AI-specific testing (agent behavior, tool validation)
  - documentation_standards: Maintain consistency while specializing for PydanticAI

PYDANTIC_AI_INTEGRATION:
  - agent_architecture: Include chat, tool-enabled, and workflow agent patterns
  - model_providers: Support OpenAI, Anthropic, Gemini configuration patterns
  - testing_framework: Use TestModel/FunctionModel for development validation
  - production_patterns: Include security, monitoring, and deployment considerations

TEMPLATE_STRUCTURE:
  - directory_organization: Follow use case template patterns with AI-specific examples
  - file_naming: generate-pydantic-ai-prp.md, prp_pydantic_ai_base.md
  - content_format: Markdown with agent code examples and configuration
  - command_patterns: Extend slash commands for AI agent development workflows
```

## 验证循环

### 级别 1：PydanticAI 模板结构验证

```bash
# Verify complete PydanticAI template package structure
find use-cases/pydantic-ai -type f | sort
ls -la use-cases/pydantic-ai/.claude/commands/
ls -la use-cases/pydantic-ai/PRPs/templates/
ls -la use-cases/pydantic-ai/examples/

# Verify copy script and agent examples
test -f use-cases/pydantic-ai/copy_template.py
ls use-cases/pydantic-ai/examples/*/agent.py 2>/dev/null | wc -l  # Should have agent files
python use-cases/pydantic-ai/copy_template.py --help 2>/dev/null || echo "Copy script needs help"

# Expected: All required files including working agent examples
# If missing: Generate missing components with PydanticAI patterns
```

### 级别 2：PydanticAI 内容质量验证

```bash
# Verify PydanticAI-specific content accuracy
grep -r "from pydantic_ai import Agent" use-cases/pydantic-ai/examples/
grep -r "@agent.tool" use-cases/pydantic-ai/examples/
grep -r "TestModel\|FunctionModel" use-cases/pydantic-ai/

# Check for PydanticAI patterns and avoid generic content
grep -r "TODO\|PLACEHOLDER" use-cases/pydantic-ai/
grep -r "openai:gpt-4o\|anthropic:" use-cases/pydantic-ai/
grep -r "RunContext\|deps_type" use-cases/pydantic-ai/

# Expected: Real PydanticAI code, no placeholders, agent patterns present
# If issues: Add proper PydanticAI-specific patterns and examples
```

### 级别 3：PydanticAI 功能验证

```bash
# Test PydanticAI template functionality
cd use-cases/pydantic-ai

# Test PRP generation with agent focus
/generate-pydantic-ai-prp INITIAL.md
ls PRPs/*.md | grep -v templates | head -1  # Should generate agent PRP

# Verify agent examples can be parsed (syntax check)
python -m py_compile examples/basic_chat_agent/agent.py 2>/dev/null && echo "Basic agent syntax OK"
python -m py_compile examples/tool_enabled_agent/agent.py 2>/dev/null && echo "Tool agent syntax OK"

# Expected: PRP generation works, agent examples have valid syntax
# If failing: Debug PydanticAI command patterns and fix agent code
```

### 级别 4：PydanticAI 集成测试

```bash
# Verify PydanticAI specialization maintains base framework compatibility
diff -r ../../.claude/commands/ .claude/commands/ | head -10
grep -r "Context is King" . | wc -l  # Should inherit base principles
grep -r "pydantic.ai.dev\|PydanticAI" . | wc -l  # Should have specializations

# Test agent examples have proper dependencies
grep -r "pydantic_ai" examples/ | wc -l  # Should import PydanticAI
grep -r "pytest" examples/testing_examples/ | wc -l  # Should have tests

# Expected: Proper specialization, working agent patterns, testing included
# If issues: Adjust to maintain compatibility while adding PydanticAI features
```

## 最终验证清单

### PydanticAI 模板包完整性

- [ ] Complete directory structure: `tree use-cases/pydantic-ai`
- [ ] PydanticAI-specific files: CLAUDE.md with agent patterns, specialized commands
- [ ] Copy script present: `copy_template.py` with proper PydanticAI functionality
- [ ] README comprehensive: Includes agent development workflow and copy instructions
- [ ] Agent examples working: All examples use real PydanticAI code patterns
- [ ] Testing patterns included: TestModel/FunctionModel examples and validation
- [ ] Documentation complete: PydanticAI-specific patterns and gotchas documented

### PydanticAI 的质量和可用性

- [ ] No placeholder content: `grep -r "TODO\|PLACEHOLDER"` returns empty
- [ ] PydanticAI specialization: Agent patterns, tools, testing properly documented
- [ ] Validation loops work: All commands executable with agent-specific functionality
- [ ] Framework integration: Works with base context engineering for AI development
- [ ] Ready for AI development: Developers can immediately create PydanticAI agents

### PydanticAI 框架集成

- [ ] Inherits base principles: Context engineering workflow preserved for AI agents
- [ ] Proper AI specialization: PydanticAI patterns, security, testing included
- [ ] Command compatibility: Slash commands work for agent development workflows
- [ ] Documentation consistency: Follows patterns while specializing for AI development
- [ ] Maintainable structure: Easy to update as PydanticAI framework evolves

---

## 要避免的反模式

### PydanticAI 模板生成

- ❌ Don't create generic AI templates - research PydanticAI specifics thoroughly
- ❌ Don't skip agent architecture research - understand tools, memory, validation
- ❌ Don't use placeholder agent code - include real, working PydanticAI examples
- ❌ Don't ignore testing patterns - TestModel/FunctionModel are critical for AI

### PydanticAI 内容质量

- ❌ Don't assume AI patterns - document PydanticAI-specific gotchas explicitly
- ❌ Don't skip security research - API keys, input validation, prompt injection critical
- ❌ Don't ignore model providers - include OpenAI, Anthropic, Gemini patterns
- ❌ Don't forget async patterns - PydanticAI has specific async/sync considerations

### PydanticAI 框架集成

- ❌ Don't break context engineering - maintain PRP workflow for AI development
- ❌ Don't duplicate base functionality - extend and specialize appropriately
- ❌ Don't ignore AI-specific validation - agent behavior testing is unique requirement
- ❌ Don't skip real examples - include working agents with tools and validation

**CONFIDENCE SCORE: 9/10** - Comprehensive PydanticAI research completed, framework patterns understood, ready to generate specialized context engineering template for AI agent development.