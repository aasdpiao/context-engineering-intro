#!/usr/bin/env python3
"""
PydanticAI 模板复制脚本

将完整的 PydanticAI 上下文工程模板复制到目标目录
用于启动新的 PydanticAI 代理开发项目。

用法:
    python copy_template.py <目标目录>

示例:
    python copy_template.py my-agent-project
    python copy_template.py /path/to/my-new-agent
"""

import os
import sys
import shutil
import argparse
from pathlib import Path
from typing import List, Tuple


def get_template_files() -> List[Tuple[str, str]]:
    """
    获取要复制的模板文件列表及其相对路径。
    
    返回:
        (源路径, 相对路径) 元组列表
    """
    template_root = Path(__file__).parent
    files_to_copy = []
    
    # 核心模板文件
    core_files = [
        "CLAUDE.md",
        "README.md",
    ]
    
    for file in core_files:
        source_path = template_root / file
        if source_path.exists():
            # 在目标中将 README.md 重命名为 readme_template.md
            target_name = "README_TEMPLATE.md" if file == "README.md" else file
            files_to_copy.append((str(source_path), target_name))
    
    # Claude 命令目录
    commands_dir = template_root / ".claude" / "commands"
    if commands_dir.exists():
        for file in commands_dir.glob("*.md"):
            rel_path = f".claude/commands/{file.name}"
            files_to_copy.append((str(file), rel_path))
    
    # PRPs 目录
    prps_dir = template_root / "PRPs"
    if prps_dir.exists():
        # 复制 templates 子目录
        templates_dir = prps_dir / "templates"
        if templates_dir.exists():
            for file in templates_dir.glob("*.md"):
                rel_path = f"PRPs/templates/{file.name}"
                files_to_copy.append((str(file), rel_path))
        
        # 复制 INITIAL.md 示例
        initial_file = prps_dir / "INITIAL.md"
        if initial_file.exists():
            files_to_copy.append((str(initial_file), "PRPs/INITIAL.md"))
    
    # 示例目录 - 复制所有示例
    examples_dir = template_root / "examples"
    if examples_dir.exists():
        for example_dir in examples_dir.iterdir():
            if example_dir.is_dir():
                # 复制每个示例目录中的所有文件
                for file in example_dir.rglob("*"):
                    if file.is_file():
                        rel_path = file.relative_to(template_root)
                        files_to_copy.append((str(file), str(rel_path)))
    
    return files_to_copy


def create_directory_structure(target_dir: Path, files: List[Tuple[str, str]]) -> None:
    """
    为所有文件创建目录结构。
    
    参数:
        target_dir: 目标目录路径
        files: (源路径, 相对路径) 元组列表
    """
    directories = set()
    
    for _, rel_path in files:
        dir_path = target_dir / Path(rel_path).parent
        directories.add(dir_path)
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def copy_template_files(target_dir: Path, files: List[Tuple[str, str]]) -> int:
    """
    将所有模板文件复制到目标目录。
    
    参数:
        target_dir: 目标目录路径
        files: (源路径, 相对路径) 元组列表
    
    返回:
        成功复制的文件数量
    """
    copied_count = 0
    
    for source_path, rel_path in files:
        target_path = target_dir / rel_path
        
        try:
            shutil.copy2(source_path, target_path)
            copied_count += 1
            print(f"  ✓ {rel_path}")
        except Exception as e:
            print(f"  ✗ {rel_path} - 错误: {e}")
    
    return copied_count


