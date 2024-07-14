import math
import pandas as pd
import numpy as np

from SchoolMarket.utils.database import MysqlOperator


# 计算热度值的函数
# 数据库实时运行之前不要使用衰减
def calculate_post_hotness(views, likes, total_comments, total_comment_likes, days_since_posted, gravity_factor=0.5):
    # 加权求和计算热度基准值 Ha
    base_hotness = 0.01 * views + 1 * likes + 1 * total_comments + 0.1 * total_comment_likes

    # 对数衰减计算热度值 H(t)
    hotness = base_hotness * math.exp(-gravity_factor * days_since_posted)
    return hotness


# 计算热度变化
# 引入封装的连接器
def calculate_and_update_hotval_rate(db_opr: MysqlOperator, pid):

    # 查询该pid的所有记录，按时间排序
    query = f"SELECT pid, id, hotVal_rate, viewNum, likeNum, comNum, c_likeNum, recordTime FROM pop_record " \
            f"WHERE pid = {pid} ORDER BY recordTime"
    # rows = db_connector.execute_query(query)
    rows = db_opr.query(query)

    # 将记录存储到DataFrame
    columns = ['pid', 'id', 'hotVal_rate', 'viewNum', 'likeNum', 'comNum', 'c_likeNum', 'recordTime']
    df = pd.DataFrame(rows, columns=columns)

    # 将recordTime转换为datetime类型
    df['recordTime'] = pd.to_datetime(df['recordTime'])

    # 遍历记录行
    for i in range(len(df)):
        pid, id, hotVal_rate, viewNum, likeNum, comNum, c_likeNum, time = df.iloc[i]

        # 通过是否有浏览量判断帖子记录是否有效（一般而言不会有0浏览量的帖子存在）
        if viewNum is not None:
            # 检查是否存在上一次记录
            if i > 0 and df.iloc[i - 1]['pid'] == pid:
                last_hotVal_rate, last_viewNum, last_likeNum, last_comNum, last_c_likeNum, last_time \
                    = df.iloc[i - 1][['hotVal_rate', 'viewNum', 'likeNum', 'comNum', 'c_likeNum', 'recordTime']]

                # 计算时间差
                time_diff = time - last_time
                hours_diff = time_diff.total_seconds() / 3600

                # 检查时间差是否大于等于1小时
                if hours_diff >= 0.9:
                    # 计算hotVal_rate的差值
                    hotVal_rate_diff = 0.02 * viewNum + likeNum + comNum + c_likeNum - (
                            0.02 * last_viewNum + last_likeNum + last_comNum + last_c_likeNum)

                    # 计算插值
                    hotVal_rate = hotVal_rate_diff / hours_diff

                    # 更新记录的hotVal_rate
                    update_query = f"UPDATE pop_record SET hotVal_rate = {hotVal_rate} WHERE id = {id}"
                    # db_connector.update_record(update_query)
                    db_opr.exec_sql(update_query)
                else:
                    # 寻找满足条件的记录
                    found = False
                    for j in range(i - 2, -1, -1):
                        prev_record = df.iloc[j]
                        if prev_record['pid'] != pid:
                            # 到达该帖子最早记录边界
                            break
                        prev_time_diff = last_time - prev_record['recordTime']
                        prev_hours_diff = prev_time_diff.total_seconds() / 3600

                        if prev_hours_diff >= 1:
                            # 计算hotVal_rate的差值
                            hotVal_rate_diff = 0.02 * last_viewNum + last_likeNum + last_comNum + last_c_likeNum - (
                                    0.02 * prev_record['viewNum'] + prev_record['likeNum'] + prev_record['comNum'] +
                                    prev_record['c_likeNum'])

                            # 计算插值
                            hotVal_rate = hotVal_rate_diff / prev_hours_diff

                            # 更新记录的hotVal_rate
                            update_query = f"UPDATE pop_record SET hotVal_rate = {hotVal_rate} WHERE id = {id}"
                            # db_connector.update_record(update_query)
                            db_opr.exec_sql(update_query)
                            found = True
                            break

                    if not found:
                        if last_hotVal_rate is None or np.isnan(last_hotVal_rate) or np.isinf(last_hotVal_rate) :
                            last_hotVal_rate = 0
                        update_query = f"UPDATE pop_record SET hotVal_rate = {last_hotVal_rate} WHERE id = {id}"
                        # db_connector.update_record(update_query)
                        db_opr.exec_sql(update_query)
                        hotVal_rate = last_hotVal_rate
            else:

                update_query = f"UPDATE pop_record SET hotVal_rate = 0 WHERE id = {id}"
                # db_connector.update_record(update_query)
                db_opr.exec_sql(update_query)
                hotVal_rate = 0

        # 返回最新记录的hotVal_rate，用于判断是否继续监控
        if i == len(df)-1:
            return hotVal_rate

