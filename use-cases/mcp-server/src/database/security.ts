import type { SqlValidationResult } from "../types";

/**
 * SQL 注入防护：基本 SQL 关键字验证
 * 这是一个简单的检查 - 在生产环境中应该使用参数化查询
 */
export function validateSqlQuery(sql: string): SqlValidationResult {
	const trimmedSql = sql.trim().toLowerCase();
	
	// 检查空查询
	if (!trimmedSql) {
		return { isValid: false, error: "SQL 查询不能为空" };
	}
	
	// 检查明显危险的模式
	const dangerousPatterns = [
		/;\s*drop\s+/i,
		/^drop\s+/i, // 查询开头的 DROP
		/;\s*delete\s+.*\s+where\s+1\s*=\s*1/i,
		/;\s*update\s+.*\s+set\s+.*\s+where\s+1\s*=\s*1/i,
		/;\s*truncate\s+/i,
		/^truncate\s+/i, // 查询开头的 TRUNCATE
		/;\s*alter\s+/i,
		/^alter\s+/i, // 查询开头的 ALTER
		/;\s*create\s+/i,
		/;\s*grant\s+/i,
		/;\s*revoke\s+/i,
		/xp_cmdshell/i,
		/sp_executesql/i,
	];
	
	for (const pattern of dangerousPatterns) {
		if (pattern.test(sql)) {
			return { isValid: false, error: "查询包含潜在危险的 SQL 模式" };
		}
	}
	
	return { isValid: true };
}

/**
 * 检查 SQL 查询是否为写操作
 */
export function isWriteOperation(sql: string): boolean {
	const trimmedSql = sql.trim().toLowerCase();
	const writeKeywords = [
		'insert', 'update', 'delete', 'create', 'drop', 'alter', 
		'truncate', 'grant', 'revoke', 'commit', 'rollback'
	];
	
	return writeKeywords.some(keyword => trimmedSql.startsWith(keyword));
}

/**
 * 格式化数据库错误以便用户友好显示
 */
export function formatDatabaseError(error: unknown): string {
	if (error instanceof Error) {
		// 隐藏敏感连接详情
		if (error.message.includes('password')) {
			return "数据库认证失败。请检查您的凭据。";
		}
		if (error.message.includes('timeout')) {
			return "数据库连接超时。请重试。";
		}
		if (error.message.includes('connection') || error.message.includes('connect')) {
			return "无法连接到数据库。请检查您的连接字符串。";
		}
		return `数据库错误: ${error.message}`;
	}
	return "发生了未知的数据库错误。";
}