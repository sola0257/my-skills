#!/bin/bash
# 全平台抓取通用脚本
# 用法: ./run_platform.sh [平台代码] [关键词]
# 平台代码: xhs(小红书), dy(抖音), ks(快手), bili(B站)

PLATFORM=$1
KEYWORD=$2

if [ -z "$PLATFORM" ] || [ -z "$KEYWORD" ]; then
    echo "❌ 用法错误！请指定平台和关键词。"
    echo "示例: find-dy '室内绿植'"
    exit 1
fi

# 激活环境
source "/Users/dj/Desktop/全域自媒体运营/工具/MediaCrawler/venv/bin/activate"

echo "🚀 正在启动 [$PLATFORM] 抓取任务: $KEYWORD"
echo "☕️ 已开启防休眠模式..."

# 运行爬虫 (使用 search 模式)
# 注意：不同平台的参数可能略有微调，但 search 模式是通用的
caffeinate -i python "/Users/dj/Desktop/全域自媒体运营/工具/MediaCrawler/main.py" \
    --platform "$PLATFORM" \
    --lt qrcode \
    --type search \
    --keywords "$KEYWORD" \
    --headless False \
    --get_comment no
