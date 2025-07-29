# 执行模板生成 PRP

执行综合模板生成 PRP，为特定技术/框架创建完整的上下文工程模板包。

## PRP 文件: $ARGUMENTS

## 执行流程

1. **加载模板生成 PRP**
   - 完整阅读指定的模板生成 PRP 文件
   - 理解目标技术和所有要求
   - 审查 PRP 中记录的所有网络研究发现
   - 遵循模板包创建的所有指令

2. **ULTRATHINK - 模板包设计**
   - 创建综合实施计划
   - 基于 PRP 研究规划完整的模板包结构
   - 设计领域特定的上下文工程适配
   - 将技术模式映射到上下文工程原则
   - 规划所有必需文件及其关系

3. **生成完整模板包**
   - 为技术用例创建完整的目录结构
   - 生成带有全局规则的领域特定 CLAUDE.md
   - 创建专门的模板 PRP 生成和执行命令
   - 开发带有研究发现的领域特定基础 PRP 模板
   - 包含来自网络研究的综合示例和文档

4. **验证模板包**
   - 运行 PRP 中指定的所有验证命令
   - 验证所有必需文件已创建并格式正确
   - 测试模板结构的完整性和准确性
   - 检查与基础上下文工程框架的集成

5. **质量保证**
   - 确保模板遵循所有上下文工程原则
   - 验证领域特定模式得到准确表示
   - 检查验证循环是否适合且可执行于该技术
   - 确认模板可立即用于目标技术

6. **完成实施**
   - 根据所有 PRP 要求审查模板包
   - 确保满足 PRP 的所有成功标准
   - 验证模板已准备好投入生产

## 模板包要求

创建具有以下确切结构的完整用例模板：

### 必需目录结构
```
use-cases/{technology-name}/
├── CLAUDE.md                                    # 领域全局规则
├── .claude/commands/
│   ├── generate-{technology}-prp.md            # 领域 PRP 生成
│   └── execute-{technology}-prp.md             # 领域 PRP 执行
├── PRPs/
│   ├── templates/
│   │   └── prp_{technology}_base.md            # 领域基础 PRP 模板
│   ├── ai_docs/                                # 领域文档（可选）
│   └── INITIAL.md                              # 示例功能请求
├── examples/                                   # 领域代码示例
├── copy_template.py                            # 模板部署脚本
└── README.md                                   # 综合使用指南
```

### 基于 PRP 研究的内容要求

**CLAUDE.md** 必须包含（领域全局规则）：
- 技术特定的工具和包管理命令
- 领域架构模式和约定
- 框架特定的开发工作流程序
- 技术特定的安全和最佳实践
- 常见陷阱和集成点

**领域 PRP 命令** 必须包含：
- 技术特定的研究流程和网络搜索策略
- 基于 PRP 发现的领域文档收集方法
- 框架适当的验证循环和测试模式
- 技术的专门实施蓝图

**基础 PRP 模板** 必须包含：
- 来自 PRP 中进行的网络研究的预填充领域上下文
- 技术特定的成功标准和验证门槛
- 框架适当的实施模式和示例
- 领域专门的文档引用和陷阱

**复制脚本 (copy_template.py)** 必须包含：
- 接受目标目录作为命令行参数
- 将整个模板目录结构复制到目标位置
- 包含所有文件：CLAUDE.md、.claude/、PRPs/、examples/、README.md
- 优雅地处理目录创建和错误处理
- 提供清晰的成功反馈和后续步骤

**README.md** 必须包含：
- 模板目的和功能的清晰描述
- 复制脚本使用说明（显著放置在顶部附近）
- 完整的 PRP 框架工作流程解释（3步流程）
- 带有文件解释的模板结构概述
- 技术特定的示例和功能
- 常见陷阱和故障排除指导

## 验证要求

### 结构验证
```bash
# 验证完整结构存在
find use-cases/{technology-name} -type f -name "*.md" | sort
ls -la use-cases/{technology-name}/.claude/commands/
ls -la use-cases/{technology-name}/PRPs/templates/

# 检查必需文件存在
test -f use-cases/{technology-name}/CLAUDE.md
test -f use-cases/{technology-name}/README.md
test -f use-cases/{technology-name}/PRPs/INITIAL.md
test -f use-cases/{technology-name}/copy_template.py

# 测试复制脚本功能
python use-cases/{technology-name}/copy_template.py 2>&1 | grep -q "Usage:" || echo "复制脚本需要适当的使用消息"
```

### 内容验证
```bash
# 检查不完整内容
grep -r "TODO\|PLACEHOLDER\|WEBSEARCH_NEEDED" use-cases/{technology-name}/
grep -r "{technology}" use-cases/{technology-name}/ | wc -l  # 应该为 0

# 验证领域特定内容存在
grep -r "framework\|library\|technology" use-cases/{technology-name}/CLAUDE.md
grep -r "WebSearch\|web search" use-cases/{technology-name}/.claude/commands/

# 验证 README 有必需部分
grep -q "Quick Start.*Copy Template" use-cases/{technology-name}/README.md
grep -q "PRP Framework Workflow" use-cases/{technology-name}/README.md
grep -q "python copy_template.py" use-cases/{technology-name}/README.md
```

### 功能测试
```bash
# 测试模板功能
cd use-cases/{technology-name}

# 验证命令正确命名
ls .claude/commands/ | grep "{technology}"

# 测试 INITIAL.md 示例存在且全面
wc -l PRPs/INITIAL.md  # 应该是实质性的，不只是几行
```

## 成功标准

- [ ] 完全按照指定创建完整的模板包结构
- [ ] 所有必需文件存在且格式正确
- [ ] 基于 PRP 研究，领域特定内容准确表示技术
- [ ] 上下文工程原则适当适配于技术
- [ ] 验证循环适当且可执行于框架
- [ ] 模板包可立即用于在领域中构建项目
- [ ] 与基础上下文工程框架的集成得到维护
- [ ] 来自 PRP 的所有网络研究发现正确集成到模板中
- [ ] 示例和文档全面且技术特定
- [ ] 复制脚本 (copy_template.py) 功能正常且文档完善
- [ ] README 在顶部显著包含复制脚本说明
- [ ] README 用具体示例解释完整的 PRP 框架工作流程

注意：如果任何验证失败，分析错误，修复模板包组件，并重新验证直到所有标准通过。模板必须准备好投入生产，并可立即用于使用目标技术的开发人员。