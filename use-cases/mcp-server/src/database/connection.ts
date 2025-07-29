import postgres from "postgres";

let dbInstance: postgres.Sql | null = null;

/**
 * 获取数据库连接单例
 * 遵循 BASIC-DB-MCP.md 的模式，但适配了 PostgreSQL 的连接池
 */
export function getDb(databaseUrl: string): postgres.Sql {
	if (!dbInstance) {
		dbInstance = postgres(databaseUrl, {
			// Cloudflare Workers 的连接池设置
			max: 5, // 最多 5 个连接，以适应 Workers 6 个并发连接的限制
			idle_timeout: 20,
			connect_timeout: 10,
			// 启用预处理语句以获得更好的性能
			prepare: true,
		});
	}
	return dbInstance;
}

/**
 * 关闭数据库连接池
 * 在 Durable Object 关闭时调用此方法
 */
export async function closeDb(): Promise<void> {
	if (dbInstance) {
		try {
			await dbInstance.end();
		} catch (error) {
			console.error('关闭数据库连接时出错:', error);
		} finally {
			dbInstance = null;
		}
	}
}