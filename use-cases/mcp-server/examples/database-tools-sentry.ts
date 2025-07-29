import * as Sentry from "@sentry/cloudflare";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { 
	Props, 
	ListTablesSchema, 
	QueryDatabaseSchema, 
	ExecuteDatabaseSchema,
	createErrorResponse,
	createSuccessResponse
} from "../types";
import { validateSqlQuery, isWriteOperation, formatDatabaseError } from "../database/security";
import { withDatabase } from "../database/utils";

const ALLOWED_USERNAMES = new Set<string>([
	// 添加应该有数据库写操作权限的 GitHub 用户名
	// 例如：'yourusername', 'coworkerusername'
	'coleam00'
]);

// 带 Sentry 的 MCP 工具错误处理助手
function handleError(error: unknown): { content: Array<{ type: "text"; text: string; isError?: boolean }> } {
	const eventId = Sentry.captureException(error);

	const errorMessage = [
		"**Error**",
		"There was a problem with your request.",
		"Please report the following to the support team:",
		`**Event ID**: ${eventId}`,
		process.env.NODE_ENV !== "production"
			? error instanceof Error
				? error.message
				: String(error)
			: "",
	].join("\n\n");

	return {
		content: [
			{
				type: "text",
				text: errorMessage,
				isError: true,
			},
		],
	};
}

export function registerDatabaseToolsWithSentry(server: McpServer, env: Env, props: Props) {
	// 工具 1：列出表 - 所有已认证用户可用
	server.tool(
		"listTables",
		"Get a list of all tables in the database along with their column information. Use this first to understand the database structure before querying.",
		ListTablesSchema,
		async () => {
			return await Sentry.startNewTrace(async () => {
				return await Sentry.startSpan({
					name: "mcp.tool/listTables",
					attributes: {
						'mcp.tool.name': 'listTables',
						'mcp.user.login': props.login,
					},
				}, async (span) => {
					// 设置用户上下文
					Sentry.setUser({
						username: props.login,
						email: props.email,
					});

					try {
						return await withDatabase((env as any).DATABASE_URL, async (db) => {
							// 单个查询获取所有表和列信息（使用您的工作查询）
							const columns = await db.unsafe(`
								SELECT 
									table_name, 
									column_name, 
									data_type, 
									is_nullable,
									column_default
								FROM information_schema.columns 
								WHERE table_schema = 'public' 
								ORDER BY table_name, ordinal_position
							`);
							
							// 按表分组列
							const tableMap = new Map();
							for (const col of columns) {
								// 使用 SQL 查询返回的 snake_case 属性名
								if (!tableMap.has(col.table_name)) {
									tableMap.set(col.table_name, {
										name: col.table_name,
										schema: 'public',
										columns: []
									});
								}
								tableMap.get(col.table_name).columns.push({
									name: col.column_name,
									type: col.data_type,
									nullable: col.is_nullable === 'YES',
									default: col.column_default
								});
							}
							
							const tableInfo = Array.from(tableMap.values());
							
							return {
								content: [
									{
										type: "text",
										text: `**Database Tables and Schema**\n\n${JSON.stringify(tableInfo, null, 2)}\n\n**Total tables found:** ${tableInfo.length}\n\n**Note:** Use the \`queryDatabase\` tool to run SELECT queries, or \`executeDatabase\` tool for write operations (if you have write access).`
									}
								]
							};
						});
					} catch (error) {
						console.error('listTables error:', error);
						span.setStatus({ code: 2 }); // 错误
						return handleError(error);
					}
				});
			});
		}
	);

	// 工具 2：查询数据库 - 所有已认证用户可用（只读）
	server.tool(
		"queryDatabase",
		"Execute a read-only SQL query against the PostgreSQL database. This tool only allows SELECT statements and other read operations. All authenticated users can use this tool.",
		QueryDatabaseSchema,
		async ({ sql }) => {
			return await Sentry.startNewTrace(async () => {
				return await Sentry.startSpan({
					name: "mcp.tool/queryDatabase",
					attributes: {
						'mcp.tool.name': 'queryDatabase',
						'mcp.user.login': props.login,
						'mcp.sql.query': sql.substring(0, 100), // 为安全起见截断
					},
				}, async (span) => {
					// 设置用户上下文
					Sentry.setUser({
						username: props.login,
						email: props.email,
					});

					try {
						// 验证 SQL 查询
						const validation = validateSqlQuery(sql);
						if (!validation.isValid) {
							return createErrorResponse(`Invalid SQL query: ${validation.error}`);
						}
						
						// 检查是否为写操作
						if (isWriteOperation(sql)) {
							return createErrorResponse(
								"Write operations are not allowed with this tool. Use the `executeDatabase` tool if you have write permissions (requires special GitHub username access)."
							);
						}
						
						return await withDatabase((env as any).DATABASE_URL, async (db) => {
							const results = await db.unsafe(sql);
							
							return {
								content: [
									{
										type: "text",
										text: `**Query Results**\n\`\`\`sql\n${sql}\n\`\`\`\n\n**Results:**\n\`\`\`json\n${JSON.stringify(results, null, 2)}\n\`\`\`\n\n**Rows returned:** ${Array.isArray(results) ? results.length : 1}`
									}
								]
							};
						});
					} catch (error) {
						console.error('queryDatabase error:', error);
						span.setStatus({ code: 2 }); // 错误
						return handleError(error);
					}
				});
			});
		}
	);

	// 工具 3：执行数据库 - 仅特权用户可用（写操作）
	if (ALLOWED_USERNAMES.has(props.login)) {
		server.tool(
			"executeDatabase",
			"Execute any SQL statement against the PostgreSQL database, including INSERT, UPDATE, DELETE, and DDL operations. This tool is restricted to specific GitHub users and can perform write transactions. **USE WITH CAUTION** - this can modify or delete data.",
			ExecuteDatabaseSchema,
			async ({ sql }) => {
				return await Sentry.startNewTrace(async () => {
					return await Sentry.startSpan({
						name: "mcp.tool/executeDatabase",
						attributes: {
							'mcp.tool.name': 'executeDatabase',
							'mcp.user.login': props.login,
							'mcp.sql.query': sql.substring(0, 100), // 为安全起见截断
							'mcp.sql.is_write': isWriteOperation(sql),
						},
					}, async (span) => {
						// 设置用户上下文
						Sentry.setUser({
							username: props.login,
							email: props.email,
						});

						try {
							// 验证 SQL 查询
							const validation = validateSqlQuery(sql);
							if (!validation.isValid) {
								return createErrorResponse(`Invalid SQL statement: ${validation.error}`);
							}
							
							return await withDatabase((env as any).DATABASE_URL, async (db) => {
								const results = await db.unsafe(sql);
								
								const isWrite = isWriteOperation(sql);
								const operationType = isWrite ? "Write Operation" : "Read Operation";
								
								return {
									content: [
										{
											type: "text",
											text: `**${operationType} Executed Successfully**\n\`\`\`sql\n${sql}\n\`\`\`\n\n**Results:**\n\`\`\`json\n${JSON.stringify(results, null, 2)}\n\`\`\`\n\n${isWrite ? '**⚠️ Database was modified**' : `**Rows returned:** ${Array.isArray(results) ? results.length : 1}`}\n\n**Executed by:** ${props.login} (${props.name})`
										}
									]
								};
							});
						} catch (error) {
							console.error('executeDatabase error:', error);
							span.setStatus({ code: 2 }); // 错误
							return handleError(error);
						}
					});
				});
			}
		);
	}
}