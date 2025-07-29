### 使用 Anthropic API 调用 Claude 的示例（模型和 API 密钥都是环境变量）

const response = await fetch('https://api.anthropic.com/v1/messages', {
method: 'POST',
headers: {
    'Content-Type': 'application/json',
    'x-api-key': this.apiKey,
    'anthropic-version': '2023-06-01'
},
body: JSON.stringify({
    model: this.model,
    max_tokens: 3000,
    messages: [{
    role: 'user',
    content: this.buildPRPParsingPrompt(prpContent, projectContext, config)
    }]
})
});

if (!response.ok) {
throw new Error(`Anthropic API 错误: ${response.status} ${response.statusText}`);
}

const result = await response.json();
const content = (result as any).content[0].text;

// 解析 JSON 响应
const aiTasks = JSON.parse(content);