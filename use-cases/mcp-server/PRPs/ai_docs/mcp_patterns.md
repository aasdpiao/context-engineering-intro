# MCP 服务器开发模式

本文档包含基于此代码库实现的使用 TypeScript 和 Cloudflare Workers 开发模型上下文协议（MCP）服务器的经过验证的模式。

## 核心 MCP 服务器架构

### 基础服务器类模式

```typescript
import { McpAgent } from "agents/mcp";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

// 来自 OAuth 流程的认证属性
type Props = {
  login: string;
  name: string;
  email: string;
  accessToken: string;
};

export class CustomMCP extends McpAgent<Env, Record<string, never>, Props> {
  server = new McpServer({
    name: "您的 MCP 服务器名称",
    version: "1.0.0",
  });

  // 关键：为 Durable Objects 实现清理
  async cleanup(): Promise<void> {
    try {
      // 关闭数据库连接
      await closeDb();
      console.log('数据库连接已成功关闭');
    } catch (error) {
      console.error('数据库清理过程中出错:', error);
    }
  }

  // 关键：Durable Objects 告警处理器
  async alarm(): Promise<void> {
    await this.cleanup();
  }

  // 初始化所有工具和资源
  async init() {
    // 在此处注册工具
    this.registerTools();
    
    // 如果需要，注册资源
    this.registerResources();
  }

  private registerTools() {
    // 工具注册逻辑
  }

  private registerResources() {
    // 资源注册逻辑
  }
}
```

### 工具注册模式

```typescript
// 基础工具注册
this.server.tool(
  "toolName",
  "为 LLM 提供的工具描述",
  {
    param1: z.string().describe("参数描述"),
    param2: z.number().optional().describe("可选参数"),
  },
  async ({ param1, param2 }) => {
    try {
      // 工具实现
      const result = await performOperation(param1, param2);
      
      return {
        content: [
          {
            type: "text",
            text: `成功: ${JSON.stringify(result, null, 2)}`
          }
        ]
      };
    } catch (error) {
      console.error('工具错误:', error);
      return {
        content: [
          {
            type: "text",
            text: `错误: ${error.message}`,
            isError: true
          }
        ]
      };
    }
  }
);
```

### 基于权限的条件工具注册

```typescript
// 基于权限的工具可用性
const ALLOWED_USERNAMES = new Set<string>([
  'admin1',
  'admin2'
]);

// 仅为授权用户注册特权工具
if (ALLOWED_USERNAMES.has(this.props.login)) {
  this.server.tool(
    "privilegedTool",
    "仅授权用户可用的工具",
    { /* 参数 */ },
    async (params) => {
      // 特权操作
      return {
        content: [
          {
            type: "text",
            text: `特权操作由以下用户执行: ${this.props.login}`
          }
        ]
      };
    }
  );
}

// 根据用户权限注册工具
private registerTools() {
  // 始终可用的工具
  this.registerReadOnlyTools();
  
  // 基于权限的条件工具
  if (hasPermission(this.props.login, 'write')) {
    this.registerWriteTools();
  }
  
  if (hasPermission(this.props.login, 'admin')) {
    this.registerAdminTools();
  }
}

private registerReadOnlyTools() {
  this.server.tool(
    "read_data",
    "从数据库读取数据",
    { /* 工具定义 */ },
    async (params) => {
      // 实现
    }
  );
}

private registerWriteTools() {
  this.server.tool(
    "write_data",
    "向数据库写入数据",
    { /* 工具定义 */ },
    async (params) => {
      // 在处理器中始终双重检查权限
      if (!hasPermission(this.props.login, 'write')) {
        return createErrorResponse(new Error("访问被拒绝"), "权限检查");
      }
      // 实现
    }
  );
}
```

## 数据库集成模式

### 数据库连接模式

```typescript
import { withDatabase, validateSqlQuery, isWriteOperation, formatDatabaseError } from "./database";

// 带连接管理的数据库操作
async function performDatabaseOperation(sql: string) {
  try {
    // 验证 SQL 查询
    const validation = validateSqlQuery(sql);
    if (!validation.isValid) {
      return {
        content: [
          {
            type: "text",
            text: `无效的 SQL 查询: ${validation.error}`,
            isError: true
          }
        ]
      };
    }

    // 使用自动连接管理执行
    return await withDatabase(this.env.DATABASE_URL, async (db) => {
      const results = await db.unsafe(sql);
      
      return {
        content: [
          {
            type: "text",
            text: `**查询结果**\n\`\`\`sql\n${sql}\n\`\`\`\n\n**结果:**\n\`\`\`json\n${JSON.stringify(results, null, 2)}\n\`\`\`\n\n**返回行数:** ${Array.isArray(results) ? results.length : 1}`
          }
        ]
      };
    });
  } catch (error) {
    console.error('数据库操作错误:', error);
    return {
      content: [
        {
          type: "text",
          text: `数据库错误: ${formatDatabaseError(error)}`,
          isError: true
        }
      ]
    };
  }
}
```

### 读写操作处理

```typescript
// 检查操作是否为只读
if (isWriteOperation(sql)) {
  return {
    content: [
      {
        type: "text",
        text: "此工具不允许写操作。如果您有写权限，请使用特权工具。",
        isError: true
      }
    ]
  };
}
```

## 身份验证和授权模式

### OAuth 集成模式

```typescript
import OAuthProvider from "@cloudflare/workers-oauth-provider";
import { GitHubHandler } from "./github-handler";

