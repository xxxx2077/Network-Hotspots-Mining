import logging
import traceback
from SchoolMarket.utils.connect_pool import pool


class MysqlOperator(object):
    def __init__(self):
        # print(pool)
        # 获取连接池对象
        self.pool = pool
        self.get()

    def get(self):
        # 获取连接和游标
        self.conn, self.cursor = self.pool.get()

    def close(self):
        self.pool.close(conn=self.conn, cursor=self.cursor)

    # 查找，返回结果
    def query(self, sql):
        try:
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            if len(res)==0:
                logging.warning(f"No result in: {sql}")
            return res
        except Exception as e:
            # print('error: ', format(e))
            # print(sql)
            logging.error(f"query error in: {sql}")
            logging.error(f"Error message: {format(e)}")
            logging.error(f"Full traceback:\n{traceback.format_exc()}")
            self.conn.rollback()

        

    # 插入、更新等（参数化），返回受影响行数
    def exec_sql(self, sql, paras=()):
        count = 0
        try:
            self.cursor.execute(sql, paras)
            count = self.cursor.rowcount
            self.conn.commit()
        except Exception as e:
            # print('error: ', format(e))
            # print(sql, '\n', paras)
            logging.error(f"execute error in: {sql} parameters: {paras}")            
            logging.error(f"Error message: {format(e)}")
            logging.error(f"Full traceback:\n{traceback.format_exc()}")
            self.conn.rollback()
            # # 失败则重连
            # try: 
            #     self.get()
            # except Exception as reconnection_error:
            #     logging.error("Failed to re-establish database connection.")
            #     logging.error(f"Error message: {str(reconnection_error)}")
            #     logging.error(f"Full traceback:\n{traceback.format_exc()}")
        return count

if __name__ == "__main__":
    db_test = MysqlOperator()
    # print(db_test.query("select * from not_exist;"))    
    # print(db_test.query("select * from post where id=0 limit 0,1;"))
        
    print(db_test.exec_sql("update post set imgNum=0 where id=a;"))
    print(db_test.exec_sql("update post set imgNum=0 where id=0;"))