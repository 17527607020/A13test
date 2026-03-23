import os
import difflib
from pathlib import Path
from datetime import datetime


def get_all_files(directory):
    """获取目录下所有文件及其相对路径"""
    files = []
    for root, dirs, filenames in os.walk(directory):
        # 跳过某些目录
        skip_dirs = ['.git', 'node_modules', '__pycache__', '.venv', 'venv']
        dirs[:] = [d for d in dirs if d not in skip_dirs]

        for filename in filenames:
            # 跳过二进制文件和某些特定类型
            if filename.endswith(('.pyc', '.pyo', '.dll', '.so', '.exe')):
                continue
            full_path = os.path.join(root, filename)
            rel_path = os.path.relpath(full_path, directory)
            files.append(rel_path)
    return files


def read_file_content(filepath):
    """读取文件内容"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        try:
            with open(filepath, 'r', encoding='gbk') as f:
                return f.read()
        except:
            return None


def compare_files(file1, file2):
    """比较两个文件的内容"""
    content1 = read_file_content(file1)
    content2 = read_file_content(file2)

    if content1 is None and content2 is None:
        return "都无法读取"
    elif content1 is None:
        return "仅在新版本中存在"
    elif content2 is None:
        return "仅在原版中存在"
    elif content1 == content2:
        return "内容相同"
    else:
        # 计算差异
        lines1 = content1.splitlines(keepends=True)
        lines2 = content2.splitlines(keepends=True)
        diff = list(difflib.unified_diff(lines1, lines2,
                    fromfile='original', tofile='current'))
        return f"内容有差异 ({len(diff)} 行差异)"


def main():
    current_project = r"E:\前端开发\vue\project\A13test03"
    original_project = r"E:\前端开发\vue\project\A13test03\github-original-project"

    print("开始对比项目...")
    print(f"当前项目：{current_project}")
    print(f"原项目：{original_project}")
    print("=" * 80)

    # 获取文件列表
    current_files = set(get_all_files(current_project))
    original_files = set(get_all_files(original_project))

    # 过滤掉一些不需要比较的文件
    filter_patterns = ['.gitignore', 'node_modules/',
                       '__pycache__', '.pyc', '.pyo']
    current_files = {f for f in current_files if not any(
        p in f for p in filter_patterns)}
    original_files = {f for f in original_files if not any(
        p in f for p in filter_patterns)}

    # 分析差异
    only_in_current = current_files - original_files
    only_in_original = original_files - current_files
    common_files = current_files & original_files

    print(f"\n当前项目文件数：{len(current_files)}")
    print(f"原项目文件数：{len(original_files)}")
    print(f"仅在当前项目中的文件：{len(only_in_current)}")
    print(f"仅在原项目中的文件：{len(only_in_original)}")
    print(f"共同拥有的文件：{len(common_files)}")

    # 生成报告
    report = []
    report.append("# 项目对比报告\n")
    report.append(
        f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report.append(f"**当前项目路径**: {current_project}\n")
    report.append(f"**原项目路径**: {original_project}\n\n")

    report.append("---\n\n")

    # 1. 新增文件
    report.append("## 一、新增的文件（当前项目有，原项目没有）\n\n")
    if only_in_current:
        for filepath in sorted(only_in_current):
            report.append(f"- `{filepath}`\n")
    else:
        report.append("*无新增文件*\n")
    report.append("\n")

    # 2. 删除的文件
    report.append("## 二、删除的文件（原项目有，当前项目没有）\n\n")
    if only_in_original:
        for filepath in sorted(only_in_original):
            report.append(f"- `{filepath}`\n")
    else:
        report.append("*无删除文件*\n")
    report.append("\n")

    # 3. 修改的文件
    report.append("## 三、修改的文件（内容发生变化）\n\n")
    modified_files = []
    for filepath in sorted(common_files):
        current_path = os.path.join(current_project, filepath)
        original_path = os.path.join(original_project, filepath)

        result = compare_files(current_path, original_path)
        if result != "内容相同":
            modified_files.append((filepath, result))

    if modified_files:
        report.append(f"共修改了 **{len(modified_files)}** 个文件\n\n")
        report.append("| 文件路径 | 变化情况 |\n")
        report.append("|---------|----------|\n")
        for filepath, change in modified_files:
            # 转义 markdown 特殊字符
            filepath_escaped = filepath.replace('|', '\\|')
            report.append(f"| `{filepath_escaped}` | {change} |\n")
    else:
        report.append("*无修改文件*\n")
    report.append("\n")

    # 4. 重点目录对比
    report.append("## 四、重点目录变化统计\n\n")

    # 按目录分组统计
    def group_by_directory(files):
        groups = {}
        for f in files:
            parts = f.split(os.sep)
            if len(parts) > 1:
                dir_name = parts[0]
                if dir_name not in groups:
                    groups[dir_name] = []
                groups[dir_name].append(f)
        return groups

    current_groups = group_by_directory(current_files)
    original_groups = group_by_directory(original_files)

    all_dirs = set(current_groups.keys()) | set(original_groups.keys())

    report.append("| 目录 | 当前项目 | 原项目 | 新增 | 删除 | 修改 |\n")
    report.append("|------|---------|-------|------|------|------|\n")

    for dir_name in sorted(all_dirs):
        current_dir_files = set(current_groups.get(dir_name, []))
        original_dir_files = set(original_groups.get(dir_name, []))

        added = len(current_dir_files - original_dir_files)
        deleted = len(original_dir_files - current_dir_files)

        # 计算修改的文件数
        modified_count = 0
        for f in (current_dir_files & original_dir_files):
            current_path = os.path.join(current_project, f)
            original_path = os.path.join(original_project, f)
            if compare_files(current_path, original_path) != "内容相同":
                modified_count += 1

        current_count = len(current_dir_files)
        original_count = len(original_dir_files)

        report.append(
            f"| {dir_name} | {current_count} | {original_count} | {added} | {deleted} | {modified_count} |\n")

    report.append("\n")

    # 5. 详细代码变更示例
    report.append("## 五、重要文件变更详情\n\n")

    # 选择一些重要文件展示详细变更
    important_extensions = ['.py', '.ts', '.vue', '.js', '.json', '.env']
    important_modified = [(f, c) for f, c in modified_files
                          if any(f.endswith(ext) for ext in important_extensions)]

    if important_modified:
        for filepath, _ in important_modified[:20]:  # 限制显示前 20 个
            current_path = os.path.join(current_project, filepath)
            original_path = os.path.join(original_project, filepath)

            content1 = read_file_content(original_path)
            content2 = read_file_content(current_path)

            if content1 and content2:
                lines1 = content1.splitlines(keepends=True)
                lines2 = content2.splitlines(keepends=True)
                diff = list(difflib.unified_diff(lines1, lines2,
                                                 fromfile=f'原/{filepath}',
                                                 tofile=f'现/{filepath}',
                                                 lineterm=''))

                if len(diff) > 0:
                    report.append(f"### {filepath}\n\n")
                    report.append("```diff\n")
                    # 只显示前 50 行差异
                    for line in diff[:50]:
                        report.append(line)
                    if len(diff) > 50:
                        report.append(f"... 还有 {len(diff) - 50} 行差异未显示\n")
                    report.append("```\n\n")
    else:
        report.append("*无重要文件变更*\n")

    # 6. 总结
    report.append("## 六、总结\n\n")
    report.append(
        f"1. **文件总数变化**: 原项目 {len(original_files)} 个文件 → 当前项目 {len(current_files)} 个文件\n")
    report.append(f"2. **新增文件**: {len(only_in_current)} 个\n")
    report.append(f"3. **删除文件**: {len(only_in_original)} 个\n")
    report.append(f"4. **修改文件**: {len(modified_files)} 个\n")
    report.append(
        f"5. **文件变化率**: {len(modified_files) / len(common_files) * 100:.2f}%\n\n")

    # 写入报告文件
    report_path = os.path.join(current_project, "项目对比报告.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.writelines(report)

    print(f"\n报告已生成：{report_path}")
    print("=" * 80)


if __name__ == "__main__":
    main()
