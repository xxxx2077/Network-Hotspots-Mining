# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SchoolmarketItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class PostItem(scrapy.Item):
    # 主要信息
    thread_id = scrapy.Field()  # 帖子id
    title = scrapy.Field()  # 标题
    content = scrapy.Field()  # 帖子内容
    nickname = scrapy.Field()  # 帖主
    cate_name = scrapy.Field()  # 所属分类名称
    # 次要信息
    timestamp = scrapy.Field()  # 时间戳
    img_paths = scrapy.Field()  # 图片路径
    # 会变化，hot表存储
    top = scrapy.Field()  # 置顶
    c_count = scrapy.Field()  # 评论
    l_count = scrapy.Field()  # 点赞
    view_count = scrapy.Field()  # 浏览次数
    hot_val = scrapy.Field()  # 热度
    c_l_count = scrapy.Field()  # 评论总赞数


class CommentItem(scrapy.Item):
    thread_id = scrapy.Field()  # 所属帖子id
    comment_id = scrapy.Field()  # 评论id
    reply_id = scrapy.Field()  # 回复评论id
    content = scrapy.Field()  # 评论内容
    timestamp = scrapy.Field()  # 时间戳
    nickname = scrapy.Field()  # 回复人
    # 会变化，目前是存储最新值
    like_num = scrapy.Field()  # 点赞
