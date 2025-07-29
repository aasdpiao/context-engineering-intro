# MCP服务器构建器 - 上下文工程用例

此用例演示如何使用**上下文工程**和**PRP（产品需求提示）流程**来构建生产就绪的模型上下文协议（MCP）服务器。它提供了一个经过验证的模板和工作流程，用于创建具有GitHub OAuth身份验证、数据库集成和Cloudflare Workers部署的MCP服务器。

> PRP是PRD + 精选代码库智能 + 代理/运行手册——AI在第一次尝试中合理交付生产就绪代码所需的最小可行包。

## 🚀 快速开始

### 前置条件

- 已安装Node.js和npm
- Cloudflare账户（免费层即可）
- 用于OAuth的GitHub账户
- PostgreSQL数据库（本地或托管）

### 步骤1：设置你的项目

```bash
# 克隆上下文工程仓库
git clone https://github.com/coleam00/Context-Engineering-Intro.git
cd Context-Engineering-Intro/use-cases/mcp-server

# 将模板复制到你的新项目目录
python copy_template.py my-mcp-server-project

# 导航到你的新项目
cd my-mcp-server-project

# 安装依赖项
npm install

# 全局安装Wrangler CLI
npm install -g wrangler

# 使用Cloudflare进行身份验证
wrangler login
```

**copy_template.py的作用：**
- 复制除构建产物外的所有模板文件（遵循.gitignore）
- 将README.md重命名为README_TEMPLATE.md（这样你可以创建自己的README）
- 包含所有源代码、示例、测试和配置文件
- 保留完整的上下文工程设置

## 🎯 你将学到什么

此用例教你如何：

- **使用PRP流程**系统性地构建复杂的MCP服务器
- **利用专门的上下文工程**进行MCP开发
- **遵循经过验证的模式**来自生产就绪的MCP服务器模板
- **实现安全身份验证**，包括GitHub OAuth和基于角色的访问
- **部署到Cloudflare Workers**，具备监控和错误处理

## 📋 工作原理 - MCP服务器的PRP流程

> **步骤1是上面的快速开始设置** - 克隆仓库、复制模板、安装依赖项、设置Wrangler

### 步骤2：定义你的MCP服务器

编辑`PRPs/INITIAL.md`来描述你的特定MCP服务器需求：

```markdown
## FEATURE:
我们想要创建一个天气MCP服务器，提供实时天气数据
并具备缓存和速率限制功能。

## ADDITIONAL FEATURES:
- 与OpenWeatherMap API集成
- Redis缓存以提高性能
- 每用户速率限制
- 历史天气数据访问
- 位置搜索和自动完成

## OTHER CONSIDERATIONS:
- 外部服务的API密钥管理
- API失败的适当错误处理
- 位置查询的坐标验证
```

### 步骤3：生成你的PRP

使用专门的MCP PRP命令创建综合实现计划：

```bash
/prp-mcp-create INITIAL.md
```

**这个命令的作用：**
- 读取你的功能请求
- 研究现有的MCP代码库模式
- 学习身份验证和数据库集成模式
- 在`PRPs/your-server-name.md`中创建综合PRP
- 包含所有上下文、验证循环和逐步任务

> 在生成PRP后验证一切是很重要的！在PRP框架中，你应该参与流程以确保所有上下文的质量！执行的好坏取决于你的PRP。使用/prp-mcp-create作为一个坚实的起点。

### Step 4: Execute Your PRP

Use the specialized MCP execution command to build your server:

```bash
/prp-mcp-execute PRPs/your-server-name.md
```

**What this does:**
- Loads the complete PRP with all context
- Creates a detailed implementation plan using TodoWrite
- Implements each component following proven patterns
- Runs comprehensive validation (TypeScript, tests, deployment)
- Ensures your MCP server works end-to-end

### Step 5: Configure Environment

```bash
# Create environment file
cp .dev.vars.example .dev.vars

# Edit .dev.vars with your credentials
# - GitHub OAuth app credentials
# - Database connection string
# - Cookie encryption key
```

### Step 6: Test and Deploy

