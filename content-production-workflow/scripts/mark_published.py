#!/usr/bin/env python3
import os
import datetime
import re
import sys
import glob

# 配置路径
BASE_PATH = "/Users/dj/Desktop/全域自媒体运营/内容发布/内容排期表"

def get_current_week_file():
    """找到当前日期对应的周排期表"""
    today = datetime.date.today()
    # 简单的逻辑：查找文件名包含 "2026年第X周" 的文件
    # 更严谨的逻辑应该解析文件中的日期范围，这里简化处理，假设最近修改的或者是本周的
    
    files = glob.glob(os.path.join(BASE_PATH, "*年第*周内容排期表.md"))
    if not files:
        return None
        
    # 找最近创建/修改的文件
    latest_file = max(files, key=os.path.getmtime)
    return latest_file

def mark_published(target_date=None, target_platform=None):
    if not target_date:
        target_date = datetime.date.today().strftime("%Y-%m-%d")
    
    file_path = get_current_week_file()
    if not file_path:
        print("❌ 未找到排期表文件")
        return

    print(f"📖 读取排期表: {os.path.basename(file_path)}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    updated_count = 0
    
    # 表格行正则: | 日期 | 星期 | 平台 | 选题 | 发布时间 | 状态 | 文件路径 |
    # 状态栏通常在第6列 (索引5)
    
    for line in lines:
        if "|" in line and target_date in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) > 6:
                # 检查平台
                current_platform = parts[3] # 索引3是平台
                current_status = parts[6]   # 索引6是状态
                
                if target_platform and target_platform not in current_platform:
                    new_lines.append(line)
                    continue

                # 更新状态
                if "✅" not in current_status:
                    # 替换状态列
                    # 这是一个简单的字符串替换，为了保持格式，我们替换图标
                    if "⏳" in line:
                        line = line.replace("⏳ 待生成", "✅ 已发布")
                        updated_count += 1
                    elif "📝" in line:
                        line = line.replace("📝 已生成", "✅ 已发布")
                        updated_count += 1
        
        new_lines.append(line)

    if updated_count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"✅ 已将 {target_date} 的 {updated_count} 个任务标记为已发布！")
    else:
        print(f"⚠️ 未找到 {target_date} 需要更新的任务 (可能已发布或日期错误)")

if __name__ == "__main__":
    # 解析参数
    date_arg = None
    platform_arg = None
    
    if len(sys.argv) > 1:
        date_arg = sys.argv[1] # 格式 YYYY-MM-DD
    if len(sys.argv) > 2:
        platform_arg = sys.argv[2]
        
    mark_published(date_arg, platform_arg)
