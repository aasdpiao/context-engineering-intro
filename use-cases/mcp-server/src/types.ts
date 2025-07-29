import { z } from "zod";
import type { AuthRequest, OAuthHelpers, ClientInfo } from "@cloudflare/workers-oauth-provider";

// 通过 OAuth 传递的用户上下文
export type Props = {
  login: string;
  name: string;
  email: string;
  accessToken: string;
};

// 带有 OAuth 提供者的扩展环境
export type ExtendedEnv = Env & { OAUTH_PROVIDER: OAuthHelpers };

// OAuth URL 构建参数
export interface UpstreamAuthorizeParams {
  upstream_url: string;
  client_id: string;
  scope: string;
  redirect_uri: string;
  state?: string;
}

// OAuth 令牌交换参数
export interface UpstreamTokenParams {
  code: string | undefined;
  upstream_url: string;
  client_secret: string;
  redirect_uri: string;
  client_id: string;
}

// 批准对话框配置
export interface ApprovalDialogOptions {
  client: ClientInfo | null;
  server: {
    name: string;
    logo?: string;
    description?: string;
  };
  state: Record<string, any>;
  cookieName?: string;
  cookieSecret?: string | Uint8Array;
  cookieDomain?: string;
  cookiePath?: string;
  cookieMaxAge?: number;
}

// 解析批准表单的结果
export interface ParsedApprovalResult {
  state: any;
  headers: Record<string, string>;
}

// 使用 Zod 的 MCP 工具模式
export const ListTablesSchema = {};

export const QueryDatabaseSchema = {
  sql: z
    .string()
    .min(1, "SQL query cannot be empty")
    .describe("SQL query to execute (SELECT queries only)"),
};

export const ExecuteDatabaseSchema = {
  sql: z
    .string()
    .min(1, "SQL command cannot be empty")
    .describe("SQL command to execute (INSERT, UPDATE, DELETE, CREATE, etc.)"),
};

// MCP 响应类型
export interface McpTextContent {
  type: "text";
  text: string;
  isError?: boolean;
}

export interface McpResponse {
  content: McpTextContent[];
}

// 标准响应创建器
export function createSuccessResponse(message: string, data?: any): McpResponse {
  let text = `**Success**\n\n${message}`;
  if (data !== undefined) {
    text += `\n\n**Result:**\n\`\`\`json\n${JSON.stringify(data, null, 2)}\n\`\`\``;
  }
  return {
    content: [{
      type: "text",
      text,
    }],
  };
}

export function createErrorResponse(message: string, details?: any): McpResponse {
  let text = `**Error**\n\n${message}`;
  if (details !== undefined) {
    text += `\n\n**Details:**\n\`\`\`json\n${JSON.stringify(details, null, 2)}\n\`\`\``;
  }
  return {
    content: [{
      type: "text",
      text,
      isError: true,
    }],
  };
}

// 数据库操作结果类型
export interface DatabaseOperationResult<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  duration?: number;
}

// SQL 验证结果
export interface SqlValidationResult {
  isValid: boolean;
  error?: string;
}

// 重新导出在整个项目中使用的外部类型
export type { AuthRequest, OAuthHelpers, ClientInfo };