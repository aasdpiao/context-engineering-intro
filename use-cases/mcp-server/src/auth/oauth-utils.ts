// 基于 Cookie 批准和上游 OAuth 流程的 OAuth 工具

import type { 
  AuthRequest, 
  ClientInfo,
  ApprovalDialogOptions,
  ParsedApprovalResult,
  UpstreamAuthorizeParams,
  UpstreamTokenParams 
} from "../types";

const COOKIE_NAME = "mcp-approved-clients";
const ONE_YEAR_IN_SECONDS = 31536000;

// --- 辅助函数 ---

/**
 * 将任意数据编码为 URL 安全的 base64 字符串。
 * @param data - 要编码的数据（将被字符串化）。
 * @returns URL 安全的 base64 编码字符串。
 */
function _encodeState(data: any): string {
	try {
		const jsonString = JSON.stringify(data);
		// Use btoa for simplicity, assuming Worker environment supports it well enough
		// For complex binary data, a Buffer/Uint8Array approach might be better
		return btoa(jsonString);
	} catch (e) {
		console.error("Error encoding state:", e);
		throw new Error("Could not encode state");
	}
}

/**
 * 将 URL 安全的 base64 字符串解码回原始数据。
 * @param encoded - URL 安全的 base64 编码字符串。
 * @returns 原始数据。
 */
function decodeState<T = any>(encoded: string): T {
	try {
		const jsonString = atob(encoded);
		return JSON.parse(jsonString);
	} catch (e) {
		console.error("Error decoding state:", e);
		throw new Error("Could not decode state");
	}
}

/**
 * 导入用于 HMAC-SHA256 签名的密钥字符串。
 * @param secret - 原始密钥字符串。
 * @returns 解析为 CryptoKey 对象的 Promise。
 */
async function importKey(secret: string): Promise<CryptoKey> {
	if (!secret) {
		throw new Error(
			"COOKIE_SECRET is not defined. A secret key is required for signing cookies.",
		);
	}
	const enc = new TextEncoder();
	return crypto.subtle.importKey(
		"raw",
		enc.encode(secret),
		{ hash: "SHA-256", name: "HMAC" },
		false, // not extractable
		["sign", "verify"], // key usages
	);
}

/**
 * 使用 HMAC-SHA256 签名数据。
 * @param key - 用于签名的 CryptoKey。
 * @param data - 要签名的字符串数据。
 * @returns 解析为十六进制字符串签名的 Promise。
 */
async function signData(key: CryptoKey, data: string): Promise<string> {
	const enc = new TextEncoder();
	const signatureBuffer = await crypto.subtle.sign("HMAC", key, enc.encode(data));
	// Convert ArrayBuffer to hex string
	return Array.from(new Uint8Array(signatureBuffer))
		.map((b) => b.toString(16).padStart(2, "0"))
		.join("");
}

/**
 * 验证 HMAC-SHA256 签名。
 * @param key - 用于验证的 CryptoKey。
 * @param signatureHex - 要验证的签名（十六进制字符串）。
 * @param data - 被签名的原始数据。
 * @returns 如果签名有效则解析为 true，否则为 false 的 Promise。
 */
async function verifySignature(
	key: CryptoKey,
	signatureHex: string,
	data: string,
): Promise<boolean> {
	const enc = new TextEncoder();
	try {
		// Convert hex signature back to ArrayBuffer
		const signatureBytes = new Uint8Array(
			signatureHex.match(/.{1,2}/g)!.map((byte) => Number.parseInt(byte, 16)),
		);
		return await crypto.subtle.verify("HMAC", key, signatureBytes.buffer, enc.encode(data));
	} catch (e) {
		// Handle errors during hex parsing or verification
		console.error("Error verifying signature:", e);
		return false;
	}
}

/**
 * 解析已签名的 Cookie 并验证其完整性。
 * @param cookieHeader - 来自请求的 Cookie 头的值。
 * @param secret - 用于签名的密钥。
 * @returns 如果 Cookie 有效则解析为已批准的客户端 ID 列表，否则为 null 的 Promise。
 */
