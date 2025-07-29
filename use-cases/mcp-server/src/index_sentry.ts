import * as Sentry from "@sentry/cloudflare";
import OAuthProvider from "@cloudflare/workers-oauth-provider";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { McpAgent } from "agents/mcp";
import { Props } from "./types";
import { GitHubHandler } from "./auth/github-handler";
import { closeDb } from "./database/connection";
//@ts-ignore
import { registerDatabaseToolsWithSentry } from "./tools/database-tools-sentry";

// Sentry 配置助手
function getSentryConfig(env: Env) {
	return {
		// 您可以通过将 SENTRY_DSN 设置为假值来禁用 Sentry
		dsn: (env as any).SENTRY_DSN,
		// 采样率 1.0 意味着"捕获所有跟踪"
		tracesSampleRate: 1,
	};
}

export class MyMCP extends McpAgent<Env, Record<string, never>, Props> {
	server = new McpServer({
		name: "PostgreSQL Database MCP Server",
		version: "1.0.0",
	});

	/**
	 * 在 Durable Object 关闭时清理数据库连接
	 */
	async cleanup(): Promise<void> {
		try {
			await closeDb();
			console.log('数据库连接成功关闭');
		} catch (error) {
			console.error('数据库清理过程中出错:', error);
		}
	}

	/**
	 * Durable Objects 警报处理器 - 用于清理
	 */
	async alarm(): Promise<void> {
		await this.cleanup();
	}

	async init() {
		// 初始化 Sentry
		const sentryConfig = getSentryConfig(this.env);
		if (sentryConfig.dsn) {
			// @ts-ignore - Sentry.init 存在但类型可能不完整
			Sentry.init(sentryConfig);
		}

		// 使用 Sentry 仪表注册所有工具
		registerDatabaseToolsWithSentry(this.server, this.env, this.props);
	}
}

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