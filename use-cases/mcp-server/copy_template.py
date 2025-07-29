#!/usr/bin/env python3
"""
MCP 服务器模板复制脚本

将完整的 MCP 服务器上下文工程模板复制到目标目录，
用于启动新的 MCP 服务器开发项目。使用 gitignore 感知复制
以避免复制构建产物和依赖项。

用法:
    python copy_template.py <目标目录>

示例:
    python copy_template.py my-mcp-server
    python copy_template.py /path/to/my-new-server
"""

import os
import sys
import shutil
import argparse
from pathlib import Path
from typing import List, Tuple, Set
import fnmatch


def parse_gitignore(gitignore_path: Path) -> Set[str]:
    """
    解析 .gitignore 文件并返回要忽略的模式集合。
    
    Args:
        gitignore_path: .gitignore 文件的路径
        
    Returns:
        gitignore 模式的集合
    """
    ignore_patterns = set()
    
    if not gitignore_path.exists():
        return ignore_patterns
    
    try:
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # 跳过空行和注释
                if line and not line.startswith('#'):
                    # 为保持一致性移除前导斜杠
                    pattern = line.lstrip('/')
                    ignore_patterns.add(pattern)
    except Exception as e:
        print(f"Warning: Could not read .gitignore: {e}")
    
    return ignore_patterns


def should_ignore_path(path: Path, template_root: Path, ignore_patterns: Set[str]) -> bool:
    """
    根据 gitignore 模式检查路径是否应该被忽略。
    
    Args:
        path: 要检查的路径
        template_root: 模板的根目录
        ignore_patterns: gitignore 模式的集合
        
    Returns:
        如果路径应该被忽略则返回 True，否则返回 False
    """
    # 获取相对于模板根目录的路径
    try:
        rel_path = path.relative_to(template_root)
    except ValueError:
        return False
    
    # 转换为使用正斜杠的字符串
    rel_path_str = str(rel_path).replace('\\', '/')
    
    # 对每个忽略模式进行检查
    for pattern in ignore_patterns:
        # 处理目录模式（以 / 结尾）
        if pattern.endswith('/'):
            pattern = pattern.rstrip('/')
            if rel_path_str.startswith(pattern + '/') or rel_path_str == pattern:
                return True
        # 处理通配符模式
        elif fnmatch.fnmatch(rel_path_str, pattern):
            return True
        # 处理精确匹配和前缀匹配
        elif rel_path_str == pattern or rel_path_str.startswith(pattern + '/'):
            return True
    
    return False


def get_template_files() -> List[Tuple[str, str]]:
    """
    获取要复制的模板文件列表及其相对路径。
    使用 gitignore 感知过滤来排除构建产物和依赖项。
    
    Returns:
        (源路径, 相对路径) 元组的列表
    """
    template_root = Path(__file__).parent
    files_to_copy = []
    
    # 解析 .gitignore 模式
    gitignore_path = template_root / '.gitignore'
    ignore_patterns = parse_gitignore(gitignore_path)
    
    # 将 copy_template.py 脚本本身添加到忽略模式中
    ignore_patterns.add('copy_template.py')
    
    # 遍历模板目录中的所有文件
    for root, dirs, files in os.walk(template_root):
        root_path = Path(root)
        
        # 过滤掉被忽略的目录
        dirs[:] = [d for d in dirs if not should_ignore_path(root_path / d, template_root, ignore_patterns)]
        
        for file in files:
            file_path = root_path / file
            
            # 如果文件应该被忽略则跳过
            if should_ignore_path(file_path, template_root, ignore_patterns):
                continue
            
            # 获取目标的相对路径
            rel_path = file_path.relative_to(template_root)
            
            # 将 README.md 重命名为 README_TEMPLATE.md
            if rel_path.name == 'README.md':
                target_rel_path = rel_path.parent / 'README_TEMPLATE.md'
            else:
                target_rel_path = rel_path
            
            files_to_copy.append((str(file_path), str(target_rel_path)))
    
    return files_to_copy


def create_directory_structure(target_dir: Path, files: List[Tuple[str, str]]) -> None:
    """
    为所有文件创建目录结构。
    
    Args:
        target_dir: 目标目录路径
        files: (源路径, 相对路径) 元组的列表
    """
    directories = set()
    
    for _, rel_path in files:
        dir_path = target_dir / Path(rel_path).parent
        if str(dir_path) != str(target_dir):  # 不添加根目录
            directories.add(dir_path)
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def copy_template_files(target_dir: Path, files: List[Tuple[str, str]]) -> int:
    """
    将所有模板文件复制到目标目录。
    
    Args:
        target_dir: 目标目录路径
        files: (源路径, 相对路径) 元组的列表
    
    Returns:
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
            print(f"  ✗ {rel_path} - Error: {e}")
    
    return copied_count


def validate_template_integrity(target_dir: Path) -> bool:
    """
    验证基本模板文件是否正确复制。
    
    Args:
        target_dir: 目标目录路径
    
    Returns:
        如果模板看起来完整则返回 True，否则返回 False
    """
    essential_files = [
        "CLAUDE.md",
        "README_TEMPLATE.md",
        ".claude/commands/prp-mcp-create.md",
        ".claude/commands/prp-mcp-execute.md",
        "PRPs/templates/prp_mcp_base.md",
        "PRPs/INITIAL.md",
        "package.json",
        "tsconfig.json",
        "src/index.ts",
        "src/types.ts"
    ]
    
    missing_files = []
    for file_path in essential_files:
        if not (target_dir / file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️  Warning: Some essential files are missing:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    return True


def print_next_steps(target_dir: Path) -> None:
    """
    打印使用模板的有用后续步骤。
    
    Args:
        target_dir: 目标目录路径
    """
    print(f"""
🎉 MCP Server template successfully copied to: {target_dir}

📋 Next Steps:

1. Navigate to your new project:
   cd {target_dir}

2. Install dependencies:
   npm install

3. Set up your environment:
   # Copy environment template (if needed)
   cp .env.example .env
   # Edit .env with your configuration

4. Start building your MCP server:
   # 1. Edit PRPs/INITIAL.md with your server requirements
   # 2. Generate PRP: /prp-mcp-create PRPs/INITIAL.md
   # 3. Execute PRP: /prp-mcp-execute PRPs/generated_prp.md

5. Development workflow:
   # Run tests
   npm test
   
   # Start development server
   npm run dev
   
   # Build for production
   npm run build

6. Read the documentation:
   # Check README_TEMPLATE.md for complete usage guide
   # Check CLAUDE.md for MCP development rules

🔗 Useful Resources:
   - MCP Specification: https://spec.modelcontextprotocol.io/
   - Examples: See examples/ directory
   - Testing: See tests/ directory

Happy MCP server building! 🤖
""")


def main():
    """复制模板脚本的主函数。"""
    parser = argparse.ArgumentParser(
        description="将 MCP 服务器上下文工程模板复制到新的项目目录",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python copy_template.py my-mcp-server
  python copy_template.py /path/to/my-new-server
  python copy_template.py ../customer-support-mcp
        """
    )
    
    parser.add_argument(
        "target_directory",
        help="新 MCP 服务器项目的目标目录"
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
    print("📂 扫描 MCP 服务器模板文件...")
    files_to_copy = get_template_files()
    
    if not files_to_copy:
        print("❌ 错误: 未找到模板文件。请确保您在模板目录中运行此脚本。")
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
        print("⚠️  模板可能不完整。请检查缺失的文件。")


if __name__ == "__main__":
    main()