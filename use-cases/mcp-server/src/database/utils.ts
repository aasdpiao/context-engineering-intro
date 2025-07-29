import postgres from "postgres";
import { getDb } from "./connection";

/**
 * 执行数据库操作并进行适当的连接管理
 * 遵循 BASIC-DB-MCP.md 的模式，但适配了 PostgreSQL
 */
export async function withDatabase<T>(
	databaseUrl: string,
	operation: (db: postgres.Sql) => Promise<T>
): Promise<T> {
	const db = getDb(databaseUrl);
	const startTime = Date.now();
	try {
		const result = await operation(db);
		const duration = Date.now() - startTime;
		console.log(`数据库操作在 ${duration}ms 内成功完成`);
		return result;
	} catch (error) {
		const duration = Date.now() - startTime;
		console.error(`数据库操作在 ${duration}ms 后失败:`, error);
		// 重新抛出错误，以便调用代码中的 Sentry 可以捕获
		throw error;
	}
	// 注意：使用 PostgreSQL 连接池时，我们不关闭单个连接
	// 它们会自动返回到池中。池在 Durable Object 关闭时关闭。
}