import datetime
import logging
import time

import scrapy
from scrapy import Request, FormRequest

from SchoolMarket.items import CommentItem, PostItem
from SchoolMarket.utils.database import MysqlOperator
from SchoolMarket.config.spider_config import *


# 热榜
class TraceSpider(scrapy.Spider):
    name = "trace"
    allowed_domains = ["c.zanao.com"]
    start_urls = []
    cookies = {
        'user_token': USER_TOKEN
    }
    headers = {
        # 'Host': 'c.zanao.com',
        # 'accept': 'application/json, text/plain, */*',
        # 'x-requested-with': 'XMLHttpRequest',
        # 'x-sc-platform': 'android',
        'x-sc-alias': 'sysu',
        # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090621) XWEB/9105 Flue',
        # 'sec-fetch-site': 'same-origin',
        # 'sec-fetch-mode': 'cors',
        # 'sec-fetch-dest': 'empty',
        # 'referer': 'https://c.zanao.com/p/hot?count=10',
        # 'accept-language': 'zh-CN,zh;q=0.9',
    }

    ids = []

    def start_requests(self):
        # 获取要追踪的帖子id
        sqlstr = "select id from post where monitoring=1 order by time;"
        self.db_opr = MysqlOperator()
        data = self.db_opr.query(sqlstr)
        self.ids = list(map(list, data))
        # print(self.ids)
        for id in self.ids:
            # print(id[0])
            body = {
                "id": str(id[0]),
                "url": "https://c.zanao.com/" + str(id[0]),
                # "isIOS": "false",
                # "from": ""
            }
            yield FormRequest(url=POST_BASE_URL, cookies=self.cookies, headers=self.headers, formdata=body,
                              callback=self.parse_post, meta={'id': id[0]})


    def parse_post(self, response):
        item = PostItem()
        # print(response.meta['id'], response.json())
        # 被删的帖子不再监控
        if not response.json()['data']['is_show']:
            print("帖子", response.meta['id'], "被删了")
            item['hot_val'] = -1
            item['thread_id'] = response.meta['id']
            yield item
        # print(response.json())
        post = response.json()['data']['detail']

        # post内没有hot_val ,在pipeline计算
        item['hot_val'] = 0
        item['thread_id'] = int(post['thread_id'])

        item['title'] = post['title']
        item['view_count'] = int(post['view_count'])
        item['content'] = post['content']
        item['nickname'] = post['nickname']
        item['cate_name'] = post['cate_name']
        # 这个时间不一定会记录，只有当数据库之前没有记录才会记录
        # 发布时间可能误差有一个小时，甚至一天，也可能精确到分钟
        item['timestamp'] = self.handle_post_time(post['post_time'])  # 时间戳，需要处理
        item['img_paths'] = post['img_paths']  # 数组，需要计算图片数量

        item['top'] = False if int(post['top_time']) == 0 else True
        item['l_count'] = int(post['like_num'])

        # 评论数c_count,评论总赞数c_l_count 在parse_comment中计算
         # 爬取评论
        params = {
            'id': post['thread_id']
        }
        yield FormRequest(url=COMMENT_BASE_URL, cookies=self.cookies, headers=self.headers, formdata=params,
                          meta={'post_item': item}, callback=self.parse_comment)

    def parse_comment(self, response):
        c_list = response.json()['data']['list']
        post_item = response.meta['post_item']
        post_id = post_item['thread_id']
        post_item['c_count'] = len(c_list)
        post_item['c_l_count'] = 0
        for comment in c_list:
            item = CommentItem()
            item['thread_id'] = post_id
            item['comment_id'] = comment['comment_id']
            item['reply_id'] = comment['reply_comment_id']
            item['content'] = comment['content']
            item['nickname'] = comment['nickname']
            item['timestamp'] = int(comment['post_time'])  # pipelines处理为datetime
            item['like_num'] = int(comment['like_num'])
            yield item
            post_item['c_l_count'] += int(comment['like_num'])
            post_item['c_count'] += len(comment['reply_list'])
            for reply in comment['reply_list']:
                item = CommentItem()
                item['thread_id'] = post_id
                item['comment_id'] = reply['comment_id']
                item['reply_id'] = reply['reply_comment_id']
                item['content'] = reply['content']
                item['nickname'] = reply['nickname']
                item['timestamp'] = int(reply['post_time'])  # pipelines处理为datetime
                item['like_num'] = int(reply['like_num'])
                yield item
                post_item['c_l_count'] += int(reply['like_num'])
        yield post_item

    def handle_post_time(self, post_time: str):
        p_time = int(time.time())
        # 一个月前的帖子没法爬（有真人验证），不考虑处理
        if self.valid_date(post_time, "%m-%d %H:%M"):
            # 跨年
            if post_time[:2] == "12" and time.localtime().tm_mon == 1:
                cur_year = str(time.localtime().tm_year - 1)
            else:
                cur_year = str(time.localtime().tm_year)
            post_time = cur_year + "-" + post_time + ":00"
            p_time = int(datetime.datetime.strptime(post_time, "%Y-%m-%d %H:%M:%S").timestamp())
        elif "分钟前" in post_time:
            hour = int(post_time[:-3])
            p_time = p_time - hour * 60
        elif "小时前" in post_time:
            hour = int(post_time[:-3])
            p_time = p_time - hour * 3600
        elif "天前" in post_time:
            day = int(post_time[:-2])
            p_time = p_time - day * 86400
        # 其它情况（应该只有“刚刚”）返回当前时间戳
        return p_time

    def valid_date(self, date_str: str, date_format: str):
        try:
            # ps：这里只是验证格式，转换的值未必是想要的（例如：不指定年份时默认1900年）
            datetime.datetime.strptime(date_str, date_format)
            return True
        except:
            return False
