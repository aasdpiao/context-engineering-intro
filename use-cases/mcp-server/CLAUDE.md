# 带有 GitHub OAuth 的 MCP 服务器 - 实现指南

本指南提供了使用 Node.js、TypeScript 和 Cloudflare Workers 构建带有 GitHub OAuth 身份验证的 MCP（模型上下文协议）服务器的实现模式和标准。关于构建什么，请参阅 PRP（产品需求提示）文档。

## 核心原则

**重要：您必须在所有代码更改和 PRP 生成中遵循这些原则：**

### KISS（保持简单，愚蠢）

- 简单性应该是设计的关键目标
- 尽可能选择直接的解决方案而不是复杂的
- 简单的解决方案更容易理解、维护和调试

### YAGNI（你不会需要它）

- 避免基于推测构建功能
- 只在需要时实现功能，而不是在您预期它们在未来可能有用时

### 开闭原则

- 软件实体应该对扩展开放，对修改封闭
- 设计系统以便可以在对现有代码进行最少更改的情况下添加新功能

## 包管理和工具

**重要：此项目使用 npm 进行 Node.js 包管理，使用 Wrangler CLI 进行 Cloudflare Workers 开发。**

### 基本 npm 命令

```bash
# 从 package.json 安装依赖
npm install

# 添加依赖
npm install package-name

# 添加开发依赖
npm install --save-dev package-name

# 移除包
npm uninstall package-name

# 更新依赖
npm update

# 运行 package.json 中定义的脚本
npm run dev
npm run deploy
npm run type-check
```

### 基本 Wrangler CLI 命令

**重要：使用 Wrangler CLI 进行所有 Cloudflare Workers 开发、测试和部署。**

```bash
# 身份验证
wrangler login          # 登录到 Cloudflare 账户
wrangler logout         # 从 Cloudflare 注销
wrangler whoami         # 检查当前用户

# 开发和测试
wrangler dev           # 启动本地开发服务器（默认端口 8787）

# 部署
wrangler deploy        # 将 Worker 部署到 Cloudflare
wrangler deploy --dry-run  # 测试部署而不实际部署

# 配置和类型
wrangler types         # 从 Worker 配置生成 TypeScript 类型
```

## 项目架构

**重要：这是一个带有 GitHub OAuth 身份验证的 Cloudflare Workers MCP 服务器，用于安全的数据库访问。**

### 当前项目结构

```
/
├── src/                          # TypeScript 源代码
│   ├── index.ts                  # 主要 MCP 服务器（标准版）
│   ├── index_sentry.ts          # 启用 Sentry 的 MCP 服务器
│   ├── simple-math.ts           # 基本 MCP 示例（无身份验证）
│   ├── github-handler.ts        # GitHub OAuth 流程实现
│   ├── database.ts              # PostgreSQL 连接和工具
│   ├── utils.ts                 # OAuth 辅助函数
│   ├── workers-oauth-utils.ts   # 基于 Cookie 的批准系统
│   └── tools/                   # 工具注册系统
│       └── register-tools.ts    # 集中式工具注册
├── PRPs/                        # 产品需求提示
│   ├── README.md
│   └── templates/
│       └── prp_mcp_base.md
├── examples/                    # 示例工具创建和注册 - 永远不要编辑或从此文件夹导入
│   ├── database-tools.ts        # Postgres MCP 服务器的示例工具，展示工具创建和注册的最佳实践
│   └── database-tools-sentry.ts # Postgres MCP 服务器的示例工具，但集成了 Sentry 用于生产监控
├── wrangler.jsonc              # 主要 Cloudflare Workers 配置
├── wrangler-simple.jsonc       # 简单数学示例配置
├── package.json                # npm 依赖和脚本
├── tsconfig.json               # TypeScript 配置
├── worker-configuration.d.ts   # 生成的 Cloudflare 类型
└── CLAUDE.md                   # 此实现指南
```

### 关键文件用途（始终在此处添加新文件）

**主要实现文件：**

- `src/index.ts` - 带有 GitHub OAuth + PostgreSQL 的生产 MCP 服务器
- `src/index_sentry.ts` - 与上述相同，但集成了 Sentry 监控

**身份验证和安全：**

