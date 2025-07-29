---
name: "MCP 服务器 PRP 模板"
description: 此模板旨在使用此代码库中经过验证的模式提供生产就绪的模型上下文协议 (MCP) 服务器。
---

## 目的

为 AI 智能体优化的模板，用于实现生产就绪的模型上下文协议 (MCP) 服务器，包含 GitHub OAuth 认证、数据库集成和 Cloudflare Workers 部署，使用此代码库中经过验证的模式。

## 核心原则

1. **上下文为王**：包含所有必要的 MCP 模式、认证流程和部署配置
2. **验证循环**：提供从 TypeScript 编译到生产部署的可执行测试
3. **安全优先**：内置认证、授权和 SQL 注入保护
4. **生产就绪**：包含监控、错误处理和部署自动化

---

## 目标

构建生产就绪的 MCP（模型上下文协议）服务器，包含：

- [特定 MCP 功能] - 描述要实现的特定工具和资源
- 带有基于角色访问控制的 GitHub OAuth 认证
- 带有监控的 Cloudflare Workers 部署
- [附加功能] - 基础认证/数据库之外的任何特定功能

## 原因

- **开发者生产力**：为 AI 助手提供对 [特定数据/操作] 的安全访问
- **企业安全**：带有细粒度权限系统的 GitHub OAuth
- **可扩展性**：Cloudflare Workers 全球边缘部署
- **集成**：[如何与现有系统集成]
- **用户价值**：[对最终用户的特定好处]

## 内容

### MCP 服务器功能

**核心 MCP 工具：**

- 工具以模块化文件组织，通过 `src/tools/register-tools.ts` 注册
- 每个功能/领域都有自己的工具注册文件（例如，`database-tools.ts`、`analytics-tools.ts`）
- [列出特定工具] - 例如，"queryDatabase"、"listTables"、"executeOperations"
- 用户认证和权限验证在工具注册期间进行
- 全面的错误处理和日志记录
- [领域特定工具] - 特定于您用例的工具

**认证与授权：**

- 带有签名 cookie 批准系统的 GitHub OAuth 2.0 集成
- 基于角色的访问控制（只读用户 vs 特权用户）
- 用户上下文传播到所有 MCP 工具
- 使用 HMAC 签名 cookie 的安全会话管理

**数据库集成：**

- 带有自动清理的 PostgreSQL 连接池
- SQL 注入保护和查询验证
- 基于用户权限的读/写操作分离
- 错误清理以防止信息泄露

**部署与监控：**

- 带有 Durable Objects 状态管理的 Cloudflare Workers
- 可选的 Sentry 集成用于错误跟踪和性能监控
- 基于环境的配置（开发 vs 生产）
- 实时日志记录和告警

### 成功标准

- [ ] MCP 服务器通过 MCP Inspector 验证
- [ ] GitHub OAuth 流程端到端工作（授权 → 回调 → MCP 访问）
- [ ] TypeScript 编译成功且无错误
- [ ] 本地开发服务器启动并正确响应
- [ ] 成功部署到 Cloudflare Workers 生产环境
- [ ] 认证阻止对敏感操作的未授权访问
- [ ] 错误处理提供用户友好的消息而不泄露系统详细信息
- [ ] [领域特定成功标准]

## 所需的所有上下文

### 文档与参考资料（必读）