async function getApprovedClientsFromCookie(
	cookieHeader: string | null,
	secret: string,
): Promise<string[] | null> {
	if (!cookieHeader) return null;

	const cookies = cookieHeader.split(";").map((c) => c.trim());
	const targetCookie = cookies.find((c) => c.startsWith(`${COOKIE_NAME}=`));

	if (!targetCookie) return null;

	const cookieValue = targetCookie.substring(COOKIE_NAME.length + 1);
	const parts = cookieValue.split(".");

	if (parts.length !== 2) {
		console.warn("Invalid cookie format received.");
		return null; // Invalid format
	}

	const [signatureHex, base64Payload] = parts;
	const payload = atob(base64Payload); // Assuming payload is base64 encoded JSON string

	const key = await importKey(secret);
	const isValid = await verifySignature(key, signatureHex, payload);

	if (!isValid) {
		console.warn("Cookie signature verification failed.");
		return null; // Signature invalid
	}

	try {
		const approvedClients = JSON.parse(payload);
		if (!Array.isArray(approvedClients)) {
			console.warn("Cookie payload is not an array.");
			return null; // Payload isn't an array
		}
		// Ensure all elements are strings
		if (!approvedClients.every((item) => typeof item === "string")) {
			console.warn("Cookie payload contains non-string elements.");
			return null;
		}
		return approvedClients as string[];
	} catch (e) {
		console.error("Error parsing cookie payload:", e);
		return null; // JSON parsing failed
	}
}

// --- 导出函数 ---

/**
 * 基于已签名的 Cookie 检查给定的客户端 ID 是否已被用户批准。
 *
 * @param request - 用于读取 Cookie 的传入 Request 对象。
 * @param clientId - 要检查批准状态的 OAuth 客户端 ID。
 * @param cookieSecret - 用于签名/验证批准 Cookie 的密钥。
 * @returns 如果客户端 ID 在有效 Cookie 的已批准客户端列表中则解析为 true，否则为 false 的 Promise。
 */
export async function clientIdAlreadyApproved(
	request: Request,
	clientId: string,
	cookieSecret: string,
): Promise<boolean> {
	if (!clientId) return false;
	const cookieHeader = request.headers.get("Cookie");
	const approvedClients = await getApprovedClientsFromCookie(cookieHeader, cookieSecret);

	return approvedClients?.includes(clientId) ?? false;
}


/**
 * 为 OAuth 授权渲染批准对话框
 * 对话框显示关于客户端和服务器的信息
 * 并包含提交批准的表单
 *
 * @param request - HTTP 请求
 * @param options - 批准对话框的配置
 * @returns 包含 HTML 批准对话框的 Response
 */
