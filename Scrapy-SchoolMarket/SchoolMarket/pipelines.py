# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter

from datetime import datetime

from SchoolMarket.items import CommentItem, PostItem
from SchoolMarket.utils import MysqlOperator, calculate_and_update_hotval_rate, calculate_post_hotness
from SchoolMarket.utils.ocr import ocr_img_from_url
from SchoolMarket.utils.sentiment_Rateing import update_all_comments_sentiment, update_post_sentiment_negative
from SchoolMarket.utils.correlation_cal_bert import update_null_relevance

class SchoolmarketPipeline:

    # 开关爬虫时运行
    def open_spider(self, spider):
        self.db_opr = MysqlOperator()
        print("start...", spider.name)

    def close_spider(self, spider):
        self.db_opr.close()
        print("end...", spider.name)

    def process_item(self, item, spider):
        if isinstance(item, PostItem):
            # 爬取主页才插入记录
            if spider.name == 'home' or spider.name == 'hot':
                p_time = datetime.fromtimestamp(item['timestamp'])
                imgNum = len(item['img_paths'])
                # 避免插入相同记录的方法
                # insert ignore（存在则忽略）
                # on duplicate key update（存在则更新）
                # replace（先删除原有再插入）
                sqlstr = f"insert into post(id, title, content, nickname, cate_name, time, imgNum, monitoring)" \
                         f" values(?, ?, ?, ?, ?, ?, ?, ?) on duplicate key update monitoring = 1;"
                para_tuple = (
                    item['thread_id'], item['title'], item['content'], item['nickname'], item['cate_name'], p_time,
                    imgNum, True
                )
                # 参数化
                self.db_opr.exec_sql(sqlstr, para_tuple)
                # 图片处理（ocr另外做）
                for img_path in item['img_paths']:
                    # id前八位是数字，代表上传时间，后面一长串字符串用于标识
                    # img_path以upload开头.jpeg结尾
                    id = img_path.replace('/', '')[6:-5]
                    imgURL = 'https://b1.cdn.zanao.com/' + img_path + '@!common'

                    sqlstr = f"insert ignore into picture(id, pid, imgURL)" \
                             f"values(?, ?, ?);"
                    para_tuple = (id, item['thread_id'], imgURL)
                    self.db_opr.exec_sql(sqlstr, para_tuple)

            # 被删贴，不再监控
            if item['hot_val'] == -1:
                # 这里的item只有两个字段hot_val和thread_id
                sqlstr = f"update post set monitoring = ? where id = ?;"
                para_tuple = (
                    False, item['thread_id']
                )
                self.db_opr.exec_sql(sqlstr, para_tuple)

            else:
                # 保存当前的热度相关信息 （热度值、浏览数、点赞数、评论数、是否置顶）
                # ps: 采用自己算法计算的热度值，覆盖集市自带的热度值
                days = (datetime.now().timestamp() - item['timestamp']) / 24 / 3600
                item['hot_val'] = calculate_post_hotness(views=item['view_count'], likes=item['l_count'],
                                                         total_comments=item['c_count'],
                                                         total_comment_likes=item['c_l_count'],
                                                         days_since_posted=days)
                # 当热度值太小则不再监控帖子
                # ps:由于每隔一段时间都会爬取一定数量的首页帖子（可重复），所以即使热度太低也会爬取一定次数，类似追踪的效果
                if item['hot_val'] < 10:
                    # print("hot value is too small", item['hot_val'], item['thread_id'])
                    sqlstr = f"update post set monitoring = ? where id = ?;"
                    para_tuple = (
                        False, item['thread_id']
                    )
                    self.db_opr.exec_sql(sqlstr, para_tuple)
                # 记录当前的时间
                r_time = datetime.now()
                # 主键: 自增id
                sqlstr = f"insert into pop_record(pid, hotVal, viewNum, likeNum, comNum, top, recordTime, c_likeNum )" \
                         f"values(?, ?, ?, ?, ?, ?, ?, ?);"
                para_tuple = (
                    item['thread_id'], item['hot_val'], item['view_count'], item['l_count'], item['c_count'],
                    item['top'], r_time, item['c_l_count']
                )
                self.db_opr.exec_sql(sqlstr, para_tuple)

        elif isinstance(item, CommentItem):
            # 忽略被删除的评论
            if item['content'] != '此内容已被用户在APP端自行删除':
                c_time = datetime.fromtimestamp(item['timestamp'])
                # 表名是comments
                # 不存在则插入，已经存在则更新点赞数
                sqlstr = f"insert into comments(id, pid, rid, content, nickname, time, likeNum) " \
                         f"values(?, ?, ?, ?, ?, ?, ?) on duplicate key update likeNum=?;"
                para_tuple = (
                    item['comment_id'], item['thread_id'], item['reply_id'], item['content'], item['nickname'],
                    c_time, item['like_num'], item['like_num']
                )
                self.db_opr.exec_sql(sqlstr, para_tuple)

        return item


class CalculatePipeline:
    # 开关爬虫时运行
    def open_spider(self, spider):
        self.db_opr = MysqlOperator()
        print("start...cal", spider.name)

    def close_spider(self, spider):
        # 帖子与中大相关性分析
        update_null_relevance(self.db_opr)        
        # ocr
        sqlstr = "select id, imgURL from picture where ocr is null;"
        rows = self.db_opr.query(sqlstr)
        for r in rows:
            id, imgURL = r
            result = ocr_img_from_url(url=imgURL, save=True)
            # 直接用url也可以，只是tqdm进度条影响日志查看
            # result = ppocr.ocr(imgURL, cls=True)
            if result[0] is None:
                res = ''
            else:
                # 将每一行的文本和得分连成一个字符串，形成一维字符串列表
                lines = [f"{line[0]}, {line[1]:.3f}" for box, line in result[0]]
                # 将所有行字符串连起来
                res = '\n'.join(lines)
                # 太长的识别文本忽略
                if len(res)>3000:
                    res = ''
            sqlstr = "update picture set ocr = ? where id = ?;"
            para_tuple = (res, id)
            self.db_opr.exec_sql(sqlstr, para_tuple)
        
        self.db_opr.close()
        print("end...cal", spider.name)

    # 计算并更新相关值
    def process_item(self, item, spider):
        if isinstance(item, PostItem):
            # 情感分析
            # 所有新增的未处理过的评论
            update_all_comments_sentiment(self.db_opr)
            # 更新帖子的负面评论分数
            update_post_sentiment_negative(self.db_opr, item['thread_id'])
            # 热度增长率
            latest_hot_rate = calculate_and_update_hotval_rate(db_opr=self.db_opr, pid=item['thread_id'])
            # 不再监控增长率低的帖子
            if latest_hot_rate < 5:
                # print("hot rate is too small", latest_hot_rate, item['thread_id'])
                sqlstr = "update post set monitoring = ? where id = ?;"
                para_tuple = (
                    False, item['thread_id']
                )
                self.db_opr.exec_sql(sqlstr, para_tuple)
        return item