- `src/github-handler.ts` - 完整的 GitHub OAuth 2.0 流程
- `src/workers-oauth-utils.ts` - HMAC 签名的 cookie 批准系统
- `src/utils.ts` - OAuth 令牌交换和 URL 构建辅助工具

**数据库集成：**

- `src/database.ts` - PostgreSQL 连接池、SQL 验证、安全性

**工具注册：**

- `src/tools/register-tools.ts` - 集中式工具注册系统，导入并注册所有工具

**配置文件：**

- `wrangler.jsonc` - 主要 Worker 配置，包含 Durable Objects、KV、AI 绑定
- `wrangler-simple.jsonc` - 简单示例配置
- `tsconfig.json` - Cloudflare Workers 的 TypeScript 编译器设置

## 开发命令

### 核心工作流程命令

```bash
# 设置和依赖
npm install                  # 安装所有依赖
npm install --save-dev @types/package  # 添加带类型的开发依赖

# 开发
wrangler dev                # 启动本地开发服务器
npm run dev                 # 通过 npm 脚本的替代方式

# 类型检查和验证
npm run type-check          # 运行 TypeScript 编译器检查
wrangler types              # 生成 Cloudflare Worker 类型
npx tsc --noEmit           # 不编译的类型检查

# 测试
npx vitest                  # 运行单元测试（如果已配置）

# 代码质量
npx prettier --write .      # 格式化代码
npx eslint src/            # 检查 TypeScript 代码
```

### Environment Configuration

**Environment Variables Setup:**

```bash
# Create .dev.vars file for local development based on .dev.vars.example
cp .dev.vars.example .dev.vars

# Production secrets (via Wrangler)
wrangler secret put GITHUB_CLIENT_ID
wrangler secret put GITHUB_CLIENT_SECRET
wrangler secret put COOKIE_ENCRYPTION_KEY
wrangler secret put DATABASE_URL
wrangler secret put SENTRY_DSN
```

## MCP 开发上下文

**重要：此项目使用 Node.js/TypeScript 在 Cloudflare Workers 上构建带有 GitHub OAuth 身份验证的生产就绪 MCP 服务器。**

### MCP 技术栈

**核心技术：**

- **@modelcontextprotocol/sdk** - 官方 MCP TypeScript SDK
- **agents/mcp** - Cloudflare Workers MCP 代理框架
- **workers-mcp** - Workers 的 MCP 传输层
- **@cloudflare/workers-oauth-provider** - OAuth 2.1 服务器实现

**Cloudflare 平台：**

- **Cloudflare Workers** - 无服务器运行时（V8 隔离）
- **Durable Objects** - 用于 MCP 代理持久化的有状态对象
- **KV Storage** - OAuth 状态和会话管理

### MCP 服务器架构

此项目将 MCP 服务器实现为具有三种主要模式的 Cloudflare Workers：

**1. 认证数据库 MCP 服务器 (`src/index.ts`)：**

```typescript
export class MyMCP extends McpAgent<Env, Record<string, never>, Props> {
  server = new McpServer({
    name: "PostgreSQL Database MCP Server",
    version: "1.0.0",
  });

  // 基于用户权限的 MCP 工具
  // - listTables（所有用户）
  // - queryDatabase（所有用户，只读）
  // - executeDatabase（仅特权用户）
}
```

**2. 监控 MCP 服务器 (`src/index_sentry.ts`)：**

- 与上述功能相同，但带有 Sentry 监控
- MCP 工具调用的分布式跟踪
- 带事件 ID 的错误跟踪
- 性能监控

### MCP 开发命令

**本地开发和测试：**

```bash
# 启动主要 MCP 服务器（带 OAuth）
wrangler dev                    # 可在 http://localhost:8792/mcp 访问

# 使用 Inspector 测试 MCP 服务器
npx @modelcontextprotocol/inspector@latest

# 在 Inspector 中连接到本地服务器：
# 传输：HTTP
# URL：http://localhost:8792/mcp
```

### Claude Desktop 集成

**本地开发：**

```json
{
  "mcpServers": {
    "database-mcp": {
      "command": "npx",
      "args": ["mcp-remote", "http://localhost:8792/mcp"],
      "env": {}
    }
  }
}
```

**生产部署：**

```json
{
  "mcpServers": {
    "database-mcp": {
      "command": "npx",
      "args": ["mcp-remote", "https://your-worker.workers.dev/mcp"],
      "env": {}
    }
  }
}
```