```yaml
# 关键 MCP 模式 - 首先阅读这些
- docfile: PRPs/ai_docs/mcp_patterns.md
  why: 核心 MCP 开发模式、安全实践和错误处理

# 关键代码示例
- docfile: PRPs/ai_docs/claude_api_usage.md
  why: 如何使用 Anthropic API 从 LLM 获取响应

# 工具注册系统 - 理解模块化方法
- file: src/tools/register-tools.ts
  why: 显示所有工具如何导入和注册的中央注册表 - 研究此模式

# MCP 工具示例 - 查看如何创建和注册新工具
- file: examples/database-tools.ts
  why: Postgres MCP 服务器的示例工具，展示工具创建和注册的最佳实践

- file: examples/database-tools-sentry.ts
  why: Postgres MCP 服务器的示例工具，但集成了 Sentry 用于生产监控

# 现有代码库模式 - 研究这些实现
- file: src/index.ts
  why: 带有认证、数据库和工具的完整 MCP 服务器 - 镜像此模式

- file: src/github-handler.ts
  why: OAuth 流程实现 - 使用此确切模式进行认证

- file: src/database.ts
  why: 数据库安全、连接池、SQL 验证 - 遵循这些模式

- file: wrangler.jsonc
  why: Cloudflare Workers 配置 - 复制此模式进行部署

# 官方 MCP 文档
- url: https://modelcontextprotocol.io/docs/concepts/tools
  why: MCP 工具注册和模式定义模式

- url: https://modelcontextprotocol.io/docs/concepts/resources
  why: 如果需要，MCP 资源实现

# 根据需要在下面添加与用户用例相关的文档
```

### 当前代码库树结构（在项目根目录运行 `tree -I node_modules`）

```bash
# 在此处插入实际的树输出
/
├── src/
│   ├── index.ts                 # 主要的认证 MCP 服务器 ← 研究此文件
│   ├── index_sentry.ts         # Sentry 监控版本
│   ├── simple-math.ts          # 基础 MCP 示例 ← 良好的起点
│   ├── github-handler.ts       # OAuth 实现 ← 使用此模式
│   ├── database.ts             # 数据库工具 ← 安全模式
│   ├── utils.ts                # OAuth 助手
│   ├── workers-oauth-utils.ts  # Cookie 安全系统
│   └── tools/                  # 工具注册系统
│       └── register-tools.ts   # 中央工具注册表 ← 理解此文件
├── PRPs/
│   ├── templates/prp_mcp_base.md  # 此模板
│   └── ai_docs/                   # 实现指南 ← 阅读全部
├── examples/                   # 示例工具实现
│   ├── database-tools.ts       # 数据库工具示例 ← 遵循模式
│   └── database-tools-sentry.ts # 带有 Sentry 监控
├── wrangler.jsonc              # Cloudflare 配置 ← 复制模式
├── package.json                # 依赖项
└── tsconfig.json               # TypeScript 配置
```

### 期望的代码库树结构（根据用户用例需要添加/修改的文件）

```bash

```

### 已知陷阱和关键 MCP/Cloudflare 模式

```typescript
// 关键：Cloudflare Workers 需要特定模式
// 1. 始终为 Durable Objects 实现清理
export class YourMCP extends McpAgent<Env, Record<string, never>, Props> {
  async cleanup(): Promise<void> {
    await closeDb(); // 关键：关闭数据库连接
  }

  async alarm(): Promise<void> {
    await this.cleanup(); // 关键：处理 Durable Object 告警
  }
}

// 2. 始终验证 SQL 以防止注入（使用现有模式）
const validation = validateSqlQuery(sql); // 来自 src/database.ts
if (!validation.isValid) {
  return createErrorResponse(validation.error);
}

// 3. 在敏感操作前始终检查权限
const ALLOWED_USERNAMES = new Set(["admin1", "admin2"]);
if (!ALLOWED_USERNAMES.has(this.props.login)) {
  return createErrorResponse("权限不足");
}

// 4. 始终使用 withDatabase 包装器进行连接管理
return await withDatabase(this.env.DATABASE_URL, async (db) => {
  // 数据库操作在此处
});

// 5. 始终使用 Zod 进行输入验证
import { z } from "zod";
const schema = z.object({
  param: z.string().min(1).max(100),
});

// 6. TypeScript 编译需要精确的接口匹配
interface Env {
  DATABASE_URL: string;
  GITHUB_CLIENT_ID: string;
  GITHUB_CLIENT_SECRET: string;
  OAUTH_KV: KVNamespace;
  // 在此处添加您的环境变量
}
```

## 实现蓝图

### 数据模型和类型

定义 TypeScript 接口和 Zod 模式以确保类型安全和验证。

