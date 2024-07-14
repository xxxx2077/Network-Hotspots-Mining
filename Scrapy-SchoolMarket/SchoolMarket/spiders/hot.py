import datetime
import time

import scrapy
from scrapy import FormRequest

from SchoolMarket.items import CommentItem, PostItem
from SchoolMarket.config.spider_config import *


# 热榜
class HotSpider(scrapy.Spider):
    name = "hot"
    allowed_domains = ["c.zanao.com"]
    start_urls = [
        HOT_URL
    ]
    cookies = {
        'user_token': USER_TOKEN
    }
    headers = HEADERS

    def start_requests(self):
        params = {
            'count': '10',  # 热榜帖子数量限制
        }
        yield FormRequest(url=HOT_URL, cookies=self.cookies, headers=self.headers, formdata=params)

    def parse(self, response):
        p_list = response.json()['data']['list']
        for post in p_list:
            item = PostItem()
            item['thread_id'] = int(post['thread_id'])
            item['title'] = post['title']
            item['view_count'] = int(post['view_count'])
            item['hot_val'] = int(post['hot_val'])
            # 爬取帖子内容，method默认是post
            body = {
                "id": post['thread_id'],
                "url": "https://c.zanao.com/" + post['thread_id'],
                # "isIOS": "false",
                # "from": ""
            }
            yield FormRequest(url=POST_BASE_URL, cookies=self.cookies, headers=self.headers, formdata=body,
                              meta={'post_item': item}, callback=self.parse_post)

    def parse_post(self, response):
        post = response.json()['data']['detail']
        # 传递过来的item
        item = response.meta['post_item']
        item['content'] = post['content']
        item['nickname'] = post['nickname']
        item['cate_name'] = post['cate_name']
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
            post_time = cur_year + post_time + ":00"
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
