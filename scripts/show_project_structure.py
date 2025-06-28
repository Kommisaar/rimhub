from pathlib import Path
from typing import Optional


def print_project_structure(root_path: Path, prefix: str = "", level: int = 0, max_depth: int = 5):
    """
    递归打印项目结构，带缩进和层级限制。

    :param root_path: 要打印的根目录路径
    :param prefix: 当前层级的前缀（用于递归）
    :param level: 当前层级数（用于控制递归深度）
    :param max_depth: 最大展示深度
    """
    if level > max_depth:
        return

    try:
        entries = sorted(root_path.iterdir(), key=lambda x: (not x.is_dir(), x.name))
    except PermissionError:
        print(f"{prefix}└── [Permission Denied]")
        return

    for i, path in enumerate(entries):
        # 忽略隐藏文件或特殊目录
        if path.name.startswith('.') or path.name in ('__pycache__', '__init__.py'):
            continue

        connector = "└── " if i == len(entries) - 1 else "├── "
        print(f"{prefix}{connector}{path.name}")

        if path.is_dir():
            new_prefix = prefix + ("    " if i == len(entries) - 1 else "│   ")
            print_project_structure(path, new_prefix, level + 1, max_depth)


def main(max_depth: int = 2):
    entry_point: Path = Path(__file__).parent.parent.absolute()
    print(f"Project Structure of {entry_point} (depth={max_depth}):\n")
    print_project_structure(entry_point, max_depth=max_depth)


if __name__ == '__main__':
    main(max_depth=5)