```typescript
// 用户认证属性（从 OAuth 继承）
type Props = {
  login: string; // GitHub 用户名
  name: string; // 显示名称
  email: string; // 电子邮件地址
  accessToken: string; // GitHub 访问令牌
};

// MCP 工具输入模式（为您的工具自定义）
const YourToolSchema = z.object({
  param1: z.string().min(1, "参数不能为空"),
  param2: z.number().int().positive().optional(),
  options: z.object({}).optional(),
});

// 环境接口（添加您的变量）
interface Env {
  DATABASE_URL: string;
  GITHUB_CLIENT_ID: string;
  GITHUB_CLIENT_SECRET: string;
  OAUTH_KV: KVNamespace;
  // YOUR_SPECIFIC_ENV_VAR: string;
}

// 权限级别（为您的用例自定义）
enum Permission {
  READ = "read",
  WRITE = "write",
  ADMIN = "admin",
}
```

### 核心 MCP 代理类

通过扩展基础 McpAgent 类来实现您的 MCP 服务器。

```typescript
export class YourMCP extends McpAgent<Env, Record<string, never>, Props> {
  // 初始化您的 MCP 服务器
  async initialize(): Promise<void> {
    // 在此处注册您的工具
    this.registerTool("your_tool", {
      description: "描述您的工具功能",
      inputSchema: YourToolSchema,
      handler: this.handleYourTool.bind(this),
    });

    // 根据需要添加更多工具
    this.registerTool("another_tool", {
      description: "另一个工具描述",
      inputSchema: AnotherToolSchema,
      handler: this.handleAnotherTool.bind(this),
    });
  }

  // 工具处理器实现
  private async handleYourTool(
    args: z.infer<typeof YourToolSchema>
  ): Promise<ToolResponse> {
    try {
      // 验证权限
      if (!this.hasPermission(Permission.READ)) {
        return createErrorResponse("权限不足");
      }

      // 您的工具逻辑在此处
      const result = await this.performYourOperation(args);
      
      return createSuccessResponse(result);
    } catch (error) {
      return createErrorResponse(`工具执行失败: ${error.message}`);
    }
  }

  // 权限检查助手
  private hasPermission(required: Permission): boolean {
    // 实现您的权限逻辑
    const userPermissions = this.getUserPermissions(this.props.login);
    return userPermissions.includes(required);
  }

  // 清理资源（对 Cloudflare 至关重要）
  async cleanup(): Promise<void> {
    await closeDb();
    // 添加其他清理逻辑
  }

  // 处理 Durable Object 告警
  async alarm(): Promise<void> {
    await this.cleanup();
  }
}
```

### 任务列表（按顺序完成）