export function renderApprovalDialog(request: Request, options: ApprovalDialogOptions): Response {
	const { client, server, state } = options;

	// Encode state for form submission
	const encodedState = btoa(JSON.stringify(state));

	// Sanitize any untrusted content
	const serverName = sanitizeHtml(server.name);
	const clientName = client?.clientName ? sanitizeHtml(client.clientName) : "Unknown MCP Client";
	const serverDescription = server.description ? sanitizeHtml(server.description) : "";

	// Safe URLs
	const logoUrl = server.logo ? sanitizeHtml(server.logo) : "";
	const clientUri = client?.clientUri ? sanitizeHtml(client.clientUri) : "";
	const policyUri = client?.policyUri ? sanitizeHtml(client.policyUri) : "";
	const tosUri = client?.tosUri ? sanitizeHtml(client.tosUri) : "";

	// Client contacts
	const contacts =
		client?.contacts && client.contacts.length > 0
			? sanitizeHtml(client.contacts.join(", "))
			: "";

	// Get redirect URIs
	const redirectUris =
		client?.redirectUris && client.redirectUris.length > 0
			? client.redirectUris.map((uri) => sanitizeHtml(uri))
			: [];

	// Generate HTML for the approval dialog
	const htmlContent = `
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>${clientName} | Authorization Request</title>
        <style>
          /* Modern, responsive styling with system fonts */
          :root {
            --primary-color: #0070f3;
            --error-color: #f44336;
            --border-color: #e5e7eb;
            --text-color: #333;
            --background-color: #fff;
            --card-shadow: 0 8px 36px 8px rgba(0, 0, 0, 0.1);
          }
          
          body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, 
                         Helvetica, Arial, sans-serif, "Apple Color Emoji", 
                         "Segoe UI Emoji", "Segoe UI Symbol";
            line-height: 1.6;
            color: var(--text-color);
            background-color: #f9fafb;
            margin: 0;
            padding: 0;
          }
          
          .container {
            max-width: 600px;
            margin: 2rem auto;
            padding: 1rem;
          }
          
          .precard {
            padding: 2rem;
            text-align: center;
          }
          
          .card {
            background-color: var(--background-color);
            border-radius: 8px;
            box-shadow: var(--card-shadow);
            padding: 2rem;
          }
          
          .header {
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 1.5rem;
          }
          
          .logo {
            width: 48px;
            height: 48px;
            margin-right: 1rem;
            border-radius: 8px;
            object-fit: contain;
          }
          
          .title {
            margin: 0;
            font-size: 1.3rem;
            font-weight: 400;
          }
          
          .alert {
            margin: 0;
            font-size: 1.5rem;
            font-weight: 400;
            margin: 1rem 0;
            text-align: center;
          }
          
          .description {
            color: #555;
          }
          
          .client-info {
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 1rem 1rem 0.5rem;
            margin-bottom: 1.5rem;
          }
          
          .client-name {
            font-weight: 600;
            font-size: 1.2rem;
            margin: 0 0 0.5rem 0;
          }
          
          .client-detail {
            display: flex;
            margin-bottom: 0.5rem;
            align-items: baseline;
          }
          
          .detail-label {
            font-weight: 500;
            min-width: 120px;
          }
          
          .detail-value {
            font-family: SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
            word-break: break-all;
          }
          
          .detail-value a {
            color: inherit;
            text-decoration: underline;
          }
          
          .detail-value.small {
            font-size: 0.8em;
          }
          
          .external-link-icon {
            font-size: 0.75em;
            margin-left: 0.25rem;
            vertical-align: super;
          }
          
          .actions {
            display: flex;
            justify-content: flex-end;
            gap: 1rem;
            margin-top: 2rem;
          }
          
          .button {
            padding: 0.75rem 1.5rem;
            border-radius: 6px;
            font-weight: 500;
            cursor: pointer;
            border: none;
            font-size: 1rem;
          }
          
          .button-primary {
            background-color: var(--primary-color);
            color: white;
          }
          
          .button-secondary {
            background-color: transparent;
            border: 1px solid var(--border-color);
            color: var(--text-color);
          }
          
          /* Responsive adjustments */
          @media (max-width: 640px) {
            .container {
              margin: 1rem auto;
              padding: 0.5rem;
            }
            
            .card {
              padding: 1.5rem;
            }
            
            .client-detail {
              flex-direction: column;
            }
            
            .detail-label {
              min-width: unset;
              margin-bottom: 0.25rem;
            }
            
            .actions {
              flex-direction: column;
            }
            
            .button {
              width: 100%;
            }
          }
        </style>
      </head>
      <body>
        <div class="container">
          <div class="precard">
            <div class="header">
              ${logoUrl ? `<img src="${logoUrl}" alt="${serverName} Logo" class="logo">` : ""}
            <h1 class="title"><strong>${serverName}</strong></h1>
            </div>
            
            ${serverDescription ? `<p class="description">${serverDescription}</p>` : ""}
          </div>
            
          <div class="card">
            
            <h2 class="alert"><strong>${clientName || "A new MCP Client"}</strong> is requesting access</h1>
            
            <div class="client-info">
              <div class="client-detail">
                <div class="detail-label">Name:</div>
                <div class="detail-value">
                  ${clientName}
                </div>
              </div>
              
              ${
					clientUri
						? `
                <div class="client-detail">
                  <div class="detail-label">Website:</div>
                  <div class="detail-value small">
                    <a href="${clientUri}" target="_blank" rel="noopener noreferrer">
                      ${clientUri}
                    </a>
                  </div>
                </div>
              `
						: ""
				}
              
              ${
					policyUri
						? `
                <div class="client-detail">
                  <div class="detail-label">Privacy Policy:</div>
                  <div class="detail-value">
                    <a href="${policyUri}" target="_blank" rel="noopener noreferrer">
                      ${policyUri}
                    </a>
                  </div>
                </div>
              `
						: ""
				}
              
              ${
					tosUri
						? `
                <div class="client-detail">
                  <div class="detail-label">Terms of Service:</div>
                  <div class="detail-value">
                    <a href="${tosUri}" target="_blank" rel="noopener noreferrer">
                      ${tosUri}
                    </a>
                  </div>
                </div>
              `
						: ""
				}
              
              ${
					redirectUris.length > 0
						? `
                <div class="client-detail">
                  <div class="detail-label">Redirect URIs:</div>
                  <div class="detail-value small">
                    ${redirectUris.map((uri) => `<div>${uri}</div>`).join("")}
                  </div>
                </div>
              `
						: ""
				}
              
              ${
					contacts
						? `
                <div class="client-detail">
                  <div class="detail-label">Contact:</div>
                  <div class="detail-value">${contacts}</div>
                </div>
              `
						: ""
				}
            </div>
            
            <p>This MCP Client is requesting to be authorized on ${serverName}. If you approve, you will be redirected to complete authentication.</p>
            
            <form method="post" action="${new URL(request.url).pathname}">
              <input type="hidden" name="state" value="${encodedState}">
              
              <div class="actions">
                <button type="button" class="button button-secondary" onclick="window.history.back()">Cancel</button>
                <button type="submit" class="button button-primary">Approve</button>
              </div>
            </form>
          </div>
        </div>
      </body>
    </html>
  `;

	return new Response(htmlContent, {
		headers: {
			"Content-Type": "text/html; charset=utf-8",
		},
	});
}