### 此项目的 MCP 关键概念

- **工具**：数据库操作（listTables、queryDatabase、executeDatabase）
- **身份验证**：带有基于角色访问控制的 GitHub OAuth
- **传输**：对 HTTP（`/mcp`）和 SSE（`/sse`）协议的双重支持
- **状态**：Durable Objects 维护已认证的用户上下文
- **安全性**：SQL 注入保护、权限验证、错误清理

## 数据库集成和安全

**重要：此项目通过带有基于角色权限的 MCP 工具提供安全的 PostgreSQL 数据库访问。**

### 数据库架构

**连接管理 (`src/database.ts`)：**

```typescript
// 带有 Cloudflare Workers 限制的单例连接池
export function getDb(databaseUrl: string): postgres.Sql {
  if (!dbInstance) {
    dbInstance = postgres(databaseUrl, {
      max: 5, // Workers 最大 5 个连接
      idle_timeout: 20,
      connect_timeout: 10,
      prepare: true, // 启用预处理语句
    });
  }
  return dbInstance;
}

// 带错误处理的连接包装器
export async function withDatabase<T>(databaseUrl: string, operation: (db: postgres.Sql) => Promise<T>): Promise<T> {
  const db = getDb(databaseUrl);
  // 执行带计时和错误处理的操作
}
```

### 安全实现

**SQL 注入保护：**

```typescript
export function validateSqlQuery(sql: string): { isValid: boolean; error?: string } {
  const dangerousPatterns = [
    /;\s*drop\s+/i,
    /;\s*delete\s+.*\s+where\s+1\s*=\s*1/i,
    /;\s*truncate\s+/i,
    // ... 更多模式
  ];
  // 基于模式的安全验证
}

export function isWriteOperation(sql: string): boolean {
  const writeKeywords = ["insert", "update", "delete", "create", "drop", "alter"];
  return writeKeywords.some((keyword) => sql.trim().toLowerCase().startsWith(keyword));
}
```

**访问控制 (`src/index.ts`)：**

```typescript
const ALLOWED_USERNAMES = new Set<string>([
  'coleam00'  // 只有这些 GitHub 用户名可以执行写操作
]);

// 基于用户权限的工具可用性
if (ALLOWED_USERNAMES.has(this.props.login)) {
  // 为特权用户注册 executeDatabase 工具
  this.server.tool("executeDatabase", ...);
}
```

### MCP 工具实现

**工具注册系统：**

工具现在以模块化方式组织，采用集中式注册：

1. **工具注册 (`src/tools/register-tools.ts`)：**
   - 导入所有工具模块的中央注册表
   - 调用各个注册函数
   - 将服务器、环境和用户属性传递给每个模块

2. **工具实现模式：**
   - 每个功能/域都有自己的工具文件（例如，`database-tools.ts`）
   - 工具作为注册函数导出
   - 注册函数接收服务器实例、环境和用户属性
   - 权限检查在注册期间进行

**示例工具注册：**

```typescript
// src/tools/register-tools.ts
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { Props } from "../types";
import { registerDatabaseTools } from "../../examples/database-tools";

export function registerAllTools(server: McpServer, env: Env, props: Props) {
  // 注册数据库工具
  registerDatabaseTools(server, env, props);
  
  // 未来的工具可以在此处注册
  // registerAnalyticsTools(server, env, props);
  // registerReportingTools(server, env, props);
}
```

**示例工具模块 (`examples/database-tools.ts`)：**

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { Props } from "../types";

const ALLOWED_USERNAMES = new Set<string>(['coleam00']);

