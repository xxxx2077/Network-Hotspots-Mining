import json
import logging
import requests
import sys
import json
import mysql.connector
import pandas as pd
import numpy as np
import time
from SchoolMarket.utils.database import MysqlOperator
from SchoolMarket.config.tokens import *


# from SchoolMarket.Heat_Algorithm.pop_value_cal import DatabaseConnector

# 简易mysql封装
class DatabaseConnector:
    def __init__(self, host, port, user, password, database, charset='utf8'):
        self.config = {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'database': database,
            'charset': charset
        }
        self.connection = None

    def connect(self):
        self.connection = mysql.connector.connect(**self.config)

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query, args=None):
        cursor = self.connection.cursor()
        cursor.execute(query, args)
        result = cursor.fetchall()
        cursor.close()
        return result

    def update_record(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        cursor.close()


# 函数一：accesskey会过期，需要定时重新获取
def get_access_key(API_Key, Secret_Key):
    url = f"https://aip.baidubce.com/oauth/2.0/token?client_id={API_Key}&client_secret={Secret_Key}&grant_type=client_credentials"

    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text


# 函数二：获取情感分析接口原始的返回数据
def get_emotion_analysis(text, flag):
    # 定义百度API情感分析的token值和URL值
    if flag:
        token = bd_token1
    else:
        token = bd_token2
    url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?charset=UTF-8&access_token={}'.format(token)
    new_each = {'text': text}  # 将文本数据保存在变量new_each中，data的数据类型为string
    new_each = json.dumps(new_each)
    for _ in range(3):
        try:
            res = requests.post(url, data=new_each)  # 利用URL请求百度情感分析API
            break
        except requests.exceptions.RequestException as e:
            logging.warning(f"{_+1} times Attempt failed: {e}")
            # print(f"Attempt failed: {e}")
            time.sleep(2)  # 等待5秒再重试

    res_text = res.text  # 保存分析得到的结果，以string格式保存
    # print("content: ", res_text)
    result = res_text.find('items')  # 查找得到的结果中是否有items这一项
    if result != -1:  # 如果结果不等于-1，则说明存在items这一项
        json_data = json.loads(res.text)
        items = json_data['items'][0]  # 获取items中的内容
        # print(items)
        return items
    elif res_text.find('error'):
        json_data = json.loads(res.text)
        # print(f"error: {json_data['error_msg']}, code: {json_data['error_code']}")
        # 模型无法识别（一般是emoji）默认为中性评论
        if json_data['error_code'] == 216630:
            items = {
                "sentiment": 1,
                "positive_prob": 0.5,
                "negative_prob": 0.5,
                "confidence": 0.5
            }
            return items
        # 失败切换token尝试
        if json_data['error_code'] == 18:
            get_emotion_analysis(text, 1-flag)
            pass
        return None


count: int = 0


# 函数三：通过四个原始参数计算返回单一的情感分析值
# 算法为：（任待修改
def get_emotion_core(text, flag=0):
    items = get_emotion_analysis(text, flag)
    if items is None:
        return None  # 返回空值
    # 将0~1得分映射到-1~+1，可以再乘以置信度
    return (items['positive_prob'] - 0.5) * 2 * items["confidence"]
    # if items["sentiment"] == 1:
    #     if (items["positive_prob"] > items["negative_prob"]):
    #         return float(items["positive_prob"])
    #     else:
    #         return float(- items["negative_prob"])
    # elif items["sentiment"] == 0:
    #     # return float(items["sentiment"] - 1 + (1-items["confidence"])*items["positive_prob"] )
    #     return float(items["sentiment"] - 1 + items["positive_prob"])
    # else:
    #     return float(items["sentiment"] - 1 - items["negative_prob"])
    #
    # # sentiment_score = (items["sentiment"] - 1) + items["confidence"] * (items["positive_prob"] - items["negative_prob"])
    # return float(sentiment_score)


# 函数四：comments表所有的sentiment值重计算
def update_all_comments_sentiment(db_opr: MysqlOperator):
    try:
        # db_connector.connect()
        # cursor = db_connector.connection.cursor()
        # cursor.execute("SELECT id, content FROM comments WHERE sentiment IS NULL")
        # comments = cursor.fetchall()
        comments = db_opr.query("SELECT id, content FROM comments WHERE sentiment IS NULL")
        flag = bool(0)
        for comment in comments:
            comment_id, content = comment
            sentiment_score = get_emotion_core(content, flag)
            flag = not flag
            # 取反flag，使用另外一个token
            if sentiment_score is not None:
                update_query = f"UPDATE comments SET sentiment = {sentiment_score} WHERE id = {comment_id}"
                # db_connector.update_record(update_query)
                db_opr.exec_sql(update_query)
                global count
                count = count + 1
                # if (count % 10 == 0):
                #     print(count)

        # db_connector.connection.commit()
    except mysql.connector.Error as err:
        # db_connector.connection.rollback()
        print(f"Error: {err}")
        print(f"Count:{count}")
    finally:
        # cursor.close()
        # print(f"Count:{count}")
        # print("finish update all comments")
        logging.info(f"finish update {count} comments")
        pass


# 函数五：更新post表单个帖子记录的sentiment_negative值
def update_post_sentiment_negative(db_opr: MysqlOperator, post_id):
    try:
        # db_connector.connect()

        # 查询指定帖子ID下情感值为负数的评论的总和
        query = f"""
        SELECT SUM(sentiment) 
        FROM comments 
        WHERE pid = {post_id} AND sentiment < 0
        """
        # result = db_connector.execute_query(query, (post_id,))
        result = db_opr.query(query)

        if result and result[0][0] is not None:
            negative_sentiment_sum = result[0][0]
        else:
            negative_sentiment_sum = 0

        # 更新相应的帖子记录
        update_query = f"""
        UPDATE post 
        SET sentiment_negative = {negative_sentiment_sum} 
        WHERE id = {post_id}
        """
        # db_connector.update_record(update_query)
        # db_connector.connection.commit()
        db_opr.exec_sql(update_query)

        # print("Update successful.")

    except mysql.connector.Error as err:
        # db_connector.connection.rollback()
        print(f"Error: {err}")
    finally:
        # db_connector.disconnect()
        # print("finish update post")
        pass


# 函数六：更新post表所有的sentiment_negative值
count2: int = 0


def update_all_null_sentiment_negative(db_opr: MysqlOperator):
    try:
        # db_connector.connect()

        # 查找所有 sentiment_negative 字段为 NULL 的帖子
        query = """
        SELECT id 
        FROM post 
        WHERE sentiment_negative IS NULL
        """
        # results = db_connector.execute_query(query)
        results = db_opr.query(query)

        # 更新每一个找到的帖子
        for row in results:
            post_id = row[0]
            update_post_sentiment_negative(db_opr, post_id)
            global count2
            count2 = count2 + 1
            if count2 % 50 == 0:
                print(count2)

    except mysql.connector.Error as err:
        # db_connector.connection.rollback()
        print(f"Error: {err}")
    finally:
        # db_connector.disconnect()
        print("finish update all null")


def main():
    # client_id = "SMBgNnL7x5eOTfAdOupeo4vN"
    # client_secret = "mmwtvQ4mVdbS7pkV9Chq9j0TuPTRBcFM"
    #
    # access_key_response = get_access_key(client_id, client_secret)
    # print(access_key_response)
    #
    # sys.stdout.reconfigure(encoding='utf-8')
    # txt1 = "🍓"
    # result = get_emotion_core(txt1, flag=1)
    # print("测试结果：", result)

    # with open('senta_output.json', 'w', encoding='utf-8') as f:
    #     json.dump(result, f, ensure_ascii=False, indent=4)

    db_connector = DatabaseConnector(
        host="sse-21311572-train.mysql.rds.aliyuncs.com",
        port="3307",
        user="SSE_user1",
        password="SSE_user1test",
        database="sse_training"
    )
    # db_connector.connect()
    # update_all_comments_sentiment(db_connector)
    # update_post_sentiment_negative(db_connector, 1838179418)
    # update_all_null_sentiment_negative(db_connector)
    # db_connector.disconnect()


if __name__ == "__main__":
    main()

# import threading
# import queue

# thread_local = threading.local()

# def get_thread_flag():
#     if not hasattr(thread_local, 'flag'):
#         thread_local.flag = False
#     return thread_local.flag

# def worker(q, semaphore, db_connector):
#     while True:
#         comment = q.get()
#         if comment is None:
#             break

#         with semaphore:
#             comment_id, content = comment
#             flag = get_thread_flag()
#             sentiment_score = get_emotion_core(content, flag)
#             thread_local.flag = not flag  # 取反 flag
#             if sentiment_score is not None:
#                 update_query = f"UPDATE comments SET sentiment = {sentiment_score} WHERE id = {comment_id}"
#                 db_connector.update_record(update_query)

#         q.task_done()

# MAX_WORKERS = 2

# def update_comments_sentiment_c(db_connector):
#     try:
#         db_connector.connect()
#         cursor = db_connector.connection.cursor()
#         cursor.execute("SELECT id, content FROM comments")
#         comments = cursor.fetchall()

#         q = queue.Queue()
#         semaphore = threading.Semaphore(MAX_WORKERS)

#         for comment in comments:
#             q.put(comment)

#         for _ in range(MAX_WORKERS):
#             q.put(None)

#         threads = []
#         for _ in range(MAX_WORKERS):
#             t = threading.Thread(target=worker, args=(q, semaphore, db_connector))
#             t.start()
#             threads.append(t)

#         q.join()

#         for t in threads:
#             t.join()

#         db_connector.connection.commit()
#     except Exception as e:
#         db_connector.connection.rollback()
#         print(f"Error: {e}")
#     finally:
#         cursor.close()