```yaml
任务 1 - 项目设置:
  复制 wrangler.jsonc 到 wrangler-[server-name].jsonc:
    - 修改 name 字段为 "[server-name]"
    - 在 vars 部分添加任何新的环境变量
    - 保留现有的 OAuth 和数据库配置

  创建 .dev.vars 文件（如果不存在）:
    - 添加 GITHUB_CLIENT_ID=your_client_id
    - 添加 GITHUB_CLIENT_SECRET=your_client_secret
    - 添加 DATABASE_URL=postgresql://...
    - 添加 COOKIE_ENCRYPTION_KEY=your_32_byte_key
    - 添加任何特定领域的环境变量

任务 2 - GitHub OAuth 应用:
  创建新的 GitHub OAuth 应用:
    - 设置主页 URL: https://your-worker.workers.dev
    - 设置回调 URL: https://your-worker.workers.dev/callback
    - 复制客户端 ID 和密钥到 .dev.vars

  或重用现有的 OAuth 应用:
    - 如果使用不同的子域名，更新回调 URL
    - 验证环境中的客户端 ID 和密钥

任务 3 - MCP 服务器实现:
  创建 src/[server-name].ts 或修改 src/index.ts:
    - 从 src/index.ts 复制类结构
    - 在 McpServer 构造函数中修改服务器名称和版本
    - 在 init() 方法中调用 registerAllTools(server, env, props)
    - 保持认证和数据库模式相同

  创建工具模块:
    - 按照 examples/database-tools.ts 模式创建新的工具文件
    - 导出接受 (server, env, props) 的注册函数
    - 使用 Zod 模式进行输入验证
    - 使用 createErrorResponse 实现适当的错误处理
    - 在工具注册期间添加权限检查

  更新工具注册表:
    - 修改 src/tools/register-tools.ts 以导入您的新工具
    - 在 registerAllTools() 中添加您的注册函数调用

任务 4 - 数据库集成（如果需要）:
  使用 src/database.ts 中的现有数据库模式:
    - 导入 withDatabase、validateSqlQuery、isWriteOperation
    - 使用安全验证实现数据库操作
    - 基于用户权限分离读写操作
    - 使用 formatDatabaseError 提供用户友好的错误消息

任务 5 - 环境配置:
  设置 Cloudflare KV 命名空间:
    - 运行: wrangler kv namespace create "OAUTH_KV"
    - 使用返回的命名空间 ID 更新 wrangler.jsonc

  设置生产密钥:
    - 运行: wrangler secret put GITHUB_CLIENT_ID
    - 运行: wrangler secret put GITHUB_CLIENT_SECRET
    - 运行: wrangler secret put DATABASE_URL
    - 运行: wrangler secret put COOKIE_ENCRYPTION_KEY

任务 6 - 本地测试:
  测试基本功能:
    - 运行: wrangler dev
    - 验证服务器启动无错误
    - 测试 OAuth 流程: http://localhost:8792/authorize
    - 验证 MCP 端点: http://localhost:8792/mcp

任务 7 - 生产部署:
  部署到 Cloudflare Workers:
    - 运行: wrangler deploy
    - 验证部署成功
    - 测试生产 OAuth 流程
    - 验证 MCP 端点可访问性
```

### Per Task Implementation Details

```typescript
// Task 3 - MCP Server Implementation Pattern
export class YourMCP extends McpAgent<Env, Record<string, never>, Props> {
  server = new McpServer({
    name: "Your MCP Server Name",
    version: "1.0.0",
  });

  // CRITICAL: Always implement cleanup
  async cleanup(): Promise<void> {
    try {
      await closeDb();
      console.log("Database connections closed successfully");
    } catch (error) {
      console.error("Error during database cleanup:", error);
    }
  }

  async alarm(): Promise<void> {
    await this.cleanup();
  }

  async init() {
    // PATTERN: Use centralized tool registration
    registerAllTools(this.server, this.env, this.props);
  }
}

// Task 3 - Tool Module Pattern (e.g., src/tools/your-feature-tools.ts)
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { Props } from "../types";
import { z } from "zod";

const PRIVILEGED_USERS = new Set(["admin1", "admin2"]);

export function registerYourFeatureTools(server: McpServer, env: Env, props: Props) {
  // Tool 1: Available to all authenticated users
  server.tool(
    "yourBasicTool",
    "Description of your basic tool",
    YourToolSchema, // Zod validation schema
    async ({ param1, param2, options }) => {
      try {
        // PATTERN: Tool implementation with error handling
        const result = await performOperation(param1, param2, options);

        return {
          content: [
            {
              type: "text",
              text: `**Success**\n\nOperation completed\n\n**Result:**\n\`\`\`json\n${JSON.stringify(result, null, 2)}\n\`\`\``,
            },
          ],
        };
      } catch (error) {
        return createErrorResponse(`Operation failed: ${error.message}`);
      }
    },
  );

  // Tool 2: Only for privileged users
  if (PRIVILEGED_USERS.has(props.login)) {
    server.tool(
      "privilegedTool",
      "Administrative tool for privileged users",
      { action: z.string() },
      async ({ action }) => {
        // Implementation
        return {
          content: [
            {
              type: "text",
              text: `Admin action '${action}' executed by ${props.login}`,
            },
          ],
        };
      },
    );
  }
}

// Task 3 - Update Tool Registry (src/tools/register-tools.ts)
import { registerYourFeatureTools } from "./your-feature-tools";

export function registerAllTools(server: McpServer, env: Env, props: Props) {
  // Existing registrations
  registerDatabaseTools(server, env, props);
  
  // Add your new registration
  registerYourFeatureTools(server, env, props);
}

