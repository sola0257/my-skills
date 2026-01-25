import sys
import os
import json
import glob
import subprocess
import time
import random
import re
from datetime import datetime

# === 配置区域 ===
MEDIA_CRAWLER_PATH = "/Users/dj/Desktop/全域自媒体运营/工具/MediaCrawler"
PYTHON_EXEC = os.path.join(MEDIA_CRAWLER_PATH, "venv/bin/python")
DATA_DIR = os.path.join(MEDIA_CRAWLER_PATH, "data/xhs/json")

# 筛选标准
MIN_LIKES = 1000       # 爆文最低点赞
MAX_FANS = 50000       # 对标最大粉丝数 (超过这个数视为大V)
TARGET_COUNT = 3       # 目标找到多少个完美对标后停止
MAX_PAGES = 5          # 最多翻多少页

def parse_number(num_str):
    """解析数字 (处理 1.2万, 10万+ 等)"""
    if not num_str: return 0
    s = str(num_str).replace('+', '').replace(' ', '').strip()
    try:
        if '万' in s:
            return int(float(s.replace('万', '')) * 10000)
        return int(s)
    except:
        return 0

def run_search(keywords, page):
    """阶段一：运行搜索"""
    print(f"\n🔍 [阶段1] 正在搜索关键词: {keywords} (第 {page} 页)...")
    cmd = [
        PYTHON_EXEC, "main.py",
        "--platform", "xhs",
        "--lt", "qrcode",
        "--type", "search",
        "--keywords", keywords,
        "--start", str(page),
        "--headless", "False",
        "--get_comment", "no"
    ]
    try:
        subprocess.run(cmd, cwd=MEDIA_CRAWLER_PATH, check=True)
        return True
    except:
        return False

def get_candidates_from_search():
    """从搜索结果中提取候选人"""
    # 找到最新的搜索结果文件
    files = glob.glob(os.path.join(DATA_DIR, "search_contents_*.json"))
    if not files: return {}
    latest_file = max(files, key=os.path.getmtime)
    
    print(f"📂 分析搜索结果: {os.path.basename(latest_file)}")
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        return {}

    candidates = {}
    for note in data:
        likes = parse_number(note.get('liked_count', 0))
        if likes < MIN_LIKES: continue
        
        # 兼容扁平结构
        user_id = note.get('user_id') or note.get('user', {}).get('user_id')
        nickname = note.get('nickname') or note.get('user', {}).get('nickname', '未知')
        
        if not user_id: continue
        
        if user_id not in candidates:
            candidates[user_id] = {
                'id': user_id,
                'nickname': nickname,
                'top_note': note.get('title', ''),
                'likes': likes,
                'url': f"https://www.xiaohongshu.com/user/profile/{user_id}"
            }
    return candidates

def batch_check_fans(candidates):
    """阶段二：批量核查粉丝数"""
    if not candidates: return []
    
    # 构造 ID 列表 (MediaCrawler 支持逗号分隔的 URL)
    urls = [c['url'] for c in candidates.values()]
    url_str = ",".join(urls[:10]) # 一次最多查10个，防止卡死
    
    print(f"\n🕵️‍♀️ [阶段2] 正在核查 {len(urls[:10])} 位候选人的粉丝数...")
    print("⏳ 正在启动爬虫访问主页，请稍候...")
    
    cmd = [
        PYTHON_EXEC, "main.py",
        "--platform", "xhs",
        "--lt", "qrcode",
        "--type", "creator",
        "--creator_id", url_str,
        "--crawler_max_notes_count", "1", # 只抓1篇笔记以加快速度
        "--headless", "False",
        "--get_comment", "no"
    ]
    
    # 运行爬虫
    subprocess.run(cmd, cwd=MEDIA_CRAWLER_PATH, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 尝试从 creator JSON 中读取信息
    # MediaCrawler 应该会生成 creator_info 相关的 JSON，或者在 notes JSON 里包含 user info
    # 这里我们通过搜索最新的 notes 文件来反查 user info，因为 creator 模式下的 notes 包含详细 user info
    
    verified_users = []
    
    # 找最新的 creator 抓取结果
    files = glob.glob(os.path.join(DATA_DIR, "creator_contents_*.json"))
    if not files: 
        print("⚠️ 未找到主页数据，无法核实粉丝数。")
        return []
        
    latest_file = max(files, key=os.path.getmtime)
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            notes = json.load(f)
            
        # 建立 user_id -> fans 映射
        user_fans_map = {}
        for note in notes:
            uid = note.get('user_id') or note.get('user', {}).get('user_id')
            # 尝试获取粉丝数 (MediaCrawler 不同版本字段可能不同，通常在 user 字段里)
            # 如果 json 里没有 fans 字段，可能需要解析 raw_data 或者 logs
            # 这里做一个假设：如果 creator 模式返回的 note 包含 fans
            
            # 补救措施：MediaCrawler 的 creator 模式会在 data/xhs/json 下生成 creator_info_xxx.json 吗？
            # 如果没有，我们可能只能从 note 的 user 字段看运气
            
            # 暂时策略：如果没有粉丝数，我们默认保留，并在表格中标注 "未知"
            # 但根据之前的 log，user 字段里有 'fans': '56'
            user_info = note.get('user', {})
            # 扁平结构检查
            fans = note.get('fans') or user_info.get('fans')
            
            if uid and fans:
                user_fans_map[uid] = parse_number(fans)
                
        # 回填数据
        for uid, user in candidates.items():
            if uid in user_fans_map:
                fans = user_fans_map[uid]
                user['fans'] = fans
                if fans <= MAX_FANS:
                    verified_users.append(user)
            else:
                # 没查到的暂时跳过
                pass
                
    except Exception as e:
        print(f"❌ 解析粉丝数据失败: {e}")
        
    return verified_users

def main(keywords):
    final_list = []
    
    for page in range(1, MAX_PAGES + 1):
        # 1. 搜索
        if not run_search(keywords, page): break
        
        # 2. 提取候选人
        candidates = get_candidates_from_search()
        print(f"🧐 初筛发现 {len(candidates)} 个爆文账号，准备核查...")
        
        if not candidates:
            print("🔄 本页无结果，翻页...")
            continue
            
        # 3. 查粉丝 (这是最关键的一步)
        # 注意：为了节省时间，我们只取前 5 个最像的去查
        top_candidates = dict(list(candidates.items())[:5])
        valid_ones = batch_check_fans(top_candidates)
        
        # 4. 输出结果
        if valid_ones:
            print(f"\n🎉 成功找到 {len(valid_ones)} 个符合要求的对标！")
            print("| 昵称 | 粉丝数 | 爆文点赞 | 爆文标题 |")
            print("|---|---|---|---|")
            for u in valid_ones:
                print(f"| {u['nickname']} | {u['fans']} | {u['likes']} | {u['top_note']} |")
                final_list.append(u)
        
        # 5. 判断停止
        if len(final_list) >= TARGET_COUNT:
            print(f"\n✅ 任务完成！已累计找到 {len(final_list)} 个优质对标。")
            break
            
        print(f"\n🔄 当前数量 ({len(final_list)}/{TARGET_COUNT}) 不足，休息 10 秒后翻下一页...")
        time.sleep(10)

if __name__ == "__main__":
    kw = sys.argv[1] if len(sys.argv) > 1 else "家庭园艺"
    main(kw)
