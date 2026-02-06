import json

# 第1页数据（10篇）
page1_data = [
    {"title":"卧室放绿植，治愈还是"致郁"？","url":"https://mp.weixin.qq.com/s/3osqFw7_UCMTaDBhL2WJ2Q","publishTime":"今天 15:30","isOriginal":True,"views":8,"likes":3,"shares":2,"favorites":3,"comments":0},
    {"title":"累了吗？给眼睛做个"绿色SPA" 💆‍♀️","url":"https://mp.weixin.qq.com/s/-BW5EhXeX6771Yb_5zzP_g","publishTime":"今天 15:18","isOriginal":False,"views":13,"likes":2,"shares":2,"favorites":2,"comments":0},
    {"title":"立春至，3个小仪式唤醒沉睡的植物与生活热爱","url":"https://mp.weixin.qq.com/s/SATwf1y99Ah_0yBG5VC84Q","publishTime":"昨天 15:28","isOriginal":True,"views":4,"likes":3,"shares":2,"favorites":3,"comments":0},
    {"title":"立春赏花图鉴：把春天最早的消息带给你 🌸","url":"https://mp.weixin.qq.com/s/Vhxhuc8hhAoLdCKSJbdFhA","publishTime":"昨天 12:33","isOriginal":False,"views":33,"likes":4,"shares":3,"favorites":5,"comments":0},
    {"title":"春节送礼攻略：别送烟酒了，这5盆\"吉利花\"长辈更喜欢","url":"https://mp.weixin.qq.com/s/fAw_k4CpB4SOFBFnTBX66A","publishTime":"星期一 11:40","isOriginal":True,"views":8,"likes":1,"shares":1,"favorites":2,"comments":0},
    {"title":"立春就急着施肥？难怪你的花总是黄叶！（10年养花血泪史）","url":"https://mp.weixin.qq.com/s/VNJopUikSwOjAxifQu6fiA","publishTime":"星期日 09:08","isOriginal":True,"views":18,"likes":3,"shares":2,"favorites":3,"comments":0},
    {"title":"君子兰冬季养护：温差管理与烂心预防完全指南","url":"https://mp.weixin.qq.com/s/dIFhnZJ5CUToR4Lx8HpiYQ","publishTime":"01月30日","isOriginal":True,"views":16,"likes":5,"shares":2,"favorites":4,"comments":0},
    {"title":"立春将至，你的植物\"醒\"了吗？3个关键动作唤醒满屋绿意","url":"https://mp.weixin.qq.com/s/_BXIF09-DkUPJQ8DSoJSgA","publishTime":"01月27日","isOriginal":True,"views":3,"likes":2,"shares":1,"favorites":2,"comments":0},
    {"title":"室内空气差？这5种植物堪称天然净化器","url":"https://mp.weixin.qq.com/s/70qVMWYYjD59nXap7HNAZA","publishTime":"01月25日","isOriginal":True,"views":17,"likes":2,"shares":2,"favorites":1,"comments":0},
    {"title":"一盆变十盆：4种常见植物的扦插技巧","url":"https://mp.weixin.qq.com/s/cXCmi7UbuX8mFdgya7NbqQ","publishTime":"01月23日","isOriginal":True,"views":18,"likes":2,"shares":3,"favorites":2,"comments":0}
]

# 第2-5页数据（29篇）
page2_5_data = [
    {"title":"第一次养植物？这5种\"防手黑绿植\"闭眼入","url":"https://mp.weixin.qq.com/s/e8TLV6kYOCxlhOfJpGJtGA","publishTime":"01月22日","isOriginal":True,"views":8,"likes":2,"shares":2,"favorites":2,"comments":0},
    {"title":"让绿意住进生活，让美好住进心里","url":"https://mp.weixin.qq.com/s/WezdSN8k_PU6hKfhYFXhrQ","publishTime":"01月21日","isOriginal":False,"views":30,"likes":2,"shares":1,"favorites":2,"comments":0},
    {"title":"新春好运来！5种年宵花寓意大揭秘，让家宅旺气满满！","url":"https://mp.weixin.qq.com/s/2TieYTkVEmwIcMk-2srMZQ","publishTime":"01月20日","isOriginal":True,"views":72,"likes":2,"shares":4,"favorites":2,"comments":0},
    {"title":"春节必备！精选年宵花，让喜庆持续到正月十五","url":"https://mp.weixin.qq.com/s/mPc5-sgMukjUePUgMkoOsw","publishTime":"01月19日","isOriginal":True,"views":16,"likes":4,"shares":2,"favorites":2,"comments":0},
    {"title":"春日阳台变菜园，超实用准备攻略","url":"https://mp.weixin.qq.com/s/YiBr3ZhL4UazdviWjtXOTw","publishTime":"01月18日","isOriginal":True,"views":11,"likes":3,"shares":2,"favorites":2,"comments":0}
]
