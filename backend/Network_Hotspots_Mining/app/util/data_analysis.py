"""
本程序主要存放对pop_record表的热度数据分析的相关函数
可根据数据分析结果，设置数据库录入及维护的参数
根据所需函数在main中修改即可运行
"""

import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
#数据库连接封装

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

    def convert_type(self, value):
        """
        将numpy类型转换为Python内置类型
        """
        if isinstance(value, (np.integer, np.int64)):
            return int(value)
        if isinstance(value, (np.floating, np.float64)):
            return float(value)
        if isinstance(value, (np.str_, np.unicode_)):
            return str(value)
        return value




#抽取每个帖子的热度最高记录
def get_max_hotval_data(db_connector):
    query = """
    SELECT pid, MAX(hotVal) AS maxHotVal
    FROM pop_record
    GROUP BY pid
    ORDER BY maxHotVal DESC
    """
    result = db_connector.execute_query(query)
    columns = ['pid', 'maxHotVal']
    df = pd.DataFrame(result, columns=columns)
    return df

#热度最高的数据可视化绘制

def visualize_highest_data(df):
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']

    # 可视化：柱状图
    plt.figure(figsize=(10, 6))
    plt.bar(range(len(df['maxHotVal'])), df['maxHotVal'], color='skyblue')
    plt.xlabel('帖子排名')
    plt.ylabel('最高热度值')
    plt.title('前1500个帖子最高热度值柱状图')
    plt.show()

    # 可视化：饼状图（按帖子热度分布）
    plt.figure(figsize=(8, 8))
    df_sorted = df.sort_values(by='maxHotVal', ascending=False)
    top_10 = df_sorted.head(10)
    others = df_sorted.iloc[10:]['maxHotVal'].sum()
    labels = ['前1', '前2', '前3', '前4', '前5', '前6', '前7', '前8', '前9', '前10', '其他']
    sizes = list(top_10['maxHotVal']) + [others]
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired(range(len(labels))))
    plt.axis('equal')
    plt.title('最高热度值分布饼状图（前10个帖子及其他）')
    plt.show()



#查看最高热度hotVal低于x的帖子比例

def calculate_percentage_below_threshold(df, threshold):
    total_posts = len(df)
    below_threshold = df[df['maxHotVal'] < threshold].shape[0]
    percentage = (below_threshold / total_posts) * 100
    return percentage



#查看每百分之10的热度值覆盖距离

def calculate_hotval_distribution(df):
    # 对帖子最高热度值进行排序
    sorted_df = df.sort_values(by='maxHotVal')
    
    # 计算每百分之十的分位数
    percentiles = np.arange(0, 101, 10)
    percentile_values = np.percentile(sorted_df['maxHotVal'], percentiles)
    
    # 最高热度值
    max_hotval = sorted_df['maxHotVal'].max()
    
    # 打印结果
    print("热度值分布：")
    for i, percentile in enumerate(percentiles):
        print(f"第{percentile}百分位: {percentile_values[i]}")
    print(f"最高热度值: {max_hotval}")


#查看评论表情感倾向得分分布
def plot_sentiment_distribution(connector):
    # 连接数据库
    connector.connect()

    try:
        # 查询 sentiment 字段数据
        query = "SELECT sentiment FROM comments"
        sentiments = connector.execute_query(query)
        
        # 将数据转换为 pandas DataFrame
        df = pd.DataFrame(sentiments, columns=['sentiment'])
        print(df.shape)
        # 绘制柱状图
        plt.figure()
        
        # 使用 pandas 的 hist 方法绘制直方图，设置区间范围为 [-2, 2]，并分成 10 个区段
        df['sentiment'].hist(bins=50, range=(-2, 2), edgecolor='black', density = True)
        
        plt.title('Sentiment Distribution')
        plt.xlabel('Sentiment')
        plt.ylabel('Frequency')
        plt.grid(False)
        plt.show()
        
    finally:
        # 断开数据库连接
        connector.disconnect()
        
        
import numpy as np

#查看post表情感倾向得分分布
def plot_sentiment_negative_distribution(connector):
    # 连接数据库
    connector.connect()

    try:
        # 查询 sentiment 字段数据
        query = '''
                SELECT sentiment_negative 
                FROM post 
                WHERE time BETWEEN '2024-06-20' AND '2024-07-5'
                AND sentiment_negative < -5 ;
                '''
        # query = '''
        #         SELECT correlation 
        #         FROM post 
        #         WHERE time BETWEEN '2024-06-30' AND '2024-07-5'
        #         '''
        sentiments = connector.execute_query(query)
        
        # 将数据转换为 pandas DataFrame
        df = pd.DataFrame(sentiments, columns=['sentiment'])
        print(df.shape)
        
        # 绘制柱状图
        plt.figure()
        
        # 计算直方图的取值范围和间隔
        sentiment_range = (df['sentiment'].min(), df['sentiment'].max())
        bin_width = (sentiment_range[1] - sentiment_range[0]) / 30  # 将范围分成20个区段
        bins = np.arange(sentiment_range[0], sentiment_range[1] + bin_width, bin_width)
        
        # 使用 pandas 的 hist 方法绘制直方图，区间范围和间隔自适应
        df['sentiment'].hist(bins=bins, edgecolor='black', density=True)
        
        plt.title('Sentiment Distribution')
        plt.xlabel('Sentiment')
        plt.ylabel('Frequency')
        plt.grid(False)
        plt.show()
        
    finally:
        # 断开数据库连接
        connector.disconnect()
        
        


def main():
    db_connector = DatabaseConnector(
        host="sse-21311572-train.mysql.rds.aliyuncs.com",
        port="3307",
        user="SSE_user1",
        password="SSE_user1test",
        database="sse_training"
    )
    # db_connector.connect()
    # # df = get_max_hotval_data(db_connector)
    # plot_sentiment_negative_distribution(db_connector)
    # db_connector.disconnect()
    
    # visualize_highest_data(df)
    
    # threshold = 10  # 示例阈值，可以根据需要进行调整
    # percentage = calculate_percentage_below_threshold(df, threshold)
    # print(f"热度值小于{threshold}的帖子占总帖子的百分比为: {percentage:.2f}%")
    
    
    # calculate_hotval_distribution(df)

    

if __name__ == "__main__":
    main()
