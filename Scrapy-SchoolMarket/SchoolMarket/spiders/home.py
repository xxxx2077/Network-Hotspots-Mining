import datetime
import json

import scrapy
from scrapy import FormRequest, signals
from SchoolMarket.items import PostItem, CommentItem
from SchoolMarket.config.spider_config import *


# 首页
class HomeSpider(scrapy.Spider):
    name = "home"
    current_page = 1
    allowed_domains = ["c.zanao.com"]
    start_urls = [HOME_URL]

    url = HOME_URL
    cookies = {
        'user_token': USER_TOKEN
    }
    headers = HEADERS
    params = {
        'from_time': '0',  # 从时间戳往前的10条帖子（0则是最新的10条）
    }

    def start_requests(self):
        yield FormRequest(url=self.url, cookies=self.cookies, headers=self.headers, formdata=self.params)

    def parse(self, response, *args, **kwargs):  # *args, **kwargs不要也行
        p_list = response.json()['data']['list']
        for post in p_list:
            item = PostItem()
            item['thread_id'] = int(post['thread_id'])
            item['title'] = post['title']
            item['content'] = post['content']
            item['nickname'] = post['nickname']
            item['cate_name'] = post['cate_name']
            item['timestamp'] = int(post['p_time'])  # 时间戳，需要处理
            item['img_paths'] = post['img_paths']  # 数组，需要计算图片数量

            item['l_count'] = int(post['l_count'])
            item['view_count'] = int(post['view_count'])
            item['hot_val'] = int(post['hot_val'])
            item['top'] = False if int(post['top_time']) == 0 else True
            # 评论数c_count,评论总赞数c_l_count 在parse_comment中计算
            # 爬取评论
            params = {
                'id': post['thread_id']
            }
            yield FormRequest(url=COMMENT_BASE_URL, cookies=self.cookies, headers=self.headers, formdata=params,
                            meta={'post_item': item}, callback=self.parse_comment)

        # 当前页面最早那个帖子往前
        self.params['from_time'] = p_list[-1]['p_time']
        # 翻页(爬5页，50条帖子)
        if self.current_page <= PAGES_COUNT:
            self.current_page += 1
            yield FormRequest(url=self.url, cookies=self.cookies, headers=self.headers, formdata=self.params)


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