export function registerDatabaseTools(server: McpServer, env: Env, props: Props) {
  // 工具 1：所有认证用户可用
  server.tool(
    "listTables",
    "获取数据库中所有表的列表",
    ListTablesSchema,
    async () => {
      // 实现
    }
  );

  // 工具 2：所有认证用户可用
  server.tool(
    "queryDatabase",
    "执行只读 SQL 查询",
    QueryDatabaseSchema,
    async ({ sql }) => {
      // 带验证的实现
    }
  );

  // 工具 3：仅特权用户
  if (ALLOWED_USERNAMES.has(props.login)) {
    server.tool(
      "executeDatabase",
      "执行任何 SQL 语句（特权）",
      ExecuteDatabaseSchema,
      async ({ sql }) => {
        // 实现
      }
    );
  }
}
```

**示例中可用的数据库工具：**

1. **`listTables`** - 模式发现（所有认证用户）
2. **`queryDatabase`** - 只读 SQL 查询（所有认证用户）
3. **`executeDatabase`** - 写操作（仅特权用户）

## GitHub OAuth 实现

**重要：此项目实现了带有签名 cookie 批准系统的安全 GitHub OAuth 2.0 流程。**

### OAuth 流程架构

**认证流程 (`src/github-handler.ts`)：**

```typescript
// 1. 授权请求
app.get("/authorize", async (c) => {
  const oauthReqInfo = await c.env.OAUTH_PROVIDER.parseAuthRequest(c.req.raw);

  // 通过签名 cookie 检查客户端是否已批准
  if (await clientIdAlreadyApproved(c.req.raw, oauthReqInfo.clientId, c.env.COOKIE_ENCRYPTION_KEY)) {
    return redirectToGithub(c.req.raw, oauthReqInfo, c.env, {});
  }

  // 显示批准对话框
  return renderApprovalDialog(c.req.raw, { client, server, state });
});

// 2. GitHub 回调
app.get("/callback", async (c) => {
  // 将代码交换为访问令牌
  const [accessToken, errResponse] = await fetchUpstreamAuthToken({
    client_id: c.env.GITHUB_CLIENT_ID,
    client_secret: c.env.GITHUB_CLIENT_SECRET,
    code: c.req.query("code"),
    redirect_uri: new URL("/callback", c.req.url).href,
  });

  // 获取 GitHub 用户信息
  const user = await new Octokit({ auth: accessToken }).rest.users.getAuthenticated();

  // 使用用户属性完成授权
  return c.env.OAUTH_PROVIDER.completeAuthorization({
    props: { accessToken, email, login, name } as Props,
    userId: login,
  });
});
```

### Cookie 安全系统

**HMAC 签名批准 Cookies (`src/workers-oauth-utils.ts`)：**

```typescript
// 为客户端批准生成签名 cookie
async function signData(key: CryptoKey, data: string): Promise<string> {
  const signatureBuffer = await crypto.subtle.sign("HMAC", key, enc.encode(data));
  return Array.from(new Uint8Array(signatureBuffer))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}

// 验证 cookie 完整性
async function verifySignature(key: CryptoKey, signatureHex: string, data: string): Promise<boolean> {
  const signatureBytes = new Uint8Array(signatureHex.match(/.{1,2}/g)!.map((byte) => parseInt(byte, 16)));
  return await crypto.subtle.verify("HMAC", key, signatureBytes.buffer, enc.encode(data));
}
```

### 用户上下文和权限

**认证用户属性：**

```typescript
type Props = {
  login: string; // GitHub 用户名
  name: string; // 显示名称
  email: string; // 电子邮件地址
  accessToken: string; // GitHub 访问令牌
};

// 在 MCP 工具中通过 this.props 可用
class MyMCP extends McpAgent<Env, Record<string, never>, Props> {
  async init() {
    // 在任何工具中访问用户上下文
    const username = this.props.login;
    const hasWriteAccess = ALLOWED_USERNAMES.has(username);
  }
}
```

## 监控与可观测性

**重要：此项目支持可选的 Sentry 集成用于生产监控，并包含内置的控制台日志。**

### 日志架构

**两种部署选项：**

1. **标准版本 (`src/index.ts`)**：仅控制台日志
2. **Sentry 版本 (`src/index_sentry.ts`)**：完整的 Sentry 监控

### Sentry 集成（可选）

**启用 Sentry 监控：**

```typescript
// src/index_sentry.ts - 带监控的生产就绪版本
import * as Sentry from "@sentry/cloudflare";

// Sentry 配置
function getSentryConfig(env: Env) {
  return {
    dsn: env.SENTRY_DSN,
    tracesSampleRate: 1,  // 100% 跟踪采样
  };
}

