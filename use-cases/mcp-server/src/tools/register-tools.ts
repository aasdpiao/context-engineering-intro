import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { Props } from "../types";
import { registerDatabaseTools } from "../../examples/database-tools";

/**
 * 基于用户权限注册所有 MCP 工具
 */
export function registerAllTools(server: McpServer, env: Env, props: Props) {
	// 注册数据库工具
	registerDatabaseTools(server, env, props);
	
	// 未来的工具可以在这里注册
	// registerOtherTools(server, env, props);
}