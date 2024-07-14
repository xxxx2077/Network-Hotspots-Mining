import logging
import time
import traceback
from dbutils.pooled_db import PooledDB
import SchoolMarket.config.db_config as config

"""
@功能：创建数据库连接池
"""


class MyConnectionPool(object):
    # 连接池对象
    __pool = None

    # 从连接池中取出一个连接conn和游标cursor
    def get(self):
        conn = self.__getconn()
        cursor = conn.cursor(prepared=True)
        return conn, cursor

    # 取出数据库连接
    def __getconn(self):
        if self.__pool is None:
            self.__pool = PooledDB(
                creator=config.DB_CREATOR,
                mincached=config.DB_MIN_CACHED,
                maxcached=config.DB_MAX_CACHED,
                maxshared=config.DB_MAX_SHARED,
                maxconnections=config.DB_MAX_CONNECTIONS,
                blocking=config.DB_BLOCKING,
                maxusage=config.DB_MAX_USAGE,
                setsession=config.DB_SET_SESSION,
                host=config.host,
                port=config.port,
                user=config.user,
                passwd=config.password,
                db=config.database,
                use_unicode=config.DB_USE_UNICODE,
                charset=config.charset
            )
        # # 查看连接池中的连接数量
        # print(f"连接池中的连接数量：{self.__pool.connections}")
        for retry in range(config.max_retry):
            try:
                conn = self.__pool.connection()
                return conn
            except Exception as e:
                logging.warning(f"Exception: {format(e)}")
                logging.warning(f"Full traceback:\n{traceback.format_exc()}")
                # 尝试重连
                if retry + 1 < config.max_retry:  
                    logging.warning(f"{retry + 1} tries failed.")
                    logging.warning(f"Try to connect after {config.delay} seconds")             
                    time.sleep(config.delay)
                else:
                    logging.error(f"Can't connect to database after {config.max_retry} tries.")
                    raise
        return None

    # 关闭连接归还给链接池
    def close(self, conn, cursor, commit=True):
        if commit:
            conn.commit()
        else:
            conn.rollback()
        cursor.close()
        conn.close()


# 获取连接池,实例化
pool = MyConnectionPool()

if __name__ == "__main__":
    c1,c2 = pool.get()
    c1,c2 = pool.get()
    pool.close(c1,c2)
    c1,c2 = pool.get()
    pool.close(c1,c2)