// 使用跟踪监控 MCP 工具
private registerTool(name: string, description: string, schema: any, handler: any) {
  this.server.tool(name, description, schema, async (args: any) => {
    return await Sentry.startNewTrace(async () => {
      return await Sentry.startSpan({
        name: `mcp.tool/${name}`,
        attributes: extractMcpParameters(args),
      }, async (span) => {
        // 设置用户上下文
        Sentry.setUser({
          username: this.props.login,
          email: this.props.email,
        });

        try {
          return await handler(args);
        } catch (error) {
          span.setStatus({ code: 2 }); // 错误
          return handleError(error);  // 返回带事件 ID 的用户友好错误
        }
      });
    });
  });
}
```

**启用的 Sentry 功能：**

- **错误跟踪**：带上下文的自动异常捕获
- **性能监控**：100% 采样率的完整请求跟踪
- **用户上下文**：GitHub 用户信息绑定到事件
- **工具跟踪**：每个 MCP 工具调用都带参数跟踪
- **分布式跟踪**：跨 Cloudflare Workers 的请求流

### 生产日志模式

**控制台日志（标准）：**

```typescript
// 数据库操作
console.log(`数据库操作在 ${duration}ms 内成功完成`);
console.error(`数据库操作在 ${duration}ms 后失败:`, error);

// 身份验证事件
console.log(`用户已认证: ${this.props.login} (${this.props.name})`);

// 工具执行
console.log(`工具调用: ${toolName} 由 ${this.props.login} 调用`);
console.error(`工具失败: ${toolName}`, error);
```

**结构化错误处理：**

```typescript
// 安全的错误清理
export function formatDatabaseError(error: unknown): string {
  if (error instanceof Error) {
    if (error.message.includes("password")) {
      return "数据库身份验证失败。请检查凭据。";
    }
    if (error.message.includes("timeout")) {
      return "数据库连接超时。请重试。";
    }
    return `数据库错误: ${error.message}`;
  }
  return "发生未知数据库错误。";
}
```

### 监控配置

**开发监控：**

```bash
# 在开发中启用 Sentry
echo 'SENTRY_DSN=https://your-dsn@sentry.io/project' >> .dev.vars
echo 'NODE_ENV=development' >> .dev.vars

# 使用启用 Sentry 的版本
wrangler dev --config wrangler.jsonc  # 确保 main = "src/index_sentry.ts"
```

**生产监控：**

```bash
# 设置生产密钥
wrangler secret put SENTRY_DSN
wrangler secret put NODE_ENV  # 设置为 "production"

# 带监控部署
wrangler deploy
```

## TypeScript 开发标准

**重要：所有 MCP 工具必须遵循 TypeScript 最佳实践，包含 Zod 验证和适当的错误处理。**

### 标准响应格式

**所有工具必须返回 MCP 兼容的响应对象：**

```typescript
import { z } from "zod";

// 遵循适当 TypeScript 模式的工具
this.server.tool(
  "standardizedTool",
  "遵循标准响应格式的工具",
  {
    name: z.string().min(1, "名称不能为空"),
    options: z.object({}).optional(),
  },
  async ({ name, options }) => {
    try {
      // 输入已通过 Zod 模式验证
      const result = await processName(name, options);

      // 返回标准化成功响应
      return {
        content: [
          {
            type: "text",
            text: `**成功**\n\n已处理: ${name}\n\n**结果:**\n\`\`\`json\n${JSON.stringify(result, null, 2)}\n\`\`\`\n\n**处理时间:** 0.5s`,
          },
        ],
      };
    } catch (error) {
      // 返回标准化错误响应
      return {
        content: [
          {
            type: "text",
            text: `**错误**\n\n处理失败: ${error instanceof Error ? error.message : String(error)}`,
            isError: true,
          },
        ],
      };
    }
  },
);
```

### 使用 Zod 进行输入验证

**所有工具输入必须使用 Zod 模式进行验证：**

```typescript
import { z } from "zod";

// 定义验证模式
const DatabaseQuerySchema = z.object({
  sql: z
    .string()
    .min(1, "SQL 查询不能为空")
    .refine((sql) => sql.trim().toLowerCase().startsWith("select"), {
      message: "只允许 SELECT 查询",
    }),
  limit: z.number().int().positive().max(1000).optional(),
});

