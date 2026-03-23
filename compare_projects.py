import os

def get_project_files(root_dir):
    """获取项目下所有文件的相对路径列表"""
    files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(full_path, root_dir)
            files.append(rel_path)
    return sorted(files)

# 获取 GitHub 原项目文件
github_backend_files = get_project_files('github-original-project/career-planner-backend')
github_frontend_files = get_project_files('github-original-project/career-planner-frontend')

# 获取当前项目文件
current_backend_files = get_project_files('career-planner-backend')
current_frontend_files = get_project_files('career-planner-frontend')

# 分析差异
print("=" * 80)
print("Backend 后端项目差异分析")
print("=" * 80)

# 新增文件（当前项目有，原项目没有）
backend_added = set(current_backend_files) - set(github_backend_files)
if backend_added:
    print("\n【新增文件】")
    for f in sorted(backend_added):
        print(f"  + {f}")

# 删除文件（原项目有，当前项目没有）
backend_removed = set(github_backend_files) - set(current_backend_files)
if backend_removed:
    print("\n【删除文件】")
    for f in sorted(backend_removed):
        print(f"  - {f}")

# 共同文件
backend_common = set(current_backend_files) & set(github_backend_files)
print(f"\n共同文件数量：{len(backend_common)}")

print("\n" + "=" * 80)
print("Frontend 前端项目差异分析")
print("=" * 80)

# 新增文件
frontend_added = set(current_frontend_files) - set(github_frontend_files)
if frontend_added:
    print("\n【新增文件】")
    for f in sorted(frontend_added):
        print(f"  + {f}")

# 删除文件
frontend_removed = set(github_frontend_files) - set(current_frontend_files)
if frontend_removed:
    print("\n【删除文件】")
    for f in sorted(frontend_removed):
        print(f"  - {f}")

# 共同文件
frontend_common = set(current_frontend_files) & set(github_frontend_files)
print(f"\n共同文件数量：{len(frontend_common)}")

# 保存结果到文件
with open('project_diff_summary.txt', 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("项目差异总结文档\n")
    f.write("=" * 80 + "\n\n")
    
    f.write("GitHub 原项目路径：github-original-project/\n")
    f.write("当前项目路径：career-planner-backend/ 和 career-planner-frontend/\n\n")
    
    f.write("=" * 80 + "\n")
    f.write("Backend 后端项目差异\n")
    f.write("=" * 80 + "\n\n")
    
    if backend_added:
        f.write("【新增文件】\n")
        for file in sorted(backend_added):
            f.write(f"  + {file}\n")
        f.write("\n")
    
    if backend_removed:
        f.write("【删除文件】\n")
        for file in sorted(backend_removed):
            f.write(f"  - {file}\n")
        f.write("\n")
    
    f.write(f"共同文件数量：{len(backend_common)}\n\n")
    
    f.write("=" * 80 + "\n")
    f.write("Frontend 前端项目差异\n")
    f.write("=" * 80 + "\n\n")
    
    if frontend_added:
        f.write("【新增文件】\n")
        for file in sorted(frontend_added):
            f.write(f"  + {file}\n")
        f.write("\n")
    
    if frontend_removed:
        f.write("【删除文件】\n")
        for file in sorted(frontend_removed):
            f.write(f"  - {file}\n")
        f.write("\n")
    
    f.write(f"共同文件数量：{len(frontend_common)}\n")

print("\n详细对比结果已保存到：project_diff_summary.txt")
