#!/bin/bash
# 自动激活环境并运行对标发现脚本

# 1. 激活 MediaCrawler 的虚拟环境
source "/Users/dj/Desktop/全域自媒体运营/工具/MediaCrawler/venv/bin/activate"

# 2. 运行 Python 脚本 (切换到 smart_discovery.py)
echo "☕️ 已开启防休眠模式，任务结束前请勿合盖..."
caffeinate -i python "/Users/dj/Desktop/小静的skills/competitor-monitor/scripts/smart_discovery.py" "$@"