// 在工具定义中使用
this.server.tool(
  "queryDatabase",
  "执行只读 SQL 查询",
  DatabaseQuerySchema, // Zod 模式提供自动验证
  async ({ sql, limit }) => {
    // sql 和 limit 已经验证并正确类型化
    const results = await db.unsafe(sql);
    return { content: [{ type: "text", text: JSON.stringify(results, null, 2) }] };
  },
);
```

### 错误处理模式

**标准化错误响应：**

```typescript
// 错误处理工具
function createErrorResponse(message: string, details?: any): any {
  return {
    content: [{
      type: "text",
      text: `**错误**\n\n${message}${details ? `\n\n**详情:**\n\`\`\`json\n${JSON.stringify(details, null, 2)}\n\`\`\`` : ''}`,
      isError: true
    }]
  };
}

// 权限错误
if (!ALLOWED_USERNAMES.has(this.props.login)) {
  return createErrorResponse(
    "此操作权限不足",
    { requiredRole: "特权", userRole: "标准" }
  );
}

// 验证错误
if (isWriteOperation(sql)) {
  return createErrorResponse(
    "此工具不允许写操作",
    { operation: "写入", allowedOperations: ["select", "show", "describe"] }
  );
}

// 数据库错误
catch (error) {
  return createErrorResponse(
    "数据库操作失败",
    { error: formatDatabaseError(error) }
  );
}
```

### 类型安全规则

**强制性 TypeScript 模式：**

1. **严格类型**：所有参数和返回类型明确类型化
2. **Zod 验证**：所有输入使用 Zod 模式验证
3. **错误处理**：所有异步操作包装在 try/catch 中
4. **用户上下文**：Props 使用 GitHub 用户信息类型化
5. **环境**：使用 `wrangler types` 生成 Cloudflare Workers 类型

## 代码风格偏好

### TypeScript 风格

- 为所有函数参数和返回类型使用明确的类型注解
- 为所有导出的函数和类使用 JSDoc 注释
- 对所有异步操作优先使用 async/await
- **强制性**：对所有输入验证使用 Zod 模式
- **强制性**：使用 try/catch 块进行适当的错误处理
- 保持函数小而专注（单一职责原则）

### 文件组织

- 每个 MCP 服务器应该在单个 TypeScript 文件中自包含
- 导入语句组织：Node.js 内置模块、第三方包、本地导入
- 在 src/ 目录内使用相对导入
- **为所有模块导入 Zod 进行验证和适当的类型**

### 测试约定

- 使用 MCP Inspector 进行集成测试：`npx @modelcontextprotocol/inspector@latest`
- 使用本地开发服务器测试：`wrangler dev`
- 使用描述性的工具名称和描述
- **测试身份验证和权限场景**
- **使用无效数据测试输入验证**

## 重要注意事项

### 不要做的事情

- **永远不要** 将密钥或环境变量提交到仓库
- **永远不要** 在简单解决方案可行时构建复杂解决方案
- **永远不要** 跳过使用 Zod 模式的输入验证

### 要做的事情

- **始终** 使用 TypeScript 严格模式和适当的类型
- **始终** 使用 Zod 模式验证输入
- **始终** 遵循核心原则（KISS、YAGNI 等）
- **始终** 使用 Wrangler CLI 进行所有开发和部署

## Git 工作流

```bash
# 提交前，始终运行：
npm run type-check              # 确保 TypeScript 编译
wrangler dev --dry-run          # 测试部署配置

# 使用描述性消息提交
git add .
git commit -m "feat: 为数据库查询添加新的 MCP 工具"
```

## 快速参考

### 添加新的 MCP 工具

1. **在项目中创建新的工具模块**（遵循 `examples/` 中的模式）：
   ```typescript
   // src/tools/your-feature-tools.ts
   export function registerYourFeatureTools(server: McpServer, env: Env, props: Props) {
     // 在此处注册您的工具
   }
   ```

2. **在类型文件中定义 Zod 模式** 用于输入验证

3. **实现工具处理程序** 使用示例中的模式进行适当的错误处理

4. **在 `src/tools/register-tools.ts` 中注册您的工具**：
   ```typescript
   import { registerYourFeatureTools } from "./your-feature-tools";
   
   export function registerAllTools(server: McpServer, env: Env, props: Props) {
     // 现有注册
     registerDatabaseTools(server, env, props);
     
     // 添加您的新注册
     registerYourFeatureTools(server, env, props);
   }
   ```

5. **如需要，更新文档**