```bash
# Test locally
wrangler dev --config <your wrangler config (.jsonc)>

# Test with MCP Inspector
npx @modelcontextprotocol/inspector@latest
# Connect to: http://localhost:8792/mcp

# Deploy to production
wrangler deploy
```

## 🏗️ MCP-Specific Context Engineering

This use case includes specialized context engineering components designed specifically for MCP server development:

### Specialized Slash Commands

Located in `.claude/commands/`:

- **`/prp-mcp-create`** - Generates PRPs specifically for MCP servers
- **`/prp-mcp-execute`** - Executes MCP PRPs with comprehensive validation

These are specialized versions of the generic commands in the root `.claude/commands/`, but tailored for MCP development patterns.

### Specialized PRP Template

The template `PRPs/templates/prp_mcp_base.md` includes:

- **MCP-specific patterns** for tool registration and authentication
- **Cloudflare Workers configuration** for deployment
- **GitHub OAuth integration** patterns
- **Database security** and SQL injection protection
- **Comprehensive validation loops** from TypeScript to production

### AI Documentation

The `PRPs/ai_docs/` folder contains:

- **`mcp_patterns.md`** - Core MCP development patterns and security practices
- **`claude_api_usage.md`** - How to integrate with Anthropic's API for LLM-powered features

## 🔧 Template Architecture

This template provides a complete, production-ready MCP server with:

### Core Components

```
src/
├── index.ts                 # Main authenticated MCP server
├── index_sentry.ts         # Version with Sentry monitoring
├── simple-math.ts          # Basic MCP example (no auth)
├── github-handler.ts       # Complete GitHub OAuth implementation
├── database.ts             # PostgreSQL with security patterns
├── utils.ts                # OAuth helpers and utilities
├── workers-oauth-utils.ts  # HMAC-signed cookie system
└── tools/                  # Modular tool registration system
    └── register-tools.ts   # Central tool registry
```

### Example Tools

The `examples/` folder shows how to create MCP tools:

- **`database-tools.ts`** - Example database tools with proper patterns
- **`database-tools-sentry.ts`** - Same tools with Sentry monitoring

### Key Features

- **🔐 GitHub OAuth** - Complete authentication flow with role-based access
- **🗄️ Database Integration** - PostgreSQL with connection pooling and security
- **🛠️ Modular Tools** - Clean separation of concerns with central registration
- **☁️ Cloudflare Workers** - Global edge deployment with Durable Objects
- **📊 Monitoring** - Optional Sentry integration for production
- **🧪 Testing** - Comprehensive validation from TypeScript to deployment

## 🔍 Key Files to Understand

To fully understand this use case, examine these files:

### Context Engineering Components

- **`PRPs/templates/prp_mcp_base.md`** - Specialized MCP PRP template
- **`.claude/commands/prp-mcp-create.md`** - MCP-specific PRP generation
- **`.claude/commands/prp-mcp-execute.md`** - MCP-specific execution

### Implementation Patterns

- **`src/index.ts`** - Complete MCP server with authentication
- **`examples/database-tools.ts`** - Tool creation and registration patterns
- **`src/tools/register-tools.ts`** - Modular tool registration system

### Configuration & Deployment

- **`wrangler.jsonc`** - Cloudflare Workers configuration
- **`.dev.vars.example`** - Environment variable template
- **`CLAUDE.md`** - Implementation guidelines and patterns

## 📈 Success Metrics

When you successfully use this process, you'll achieve:

- **Fast Implementation** - Quickly have an MCP Server with minimal iterations
- **Production Ready** - Secure authentication, monitoring, and error handling
- **Scalable Architecture** - Clean separation of concerns and modular design
- **Comprehensive Testing** - Validation from TypeScript to production deployment

## 🤝 Contributing

This use case demonstrates the power of Context Engineering for complex software development. To improve it:

1. **Add new MCP server examples** to show different patterns
2. **Enhance the PRP templates** with more comprehensive context
3. **Improve validation loops** for better error detection
4. **Document edge cases** and common pitfalls

The goal is to make MCP server development predictable and successful through comprehensive context engineering.

---

**Ready to build your MCP server?** Follow the complete process above: setup your project with the copy template, configure your environment, define your requirements in `PRPs/INITIAL.md`, then generate and execute your PRP to build your production-ready MCP server.