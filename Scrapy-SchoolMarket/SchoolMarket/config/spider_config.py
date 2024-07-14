# 爬虫运行间隔时间
INTERVAL_SECOND = 3600

# 校园集市用户token
USER_TOKEN = '自己的token'

# 请求头
HEADERS = {
    # 'Host': 'c.zanao.com',
    # 'accept': 'application/json, text/plain, */*',
    # 'x-requested-with': 'XMLHttpRequest',
    # 'x-sc-platform': 'android',
    'x-sc-alias': 'sysu',
    # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090621) XWEB/9105 Flue',
    # 'sec-fetch-site': 'same-origin',
    # 'sec-fetch-mode': 'cors',
    # 'sec-fetch-dest': 'empty',
    # 'accept-language': 'zh-CN,zh;q=0.9',
}

# 校园集市相关url
# 首页（从当前开始）
HOME_URL = "https://c.zanao.com/sc-api/thread/v2/list"
# 首页爬取页数，一页10个帖子
PAGES_COUNT = 5

# 热榜(最多10个帖子)
HOT_URL = "https://c.zanao.com/sc-api/thread/hot"

# 帖子(必须指定帖子id和url参数)
POST_BASE_URL = "https://c.zanao.com/sc-api/thread/info"

# 评论（必须指定帖子id参数）
COMMENT_BASE_URL = "https://c.zanao.com/sc-api/comment/list"
