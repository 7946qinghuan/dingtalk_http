import os
from typing import Optional, List


class DirectoryTreeViewer:
    """目录结构查看器，以树形结构展示目录和文件"""

    def __init__(
        self,
        root_dir: Optional[str] = None,
        show_files: bool = True,
        show_hidden: bool = False,
        ignore_patterns: Optional[List[str]] = None,
        max_depth: Optional[int] = None,
    ):
        """
        初始化目录树查看器

        Args:
            root_dir: 根目录路径，默认当前目录
            show_files: 是否显示文件，默认True
            show_hidden: 是否显示隐藏文件/目录（以.开头），默认False
            ignore_patterns: 要忽略的文件/目录模式列表
            max_depth: 最大遍历深度，None表示无限制
        """
        self.root_dir = root_dir or os.getcwd()
        self.show_files = show_files
        self.show_hidden = show_hidden
        self.ignore_patterns = ignore_patterns or []
        self.max_depth = max_depth

        # 树形结构的装饰符
        self.PREFIX = "│   "
        self.LAST_PREFIX = "    "
        self.BRANCH = "├── "
        self.LAST_BRANCH = "└── "

    def _should_ignore(self, name: str) -> bool:
        """判断是否应该忽略某个文件/目录"""
        # 检查隐藏文件
        if not self.show_hidden and name.startswith("."):
            return True

        # 检查忽略模式
        for pattern in self.ignore_patterns:
            if pattern in name:
                return True

        return False

    def _tree_traverse(
        self,
        current_dir: str,
        prefix: str = "",
        is_last: bool = False,
        current_depth: int = 0,
    ) -> None:
        """
        递归遍历目录并打印树形结构

        Args:
            current_dir: 当前目录路径
            prefix: 前缀装饰符
            is_last: 是否是同级中的最后一个条目
            current_depth: 当前深度
        """
        # 检查最大深度
        if self.max_depth is not None and current_depth > self.max_depth:
            return

        try:
            # 获取目录内容并排序
            entries = sorted(os.listdir(current_dir))
        except PermissionError:
            # 处理权限不足的情况
            print(f"{prefix}{self.LAST_BRANCH if is_last else self.BRANCH}[权限不足]")
            return
        except Exception as e:
            # 处理其他异常
            print(
                f"{prefix}{self.LAST_BRANCH if is_last else self.BRANCH}[错误: {str(e)}]"
            )
            return

        # 过滤需要忽略的条目
        filtered_entries = [
            entry for entry in entries if not self._should_ignore(entry)
        ]

        # 分离目录和文件
        dirs = []
        files = []

        for entry in filtered_entries:
            entry_path = os.path.join(current_dir, entry)
            if os.path.isdir(entry_path) and not os.path.islink(entry_path):
                dirs.append(entry)
            elif self.show_files and not os.path.islink(entry_path):
                files.append(entry)

        # 处理目录
        total_entries = len(dirs) + (len(files) if self.show_files else 0)
        current_entry = 0

        for dir_name in dirs:
            current_entry += 1
            is_last_entry = current_entry == total_entries
            branch = self.LAST_BRANCH if is_last_entry else self.BRANCH
            new_prefix = prefix + (self.LAST_PREFIX if is_last_entry else self.PREFIX)

            # 打印目录名
            print(f"{prefix}{branch}{dir_name}/")

            # 递归处理子目录
            self._tree_traverse(
                os.path.join(current_dir, dir_name),
                new_prefix,
                is_last_entry,
                current_depth + 1,
            )

        # 处理文件（如果需要显示）
        if self.show_files:
            for file_name in files:
                current_entry += 1
                is_last_entry = current_entry == total_entries
                branch = self.LAST_BRANCH if is_last_entry else self.BRANCH

                # 打印文件名
                print(f"{prefix}{branch}{file_name}")

    def show_tree(self) -> None:
        """显示目录树"""
        print(f"📂 {os.path.abspath(self.root_dir)}")
        print("└── 目录结构开始")
        self._tree_traverse(self.root_dir)
        print("└── 目录结构结束")


# 使用示例
if __name__ == "__main__":
    # 方式1：查看当前目录（默认配置）
    print("=== 方式1：查看当前目录（默认配置）===")
    viewer1 = DirectoryTreeViewer(root_dir="/mnt/ssd2/steins/zhihao/dingtalk_http")
    viewer1.show_tree()
    print()

    # # 方式2：查看指定目录，不显示文件，忽略__pycache__和venv
    # print("=== 方式2：查看指定目录，不显示文件，忽略特定目录 ===")
    # viewer2 = DirectoryTreeViewer(
    #     root_dir="./",  # 可替换为你的目标目录，如 "~/projects/my_project"
    #     show_files=False,
    #     ignore_patterns=["__pycache__", "venv", ".git", "node_modules", "dist", "build"],
    #     max_depth=3  # 只显示3级深度
    # )
    # viewer2.show_tree()
    # print()

    # # 方式3：显示隐藏文件，显示所有深度
    # print("=== 方式3：显示隐藏文件，显示所有深度 ===")
    # viewer3 = DirectoryTreeViewer(
    #     root_dir="./",
    #     show_hidden=True,
    #     show_files=True,
    #     ignore_patterns=["__pycache__"]
    # )
    # viewer3.show_tree()