/**
 * 解析来自批准对话框的表单提交，提取状态，
 * 并生成 Set-Cookie 头以将客户端标记为已批准。
 *
 * @param request - 包含表单数据的传入 POST Request 对象。
 * @param cookieSecret - 用于签名批准 Cookie 的密钥。
 * @returns 解析为包含解析状态和必要头的对象的 Promise。
 * @throws 如果请求方法不是 POST、表单数据无效或状态缺失。
 */
export async function parseRedirectApproval(
	request: Request,
	cookieSecret: string,
): Promise<ParsedApprovalResult> {
	if (request.method !== "POST") {
		throw new Error("Invalid request method. Expected POST.");
	}

	let state: any;
	let clientId: string | undefined;

	try {
		const formData = await request.formData();
		const encodedState = formData.get("state");

		if (typeof encodedState !== "string" || !encodedState) {
			throw new Error("Missing or invalid 'state' in form data.");
		}

		state = decodeState<{ oauthReqInfo?: AuthRequest }>(encodedState); // Decode the state
		clientId = state?.oauthReqInfo?.clientId; // Extract clientId from within the state

		if (!clientId) {
			throw new Error("Could not extract clientId from state object.");
		}
	} catch (e) {
		console.error("Error processing form submission:", e);
		// Rethrow or handle as appropriate, maybe return a specific error response
		throw new Error(
			`Failed to parse approval form: ${e instanceof Error ? e.message : String(e)}`,
		);
	}

	// Get existing approved clients
	const cookieHeader = request.headers.get("Cookie");
	const existingApprovedClients =
		(await getApprovedClientsFromCookie(cookieHeader, cookieSecret)) || [];

	// Add the newly approved client ID (avoid duplicates)
	const updatedApprovedClients = Array.from(new Set([...existingApprovedClients, clientId]));

	// Sign the updated list
	const payload = JSON.stringify(updatedApprovedClients);
	const key = await importKey(cookieSecret);
	const signature = await signData(key, payload);
	const newCookieValue = `${signature}.${btoa(payload)}`; // signature.base64(payload)

	// Generate Set-Cookie header
	const headers: Record<string, string> = {
		"Set-Cookie": `${COOKIE_NAME}=${newCookieValue}; HttpOnly; Secure; Path=/; SameSite=Lax; Max-Age=${ONE_YEAR_IN_SECONDS}`,
	};

	return { headers, state };
}

/**
 * 清理 HTML 内容以防止 XSS 攻击
 * @param unsafe - 可能包含 HTML 的不安全字符串
 * @returns 转义了 HTML 特殊字符的安全字符串
 */
function sanitizeHtml(unsafe: string): string {
	return unsafe
		.replace(/&/g, "&amp;")
		.replace(/</g, "&lt;")
		.replace(/>/g, "&gt;")
		.replace(/"/g, "&quot;")
		.replace(/'/g, "&#039;");
}

// --- OAuth 辅助函数 ---

/**
 * 为上游服务构建授权 URL。
 *
 * @param {UpstreamAuthorizeParams} options - 构建 URL 的参数
 * @returns {string} 授权 URL。
 */
export function getUpstreamAuthorizeUrl({
	upstream_url,
	client_id,
	scope,
	redirect_uri,
	state,
}: UpstreamAuthorizeParams): string {
	const upstream = new URL(upstream_url);
	upstream.searchParams.set("client_id", client_id);
	upstream.searchParams.set("redirect_uri", redirect_uri);
	upstream.searchParams.set("scope", scope);
	if (state) upstream.searchParams.set("state", state);
	upstream.searchParams.set("response_type", "code");
	return upstream.href;
}

/**
 * 从上游服务获取授权令牌。
 *
 * @param {UpstreamTokenParams} options - 令牌交换的参数
 * @returns {Promise<[string, null] | [null, Response]>} 解析为包含访问令牌或错误响应的数组的 Promise。
 */
export async function fetchUpstreamAuthToken({
	client_id,
	client_secret,
	code,
	redirect_uri,
	upstream_url,
}: UpstreamTokenParams): Promise<[string, null] | [null, Response]> {
	if (!code) {
		return [null, new Response("Missing code", { status: 400 })];
	}

	const resp = await fetch(upstream_url, {
		body: new URLSearchParams({ client_id, client_secret, code, redirect_uri }).toString(),
		headers: {
			"Content-Type": "application/x-www-form-urlencoded",
		},
		method: "POST",
	});
	if (!resp.ok) {
		console.log(await resp.text());
		return [null, new Response("Failed to fetch access token", { status: 500 })];
	}
	const body = await resp.formData();
	const accessToken = body.get("access_token") as string;
	if (!accessToken) {
		return [null, new Response("Missing access token", { status: 400 })];
	}
	return [accessToken, null];
}
