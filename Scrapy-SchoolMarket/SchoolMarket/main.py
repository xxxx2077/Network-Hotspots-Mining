import logging
import time
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from multiprocessing import Process
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from SchoolMarket.config.spider_config import INTERVAL_SECOND

from SchoolMarket.spiders import HomeSpider, HotSpider, TraceSpider

settings = get_project_settings()
# configure_logging(settings)

def crawl():
    @defer.inlineCallbacks
    def serial():     
        crawler = CrawlerRunner(settings)
        yield crawler.crawl(TraceSpider)
        yield crawler.crawl(HomeSpider)
        yield crawler.crawl(HotSpider)
        reactor.stop()

    serial()
    reactor.run()
    print("ok")


def run_spider(interval: int = 0):
    # 单进程启动多个爬虫
    print(time.strftime("%Y-%m-%d %H:%M:%S"))
    start_time = time.time()
    # 串行
    process = Process(target=crawl)
    process.start()
    process.join()

    end_time = time.time()
    print("wait for next...")
    print(time.strftime("%Y-%m-%d %H:%M:%S"))
    print("elapsed time:", end_time - start_time)
    logging.info(f"---elapsed time: {end_time - start_time}")
    # 时间间隔是两次爬虫开始的间隔
    wait = interval + start_time - end_time
    if wait < 0:
        wait = 0
    time.sleep(wait)


import logging
from scrapy.utils.project import get_project_settings
from logging.handlers import TimedRotatingFileHandler

LOG_FILE = settings['LOG_FILE']

# 创建一个日志记录器
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # 设置日志级别

# 创建一个处理器，轮转日志文件
handler = TimedRotatingFileHandler(LOG_FILE, when="MIDNIGHT", interval=1, backupCount=7)
# handler.suffix = "%Y-%m-%d_%H-%M-%S"  # 自定义日志后缀可能会导致无法实现轮转
handler.setLevel(logging.INFO)

# 创建一个格式化器并将其添加到处理器中
formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s : %(message)s')
handler.setFormatter(formatter)

# 将处理器添加到记录器中
logger.addHandler(handler)

# 禁用 Scrapy 默认的日志处理器
from scrapy.utils.log import configure_logging
configure_logging(settings, install_root_handler=False)


if __name__ == '__main__':
    # 启动
    while True:
        run_spider(INTERVAL_SECOND)
