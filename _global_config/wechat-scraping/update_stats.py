import json

# 所有39篇文章的统计数据
all_stats_data = {
    'https://mp.weixin.qq.com/s/3osqFw7_UCMTaDBhL2WJ2Q': {'views':8,'likes':3,'shares':2,'favorites':3,'comments':0},
    'https://mp.weixin.qq.com/s/-BW5EhXeX6771Yb_5zzP_g': {'views':13,'likes':2,'shares':2,'favorites':2,'comments':0},
    'https://mp.weixin.qq.com/s/SATwf1y99Ah_0yBG5VC84Q': {'views':4,'likes':3,'shares':2,'favorites':3,'comments':0},
    'https://mp.weixin.qq.com/s/Vhxhuc8hhAoLdCKSJbdFhA': {'views':33,'likes':4,'shares':3,'favorites':5,'comments':0},
    'https://mp.weixin.qq.com/s/fAw_k4CpB4SOFBFnTBX66A': {'views':8,'likes':1,'shares':1,'favorites':2,'comments':0},
    'https://mp.weixin.qq.com/s/VNJopUikSwOjAxifQu6fiA': {'views':18,'likes':3,'shares':2,'favorites':3,'comments':0},
    'https://mp.weixin.qq.com/s/dIFhnZJ5CUToR4Lx8HpiYQ': {'views':16,'likes':5,'shares':2,'favorites':4,'comments':0},
    'https://mp.weixin.qq.com/s/_BXIF09-DkUPJQ8DSoJSgA': {'views':3,'likes':2,'shares':1,'favorites':2,'comments':0},
    'https://mp.weixin.qq.com/s/70qVMWYYjD59nXap7HNAZA': {'views':17,'likes':2,'shares':2,'favorites':1,'comments':0},
    'https://mp.weixin.qq.com/s/cXCmi7UbuX8mFdgya7NbqQ': {'views':18,'likes':2,'shares':3,'favorites':2,'comments':0},
    'https://mp.weixin.qq.com/s/e8TLV6kYOCxlhOfJpGJtGA': {'views':8,'likes':2,'shares':2,'favorites':2,'comments':0},
    'https://mp.weixin.qq.com/s/WezdSN8k_PU6hKfhYFXhrQ': {'views':30,'likes':2,'shares':1,'favorites':2,'comments':0},
    'https://mp.weixin.qq.com/s/2TieYTkVEmwIcMk-2srMZQ': {'views':72,'likes':2,'shares':4,'favorites':2,'comments':0},
    'https://mp.weixin.qq.com/s/mPc5-sgMukjUePUgMkoOsw': {'views':16,'likes':4,'shares':2,'favorites':2,'comments':0},
    'https://mp.weixin.qq.com/s/YiBr3ZhL4UazdviWjtXOTw': {'views':11,'likes':3,'shares':2,'favorites':2,'comments':0},
    'https://mp.weixin.qq.com/s/hgCDR0YjGuAwYoN3BpnYrA': {'views':5,'likes':2,'shares':1,'favorites':2,'comments':0},
    'https://mp.weixin.qq.com/s/PXLJiOhEub2E7XvAnDJAYw': {'views':155,'likes':4,'shares':5,'favorites':4,'comments':0},
    'https://mp.weixin.qq.com/s/LNWI89jK20JNdy3G96-ijQ': {'views':7,'likes':2,'shares':1,'favorites':2,'comments':0},
    'https://mp.weixin.qq.com/s/bfp6utvlZXgyJkq89DnzcQ': {'views':7,'likes':4,'shares':2,'favorites':3,'comments':0},
    'https://mp.weixin.qq.com/s/mSVlomSelxch98Kaj-RVnQ': {'views':25,'likes':5,'shares':6,'favorites':4,'comments':0},
    'https://mp.weixin.qq.com/s/uCk-6kMCVzIz-uNgsQuLVg': {'views':9,'likes':3,'shares':1,'favorites':3,'comments':0},
    'https://mp.weixin.qq.com/s/ugLEMUELzOm9d2n0wrb-Mw': {'views':33,'likes':2,'shares':3,'favorites':3,'comments':0},
    'https://mp.weixin.qq.com/s/JNXeKSNCzls_2LWP_5WJXw': {'views':13,'likes':2,'shares':2,'favorites':2,'comments':0},
    'https://mp.weixin.qq.com/s/AvdIcx7yuGvgUeQGkUn3DQ': {'views':53,'likes':2,'shares':2,'favorites':2,'comments':0},
    'https://mp.weixin.qq.com/s/4raJot6ETAeEyDS7aCPPXQ': {'views':20,'likes':2,'shares':2,'favorites':3,'comments':0},
    'https://mp.weixin.qq.com/s/ixZ49jw_kdHs3uYHtSBkEQ': {'views':32,'likes':5,'shares':5,'favorites':4,'comments':0},
    'https://mp.weixin.qq.com/s/1BHu6dKmjTz1QIwLNg3u0g': {'views':83,'likes':2,'shares':2,'favorites':4,'comments':0},
    'https://mp.weixin.qq.com/s/L8Hu-GjVoR_3y4JrB9fN1g': {'views':53,'likes':3,'shares':2,'favorites':2,'comments':0},
    'https://mp.weixin.qq.com/s/mb8WUbU0REVDr4BrThsFHA': {'views':49,'likes':4,'shares':3,'favorites':4,'comments':0},
    'https://mp.weixin.qq.com/s/gHs_83FJKedbZnTTf0m5Iw': {'views':65,'likes':3,'shares':2,'favorites':3,'comments':0},
    'https://mp.weixin.qq.com/s/r0YKBDolEk1BVrfzQZDtmA': {'views':416,'likes':3,'shares':5,'favorites':3,'comments':0},
    'https://mp.weixin.qq.com/s/nRuYIiRiE0pkc9XdKQveqA': {'views':18,'likes':2,'shares':2,'favorites':2,'comments':0},
    'https://mp.weixin.qq.com/s/NA6v7eHrdBpFbKnd2CzqpQ': {'views':25,'likes':3,'shares':2,'favorites':3,'comments':0},
    'https://mp.weixin.qq.com/s/zmJugGFcLFxw7euhtcsEYg': {'views':286,'likes':6,'shares':5,'favorites':5,'comments':1},
    'https://mp.weixin.qq.com/s/6J5hlNf8xkqq5STgJYK8ZQ': {'views':35,'likes':1,'shares':3,'favorites':0,'comments':0},
    'https://mp.weixin.qq.com/s/HkQKbdCWwsyabXbTC28pcQ': {'views':47,'likes':7,'shares':6,'favorites':6,'comments':6},
    'https://mp.weixin.qq.com/s/sG05m1K-7E8hFt3oV_A1dg': {'views':47,'likes':3,'shares':7,'favorites':3,'comments':0},
    'https://mp.weixin.qq.com/s/sbVbK6spsL8lWjnicn9EnQ': {'views':188,'likes':2,'shares':10,'favorites':2,'comments':0},
    'https://mp.weixin.qq.com/s/A9DTqy2JCvI5KvSUE7-44Q': {'views':17,'likes':4,'shares':1,'favorites':3,'comments':0}
}

# 读取现有数据
with open('wechat_articles_data.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

# 更新统计数据
updated_count = 0
for article in articles:
    url = article['url']
    if url in all_stats_data:
        stats = all_stats_data[url]
        article['views'] = stats['views']
        article['likes'] = stats['likes']
        article['shares'] = stats['shares']
        article['favorites'] = stats['favorites']
        article['comments'] = stats['comments']
        updated_count += 1

print(f'Successfully updated {updated_count} articles with statistics data')

# 保存更新后的数据
with open('wechat_articles_data_with_stats.json', 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

print('Data saved to wechat_articles_data_with_stats.json')