// OAuth 配置
export default new OAuthProvider({
  apiHandlers: {
    '/sse': MyMCP.serveSSE('/sse') as any,
    '/mcp': MyMCP.serve('/mcp') as any,
  },
  authorizeEndpoint: "/authorize",
  clientRegistrationEndpoint: "/register",
  defaultHandler: GitHubHandler as any,
  tokenEndpoint: "/token",
});
```

### 用户权限检查

```typescript
// 权限验证模式
function hasPermission(username: string, operation: string): boolean {
  const WRITE_PERMISSIONS = new Set(['admin1', 'admin2']);
  const READ_PERMISSIONS = new Set(['user1', 'user2', ...WRITE_PERMISSIONS]);
  
  switch (operation) {
    case 'read':
      return READ_PERMISSIONS.has(username);
    case 'write':
      return WRITE_PERMISSIONS.has(username);
    default:
      return false;
  }
}
```

## 错误处理模式

### 标准化错误响应

```typescript
// 错误响应模式
function createErrorResponse(error: Error, operation: string) {
  console.error(`${operation} 错误:`, error);
  
  return {
    content: [
      {
        type: "text",
        text: `${operation} 失败: ${error.message}`,
        isError: true
      }
    ]
  };
}
```

### 数据库错误格式化

```typescript
// 使用内置的数据库错误格式化器
import { formatDatabaseError } from "./database";

try {
  // 数据库操作
} catch (error) {
  return {
    content: [
      {
        type: "text",
        text: `数据库错误: ${formatDatabaseError(error)}`,
        isError: true
      }
    ]
  };
}
```

## 资源注册模式

### 基础资源模式

```typescript
// 资源注册
this.server.resource(
  "resource://example/{id}",
  "资源描述",
  async (uri) => {
    const id = uri.path.split('/').pop();
    
    try {
      const data = await fetchResourceData(id);
      
      return {
        contents: [
          {
            uri: uri.href,
            mimeType: "application/json",
            text: JSON.stringify(data, null, 2)
          }
        ]
      };
    } catch (error) {
      throw new Error(`获取资源失败: ${error.message}`);
    }
  }
);
```

## 测试模式

### 工具测试模式

```typescript
// 测试工具功能
async function testTool(toolName: string, params: any) {
  try {
    const result = await server.callTool(toolName, params);
    console.log(`${toolName} 测试通过:`, result);
    return true;
  } catch (error) {
    console.error(`${toolName} 测试失败:`, error);
    return false;
  }
}
```

### 数据库连接测试

```typescript
// 测试数据库连接
async function testDatabaseConnection() {
  try {
    await withDatabase(process.env.DATABASE_URL, async (db) => {
      const result = await db`SELECT 1 as test`;
      console.log('数据库连接测试通过:', result);
    });
    return true;
  } catch (error) {
    console.error('数据库连接测试失败:', error);
    return false;
  }
}
```

## 安全最佳实践

### 输入验证

```typescript
// 始终使用 Zod 验证输入
const inputSchema = z.object({
  query: z.string().min(1).max(1000),
  parameters: z.array(z.string()).optional()
});

// 在工具处理器中
try {
  const validated = inputSchema.parse(params);
  // 使用验证后的数据
} catch (error) {
  return createErrorResponse(error, "输入验证");
}
```

### SQL 注入防范

```typescript
// 使用内置的 SQL 验证
import { validateSqlQuery } from "./database";

const validation = validateSqlQuery(sql);
if (!validation.isValid) {
  return createErrorResponse(new Error(validation.error), "SQL 验证");
}
```

### 访问控制

```typescript
// 在执行敏感操作前始终检查权限
if (!hasPermission(this.props.login, 'write')) {
  return {
    content: [
      {
        type: "text",
        text: "访问被拒绝：权限不足",
        isError: true
      }
    ]
  };
}
```

## 性能模式

### 连接池

```typescript
// 使用内置的连接池
import { withDatabase } from "./database";

// withDatabase 函数自动处理连接池
await withDatabase(databaseUrl, async (db) => {
  // 数据库操作
});
```

### 资源清理

```typescript
// 在 Durable Objects 中实现适当的清理
async cleanup(): Promise<void> {
  try {
    // 关闭数据库连接
    await closeDb();
    
    // 清理其他资源
    await cleanupResources();
    
    console.log('清理成功完成');
  } catch (error) {
    console.error('清理错误:', error);
  }
}
```

## 常见陷阱

### 1. 缺少清理实现
- 始终在 Durable Objects 中实现 `cleanup()` 方法
- 正确处理数据库连接清理
- 设置告警处理器进行自动清理

### 2. SQL 注入漏洞
- 在执行 SQL 前始终使用 `validateSqlQuery()`
- 永远不要将用户输入直接连接到 SQL 字符串中
- 尽可能使用参数化查询

### 3. 权限绕过
- 为每个敏感操作检查权限
- 不要仅依赖工具注册来保证安全
- 始终从 props 验证用户身份

### 4. 错误信息泄露
- 使用 `formatDatabaseError()` 清理错误消息
- 不要在错误响应中暴露内部系统详情
- 在服务器端记录详细错误，向客户端返回通用消息

### 5. 资源泄露
- 始终使用 `withDatabase()` 进行数据库操作
- 在异步操作中实现适当的错误处理
- 在 finally 块中清理资源

## 环境配置

### 必需的环境变量

```typescript
// 环境类型定义
interface Env {
  DATABASE_URL: string;
  GITHUB_CLIENT_ID: string;
  GITHUB_CLIENT_SECRET: string;
  OAUTH_KV: KVNamespace;
  // 根据需要添加其他绑定
}
```

### Wrangler 配置模式

```toml
# wrangler.toml
name = "mcp-server"
main = "src/index.ts"
compatibility_date = "2024-01-01"

[[kv_namespaces]]
binding = "OAUTH_KV"
id = "your-kv-namespace-id"

[env.production]
# 生产环境特定配置
```

本文档提供了使用此代码库中经过验证的架构构建安全、可扩展的 MCP 服务器的核心模式。