// PATTERN: Export OAuth provider with MCP endpoints
export default new OAuthProvider({
  apiHandlers: {
    "/sse": YourMCP.serveSSE("/sse") as any,
    "/mcp": YourMCP.serve("/mcp") as any,
  },
  authorizeEndpoint: "/authorize",
  clientRegistrationEndpoint: "/register",
  defaultHandler: GitHubHandler as any,
  tokenEndpoint: "/token",
});
```

### Integration Points

```yaml
CLOUDFLARE_WORKERS:
  - wrangler.jsonc: Update name, environment variables, KV bindings
  - Environment secrets: GitHub OAuth credentials, database URL, encryption key
  - Durable Objects: Configure MCP agent binding for state persistence

GITHUB_OAUTH:
  - GitHub App: Create with callback URL matching your Workers domain
  - Client credentials: Store as Cloudflare Workers secrets
  - Callback URL: Must match exactly: https://your-worker.workers.dev/callback

DATABASE:
  - PostgreSQL connection: Use existing connection pooling patterns
  - Environment variable: DATABASE_URL with full connection string
  - Security: Use validateSqlQuery and isWriteOperation for all SQL

ENVIRONMENT_VARIABLES:
  - Development: .dev.vars file for local testing
  - Production: Cloudflare Workers secrets for deployment
  - Required: GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET, DATABASE_URL, COOKIE_ENCRYPTION_KEY

KV_STORAGE:
  - OAuth state: Used by OAuth provider for state management
  - Namespace: Create with `wrangler kv namespace create "OAUTH_KV"`
  - Configuration: Add namespace ID to wrangler.jsonc bindings
```

## Validation Gate

### Level 1: TypeScript & Configuration

```bash
# CRITICAL: Run these FIRST - fix any errors before proceeding
npm run type-check                 # TypeScript compilation
wrangler types                     # Generate Cloudflare Workers types

# Expected: No TypeScript errors
# If errors: Fix type issues, missing interfaces, import problems
```

### Level 2: Local Development Testing

```bash
# Start local development server
wrangler dev

# Test OAuth flow (should redirect to GitHub)
curl -v http://localhost:8792/authorize

# Test MCP endpoint (should return server info)
curl -v http://localhost:8792/mcp

# Expected: Server starts, OAuth redirects to GitHub, MCP responds with server info
# If errors: Check console output, verify environment variables, fix configuration
```

### Level 3: Unit test each feature, function, and file, following existing testing patterns if they are there.

```bash
npm run test
```

Run unit tests with the above command (Vitest) to make sure all functionality is working.

### Level 4: Database Integration Testing (if applicable)

```bash
# Test database connection
curl -X POST http://localhost:8792/mcp \
  -H "Content-Type: application/json" \
  -d '{"method": "tools/call", "params": {"name": "listTables", "arguments": {}}}'

# Test permission validation
# Test SQL injection protection and other kinds of security if applicable
# Test error handling for database failures

# Expected: Database operations work, permissions enforced, errors handled gracefully, etc.
# If errors: Check DATABASE_URL, connection settings, permission logic
```

## Final Validation Checklist

### Core Functionality

- [ ] TypeScript compilation: `npm run type-check` passes
- [ ] Unit tests pass: `npm run test` passes
- [ ] Local server starts: `wrangler dev` runs without errors
- [ ] MCP endpoint responds: `curl http://localhost:8792/mcp` returns server info
- [ ] OAuth flow works: Authentication redirects and completes successfully

---

## Anti-Patterns to Avoid

### MCP-Specific

- ❌ Don't skip input validation with Zod - always validate tool parameters
- ❌ Don't forget to implement cleanup() method for Durable Objects
- ❌ Don't hardcode user permissions - use configurable permission systems

### Development Process

- ❌ Don't skip the validation loops - each level catches different issues
- ❌ Don't guess about OAuth configuration - test the full flow
- ❌ Don't deploy without monitoring - implement logging and error tracking
- ❌ Don't ignore TypeScript errors - fix all type issues before deployment
