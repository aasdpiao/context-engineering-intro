# 上下文工程模板

一个全面的上下文工程入门模板 - 上下文工程是为AI编程助手设计上下文的学科，使其拥有端到端完成工作所需的信息。

> **上下文工程比提示工程好10倍，比随意编程好100倍。**

## 🚀 快速开始

```bash
# 1. 克隆此模板
git clone https://github.com/coleam00/Context-Engineering-Intro.git
cd Context-Engineering-Intro

# 2. 设置项目规则（可选 - 已提供模板）
# 编辑 CLAUDE.md 添加项目特定的指导原则

# 3. 添加示例（强烈推荐）
# 在 examples/ 文件夹中放置相关代码示例

# 4. 创建初始功能请求
# 编辑 INITIAL.md 填写功能需求

# 5. 生成综合性PRP（产品需求提示）
# 在 Claude Code 中运行：
/generate-prp INITIAL.md

# 6. 执行PRP来实现功能
# 在 Claude Code 中运行：
/execute-prp PRPs/your-feature-name.md
```

## 📚 目录

- [什么是上下文工程？](#什么是上下文工程)
- [模板结构](#模板结构)
- [分步指南](#分步指南)
- [编写有效的INITIAL.md文件](#编写有效的initialmd文件)
- [PRP工作流程](#prp工作流程)
- [有效使用示例](#有效使用示例)
- [最佳实践](#最佳实践)

## 什么是上下文工程？

上下文工程代表了从传统提示工程的范式转变：

### 提示工程 vs 上下文工程

**提示工程：**
- 专注于巧妙的措辞和特定的表达
- 局限于如何表述任务
- 就像给某人一张便利贴

**上下文工程：**
- 提供全面上下文的完整系统
- 包括文档、示例、规则、模式和验证
- 就像编写包含所有细节的完整剧本

### 为什么上下文工程很重要

1. **减少AI失败**：大多数代理失败不是模型失败 - 而是上下文失败
2. **确保一致性**：AI遵循你的项目模式和约定
3. **启用复杂功能**：AI可以通过适当的上下文处理多步骤实现
4. **自我纠正**：验证循环允许AI修复自己的错误

## 模板结构

```
context-engineering-intro/
├── .claude/
│   ├── commands/
│   │   ├── generate-prp.md    # 生成综合性PRP
│   │   └── execute-prp.md     # 执行PRP来实现功能
│   └── settings.local.json    # Claude Code权限设置
├── PRPs/
│   ├── templates/
│   │   └── prp_base.md       # PRP基础模板
│   └── EXAMPLE_multi_agent_prp.md  # 完整PRP示例
├── examples/                  # 你的代码示例（关键！）
├── CLAUDE.md                 # AI助手全局规则
├── INITIAL.md               # 功能请求模板
├── INITIAL_EXAMPLE.md       # 功能请求示例
└── README.md                # 本文件
```

这个模板不专注于RAG和上下文工程工具，因为我很快会有更多相关内容。;)

## 分步指南

### 1. 设置全局规则 (CLAUDE.md)

`CLAUDE.md` 文件包含AI助手在每次对话中都会遵循的项目范围规则。模板包括：

- **项目意识**：阅读规划文档，检查任务
- **代码结构**：文件大小限制，模块组织
- **测试要求**：单元测试模式，覆盖率期望
- **风格约定**：语言偏好，格式规则
- **文档标准**：文档字符串格式，注释实践

**你可以直接使用提供的模板，或为你的项目进行自定义。**

### 2. 创建初始功能请求

编辑 `INITIAL.md` 来描述你想要构建的内容：

```markdown
## FEATURE:
[描述你想要构建的内容 - 具体说明功能和需求]

## EXAMPLES:
[列出examples/文件夹中的任何示例文件并解释如何使用它们]

## DOCUMENTATION:
[包含相关文档、API或MCP服务器资源的链接]

## OTHER CONSIDERATIONS:
[提及任何陷阱、特定需求或AI助手常常遗漏的事项]
```

**查看 `INITIAL_EXAMPLE.md` 获取完整示例。**

### 3. 生成PRP

PRP（产品需求提示）是包含以下内容的综合实现蓝图：

- 完整的上下文和文档
- 带验证的实现步骤
- 错误处理模式
- 测试要求

它们类似于PRD（产品需求文档），但更专门用于指导AI编程助手。

在Claude Code中运行：
```bash
/generate-prp INITIAL.md
```

**注意：** 斜杠命令是在 `.claude/commands/` 中定义的自定义命令。你可以查看它们的实现：
- `.claude/commands/generate-prp.md` - 查看它如何研究和创建PRP
- `.claude/commands/execute-prp.md` - 查看它如何从PRP实现功能

这些命令中的 `$ARGUMENTS` 变量接收你在命令名后传递的任何内容（例如，`INITIAL.md` 或 `PRPs/your-feature.md`）。

此命令将：
1. 读取你的功能请求
2. 研究代码库中的模式
3. 搜索相关文档
4. 在 `PRPs/your-feature-name.md` 中创建综合性PRP

### 4. 执行PRP

生成后，执行PRP来实现你的功能：

```bash
/execute-prp PRPs/your-feature-name.md
```

AI编程助手将：
1. 从PRP中读取所有上下文
2. 创建详细的实现计划
3. 执行每个步骤并进行验证
4. 运行测试并修复任何问题
5. 确保满足所有成功标准

## 编写有效的INITIAL.md文件

### 关键部分说明

**FEATURE**: 要具体和全面
- ❌ "构建一个网页爬虫"
- ✅ "使用BeautifulSoup构建异步网页爬虫，从电商网站提取产品数据，处理速率限制，并将结果存储在PostgreSQL中"

**EXAMPLES**: 利用examples/文件夹
- 在 `examples/` 中放置相关代码模式
- 引用要遵循的特定文件和模式
- 解释应该模仿的方面

**DOCUMENTATION**: 包含所有相关资源
- API文档URL
- 库指南
- MCP服务器文档
- 数据库架构

**OTHER CONSIDERATIONS**: 捕获重要细节
- 身份验证要求
- 速率限制或配额
- 常见陷阱
- 性能要求

## PRP工作流程

### /generate-prp 如何工作

该命令遵循以下过程：

1. **研究阶段**
   - 分析你的代码库中的模式
   - 搜索类似的实现
   - 识别要遵循的约定

2. **文档收集**
   - 获取相关API文档
   - 包含库文档
   - 添加陷阱和特殊情况

3. **蓝图创建**
   - 创建分步实现计划
   - 包含验证关卡
   - 添加测试要求

4. **质量检查**
   - 评分信心水平（1-10）
   - 确保包含所有上下文

### /execute-prp 如何工作

1. **加载上下文**：读取整个PRP
2. **制定计划**：使用TodoWrite创建详细任务列表
3. **执行**：实现每个组件
4. **验证**：运行测试和代码检查
5. **迭代**：修复发现的任何问题
6. **完成**：确保满足所有要求

查看 `PRPs/EXAMPLE_multi_agent_prp.md` 获取生成内容的完整示例。

## 有效使用示例

`examples/` 文件夹对成功**至关重要**。AI编程助手在能看到要遵循的模式时表现得更好。

### 示例中应包含什么

1. **代码结构模式**
   - 如何组织模块
   - 导入约定
   - 类/函数模式

2. **测试模式**
   - 测试文件结构
   - 模拟方法
   - 断言风格

3. **集成模式**
   - API客户端实现
   - 数据库连接
   - 身份验证流程

4. **CLI模式**
   - 参数解析
   - 输出格式化
   - 错误处理

### 示例结构

```
examples/
├── README.md           # 解释每个示例展示的内容
├── cli.py             # CLI实现模式
├── agent/             # 代理架构模式
│   ├── agent.py      # 代理创建模式
│   ├── tools.py      # 工具实现模式
│   └── providers.py  # 多提供商模式
└── tests/            # 测试模式
    ├── test_agent.py # 单元测试模式
    └── conftest.py   # Pytest配置
```

## 最佳实践

### 1. 在INITIAL.md中要明确
- 不要假设AI知道你的偏好
- 包含具体的要求和约束
- 大量引用示例

### 2. 提供全面的示例
- 更多示例 = 更好的实现
- 展示应该做什么和不应该做什么
- 包含错误处理模式

### 3. 使用验证关卡
- PRP包含必须通过的测试命令
- AI将迭代直到所有验证成功
- 这确保第一次就能得到可工作的代码

### 4. 利用文档
- 包含官方API文档
- 添加MCP服务器资源
- 引用特定的文档章节

### 5. 自定义CLAUDE.md
- 添加你的约定
- 包含项目特定的规则
- 定义编码标准

## 资源

- [Claude Code 文档](https://docs.anthropic.com/en/docs/claude-code)
- [上下文工程最佳实践](https://www.philschmid.de/context-engineering)