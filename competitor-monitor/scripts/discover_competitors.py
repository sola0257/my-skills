import sys
import os
import json
import glob
import subprocess
import time

# 路径配置
MEDIA_CRAWLER_PATH = "/Users/dj/Desktop/全域自媒体运营/工具/MediaCrawler"
PYTHON_EXEC = os.path.join(MEDIA_CRAWLER_PATH, "venv/bin/python")
DATA_DIR = os.path.join(MEDIA_CRAWLER_PATH, "data/xhs/json")

def run_search(keywords):
    """调用 MediaCrawler 执行搜索"""
    print(f"🚀 开始搜索关键词: {keywords}")
    print("⏳这可能需要几分钟，请耐心等待（已开启防反爬延迟）...")
    
    cmd = [
        PYTHON_EXEC, "main.py",
        "--platform", "xhs",
        "--lt", "qrcode",
        "--type", "search",
        "--keywords", keywords,
        "--get_comment", "no",      # 禁用一级评论
        "--get_sub_comment", "no",  # 禁用二级评论
        "--headless", "False"       # 强制显示浏览器界面
    ]
    
    # 切换工作目录执行
    try:
        subprocess.run(cmd, cwd=MEDIA_CRAWLER_PATH, check=True)
        print("✅ 搜索任务完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 搜索失败: {e}")
        return False

def find_latest_json():
    """找到最新的搜索结果文件"""
    search_files = glob.glob(os.path.join(DATA_DIR, "search_*.json"))
    if not search_files:
        return None
    return max(search_files, key=os.path.getmtime)

def analyze_candidates(json_file):
    """分析搜索结果，寻找对标"""
    print(f"📂 分析数据文件: {os.path.basename(json_file)}")
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return

    candidates = {}
    
    # 行业特征词库 (用于判断垂直度)
    INDUSTRY_KEYWORDS = ["花", "植物", "园艺", "花园", "养护", "种植", "阳台", "绿植", "多肉", "盆栽"]
    
    for note in data:
        # 提取关键数据
        try:
            # 兼容处理点赞数 (处理 "1.2万", "10万+" 等格式)
            raw_likes = str(note.get('liked_count', 0))
            if '万' in raw_likes:
                likes = int(float(raw_likes.replace('万', '').replace('+', '')) * 10000)
            else:
                likes = int(raw_likes.replace('+', ''))

            # 适配 search 模式的扁平结构
            user_id = note.get('user_id') or note.get('user', {}).get('user_id')
            nickname = note.get('nickname') or note.get('user', {}).get('nickname', '未知')
            
            title = note.get('title', '无标题')
            note_id = note.get('note_id')
            
            # 垂直度打分 (简单算法)
            score = 0
            # 1. 昵称包含行业词
            if any(k in nickname for k in INDUSTRY_KEYWORDS):
                score += 5
            # 2. 标题包含行业词
            if any(k in title for k in INDUSTRY_KEYWORDS):
                score += 2
            
            # 筛选条件：点赞 > 500 (放宽标准，以免漏掉起号期黑马)
            if likes >= 500:
                if user_id not in candidates:
                    candidates[user_id] = {
                        'nickname': nickname,
                        'url': f"https://www.xiaohongshu.com/user/profile/{user_id}",
                        'top_note': title,
                        'likes': likes,
                        'score': score, # 记录垂直度分数
                        'note_url': f"https://www.xiaohongshu.com/explore/{note_id}"
                    }
                else:
                    # 如果该作者有多篇爆文，更新数据并加分
                    candidates[user_id]['score'] += 3 # 多篇爆文，垂直度概率大增
                    if likes > candidates[user_id]['likes']:
                        candidates[user_id]['top_note'] = title
                        candidates[user_id]['likes'] = likes
                        
        except Exception:
            continue

    # 输出报告
    print("\n🎯 --- 发现潜在对标账号 (按垂直度+热度排序) ---")
    print(f"共扫描笔记: {len(data)} 篇")
    
    # 过滤低分账号 (可能是路人)
    filtered_candidates = [c for c in candidates.values() if c['score'] >= 2]
    
    print(f"符合条件作者: {len(filtered_candidates)} 位 (已过滤非垂直账号)\n")
    
    if not filtered_candidates:
        print("⚠️ 未找到符合条件的作者，建议更换更精准的行业关键词。")
        return

    print("| 垂直度 | 昵称 | 爆文标题 | 点赞数 | 主页链接 |")
    print("|---|---|---|---|---|")
    
    # 优先按分数排序，其次按点赞
    sorted_candidates = sorted(filtered_candidates, key=lambda x: (x['score'], x['likes']), reverse=True)
    
    for c in sorted_candidates[:15]: 
        # 转换分数为星级
        stars = "⭐⭐⭐" if c['score'] >= 5 else "⭐"
        print(f"| {stars} | {c['nickname']} | {c['top_note']} | {c['likes']} | {c['url']} |")

    print("\n💡 筛选逻辑：")
    print("⭐⭐⭐：昵称含行业词，或有多篇行业爆文（高潜力对标）")
    print("⭐：单篇爆文命中行业词（需人工确认）")

if __name__ == "__main__":
    # 默认搜索词
    keywords = "办公室绿植,懒人绿植"
    if len(sys.argv) > 1:
        keywords = sys.argv[1]
        
    if run_search(keywords):
        latest_file = find_latest_json()
        if latest_file:
            analyze_candidates(latest_file)
        else:
            print("❌ 未找到生成的数据文件")
