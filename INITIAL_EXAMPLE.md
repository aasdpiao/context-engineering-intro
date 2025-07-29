## 功能特性：

- 一个Pydantic AI代理，它将另一个Pydantic AI代理作为工具。
- 主代理的研究代理，然后是子代理的邮件起草代理。
- 与代理交互的CLI。
- 邮件起草代理使用Gmail，研究代理使用Brave API。

## 示例：

在`examples/`文件夹中，有一个README供你阅读，以了解示例的全部内容，以及在为上述功能创建文档时如何构建你自己的README。

- `examples/cli.py` - 使用此作为创建CLI的模板
- `examples/agent/` - 通读这里的所有文件，了解创建支持不同提供商和LLM的Pydantic AI代理、处理代理依赖关系以及向代理添加工具的最佳实践。

不要直接复制这些示例，它们完全是为不同的项目准备的。但将其用作灵感和最佳实践。

## 文档：

Pydantic AI文档：https://ai.pydantic.dev/

## 其他注意事项：

- 包含.env.example、README以及设置说明，包括如何配置Gmail和Brave。
- 在README中包含项目结构。
- 虚拟环境已经设置好必要的依赖项。
- 使用python_dotenv和load_env()处理环境变量
