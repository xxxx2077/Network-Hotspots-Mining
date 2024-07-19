# Scrapy settings for SchoolMarket project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "SchoolMarket"

SPIDER_MODULES = ["SchoolMarket.spiders"]
NEWSPIDER_MODULE = "SchoolMarket.spiders"

log_file_path = "logs/scrapy_log.log"
# Log setting
# 日志信息等级 CRITICAL ERROR WARNING INFO DEBUG
LOG_LEVEL = 'INFO'
# 日志保存路径
LOG_FILE = log_file_path
# 标准输出也写入日志，即print内容也存入日志
LOG_STDOUT = True

LOG_ENABLED = True


# cookie_pool = [
#     {"cookie_key1": "cookie_value1"},
#     {"cookie_key2": "cookie_value2"},
#     {"cookie_key3": "cookie_value3"},
#     # 添加更多cookie
# ]

# def get_random_cookie(cookie_pool):
#     """从cookie池中随机选择一个cookie"""
#     return random.choice(cookie_pool)

# def fetch_with_random_cookie(url, cookie_pool):
#     """使用随机选择的cookie访问URL"""
#     cookie = get_random_cookie(cookie_pool)
#     response = requests.get(url, cookies=cookie)
#     return response

# # 示例使用
# url = "http://example.com"
# response = fetch_with_random_cookie(url, cookie_pool)

# print("Status Code:", response.status_code)
# print("Response Content:", response.content)

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "SchoolMarket (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
   "Accept-Language": "en",
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "SchoolMarket.middlewares.SchoolmarketSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "SchoolMarket.middlewares.SchoolmarketDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   "SchoolMarket.pipelines.SchoolmarketPipeline": 300,
   "SchoolMarket.pipelines.CalculatePipeline": 400
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
# TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