def validate_template_integrity(target_dir: Path) -> bool:
    """
    验证基本模板文件是否正确复制。
    
    参数:
        target_dir: 目标目录路径
    
    返回:
        如果模板看起来完整则返回 True，否则返回 False
    """
    essential_files = [
        "CLAUDE.md",
        "README_TEMPLATE.md",
        ".claude/commands/generate-pydantic-ai-prp.md",
        ".claude/commands/execute-pydantic-ai-prp.md",
        "PRPs/templates/prp_pydantic_ai_base.md",
        "PRPs/INITIAL.md",
        "examples/basic_chat_agent/agent.py",
        "examples/testing_examples/test_agent_patterns.py"
    ]
    
    missing_files = []
    for file_path in essential_files:
        if not (target_dir / file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️  警告: 一些基本文件缺失:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    return True


def print_next_steps(target_dir: Path) -> None:
    """
    打印使用模板的有用后续步骤。
    
    参数:
        target_dir: 目标目录路径
    """
    print(f"""
🎉 PydanticAI 模板已成功复制到: {target_dir}

📋 后续步骤:

1. 导航到您的新项目:
   cd {target_dir}

2. 设置您的环境:
   # 创建虚拟环境
   python -m venv venv
   source venv/bin/activate  # Windows 上: venv\\Scripts\\activate

   # 提前安装包或让您的 AI 编码助手处理

3. 开始构建您的代理:
   # 1. 使用您的代理需求编辑 PRPs/INITIAL.md
   # 2. 生成 PRP: /generate-pydantic-ai-prp PRPs/INITIAL.md
   # 3. 执行 PRP: /execute-pydantic-ai-prp PRPs/generated_prp.md

5. 阅读文档:
   # 查看 README.md 获取完整使用指南
   # 查看 CLAUDE.md 获取 PydanticAI 开发规则

🔗 有用资源:
   - PydanticAI 文档: https://ai.pydantic.dev/
   - 示例: 查看 examples/ 目录
   - 测试: 查看 examples/testing_examples/

祝您代理构建愉快! 🤖
""")


def main():
    """复制模板脚本的主函数。"""
    parser = argparse.ArgumentParser(
        description="将 PydanticAI 上下文工程模板复制到新项目目录",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python copy_template.py my-agent-project
  python copy_template.py /path/to/my-new-agent
  python copy_template.py ../customer-support-agent
        """
    )
    
    parser.add_argument(
        "target_directory",
        help="新 PydanticAI 项目的目标目录"
    )
    
    parser.add_argument(
        "--force",
        action="store_true",
        help="如果目标目录存在则覆盖"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="显示将要复制的内容而不实际复制"
    )
    
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    args = parser.parse_args()
    
    # 将目标目录转换为 Path 对象
    target_dir = Path(args.target_directory).resolve()
    
    # 检查目标目录是否存在
    if target_dir.exists():
        if target_dir.is_file():
            print(f"❌ 错误: {target_dir} 是一个文件，不是目录")
            return
        
        if list(target_dir.iterdir()) and not args.force:
            print(f"❌ 错误: {target_dir} 不为空")
            print("使用 --force 覆盖现有目录")
            return
        
        if args.force and not args.dry_run:
            print(f"⚠️  覆盖现有目录: {target_dir}")
    
    # 获取要复制的文件列表
    print("📂 扫描 PydanticAI 模板文件...")
    files_to_copy = get_template_files()
    
    if not files_to_copy:
        print("❌ 错误: 未找到模板文件。确保您从模板目录运行此脚本。")
        return
    
    print(f"找到 {len(files_to_copy)} 个文件要复制")
    
    if args.dry_run:
        print(f"\n🔍 试运行 - 将复制到: {target_dir}")
        for _, rel_path in files_to_copy:
            print(f"  → {rel_path}")
        return
    
    # 创建目标目录和结构
    print(f"\n📁 在以下位置创建目录结构: {target_dir}")
    target_dir.mkdir(parents=True, exist_ok=True)
    create_directory_structure(target_dir, files_to_copy)
    
    # 复制文件
    print(f"\n📋 复制模板文件:")
    copied_count = copy_template_files(target_dir, files_to_copy)
    
    # 验证模板完整性
    print(f"\n✅ 成功复制 {copied_count}/{len(files_to_copy)} 个文件")
    
    if validate_template_integrity(target_dir):
        print("✅ 模板完整性检查通过")
        print_next_steps(target_dir)
    else:
        print("⚠️  模板可能不完整。检查缺失的文件。")


if __name__ == "__main__":
    main()