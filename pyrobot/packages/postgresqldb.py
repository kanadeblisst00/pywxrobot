#-*- coding: utf-8 -*-
import re
import time
import psycopg2
import traceback
from psycopg2.extras import RealDictCursor
from psycopg2.errors import UniqueViolation, DatabaseError, OperationalError


class Database:

    def __init__(self, config):
        self.config = config
        self.conn = None
    
    def check_conn(self):
        if not self.conn or self.conn.closed:
           self.connect()
        else:
            try:
                self.conn.cursor().execute("SELECT 1")
            except (OperationalError, DatabaseError):
                self.connect()
    
    def connect(self, retry=0):
        if retry > 1:
            raise Exception("连接psycopg2次数超过限制(3次)！")
        try:
            self.conn = psycopg2.connect(**self.config)
        except OperationalError:
            traceback.print_exc()
            time.sleep(2)
            return self.connect(retry+1)
        except:
            traceback.print_exc()
            raise Exception("出现未知异常！")

    def execute(self, sql, value=None, retry=0, cursor=None):
        if retry>2:
            return
        self.check_conn()
        try:
            cursor1 = cursor or self.conn.cursor(cursor_factory=RealDictCursor)
            cursor1.execute(sql, value)
        except OperationalError:
            self.check_conn()
            traceback.print_exc()
            print(sql%value)
            return self.execute(sql, value, retry=retry, cursor=cursor)
        except UniqueViolation as e:
            str_e = str(e)
            self.conn.rollback()
            if "duplicate key value violates unique constraint" in str_e:
                pass
                # key = re.search(r'constraint "(.*?)"', str_e).group(1)
                # value = re.search(r'=(.*?)', str_e).group(1)
                # print(f'数据库已包含重复的值, 字段名: {key}, 值: {value}')
            else:
                traceback.print_exc()
                print(sql%value)
        except DatabaseError:
            traceback.print_exc()
            print(sql%value)
            self.conn.rollback()
            return self.execute(sql, value, retry=retry+1, cursor=cursor)
        except Exception as e:
            traceback.print_exc()
            print(sql%value)
            self.conn.rollback()
        else :
            self.conn.commit()
            return True
        finally:
            if not cursor:
                cursor1.close()
        return False
    
    def select(self, sql, value=None):
        self.check_conn()
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            if self.execute(sql, value, cursor=cursor):
                for row in cursor.fetchall():
                    yield dict(row)
    
    def execute_many(self, sql, values, cursor=None, retry=0) -> int:
        if retry>2:
            return
        self.check_conn()
        try:
            cursor1 = cursor or self.conn.cursor(cursor_factory=RealDictCursor)
            cursor1.executemany(sql, values)
        except OperationalError:
            self.check_conn()
            return self.execute_many(sql, values, retry=retry)
        except UniqueViolation as e:
            str_e = str(e)
            self.conn.rollback()
            if "duplicate key value violates unique constraint" in str_e:
                key = re.search(r'constraint "(.*?)"', str_e).group(1)
                value = re.search(r'=(.*?)', str_e).group(1)
                print(f'数据库已包含重复的值, 字段名: {key}, 值: {value}')
            else:
                print(e)
            n = 0
            for value in values:
                if self.execute(sql, value, cursor=cursor):
                    n += 1
            return n 
        except DatabaseError as e:
            import traceback
            traceback.print_exc()

            self.conn.rollback()
            return self.execute_many(sql, values, retry=retry+1)
        except Exception as e:
            print("execute_many:"+'-'*100)
            print(sql)
            print(e)
            self.conn.rollback()
            n = 0
            for value in values:
                if self.execute(sql, value, cursor=cursor):
                    n += 1
            return n 
        else:
            self.conn.commit()
            return len(values)
        finally:
            if not cursor:
                cursor1.close()

    def insert(self, sql_table, item):
        keys_list = list(item.keys())
        values = ', '.join(['%s']*len(keys_list))
        keys = ', '.join(keys_list)
        sql = f'INSERT INTO {sql_table} ({keys}) VALUES ({values}) '
        return self.execute(sql, tuple(item.values()))

    def insert_many(self, sql_table, items):
        if not items:
            return
        values_list = []
        keys_list = sorted(items[0])
        values = ', '.join(['%s']*len(keys_list))
        keys = ', '.join([f'"{key}"' for key in keys_list])
        for item in items:
            d = sorted(item.items(), key=lambda x:keys_list.index(x[0]))
            d = tuple([i[1] for i in d])
            values_list.append(d)
        sql = f'INSERT INTO {sql_table} ({keys}) VALUES ({values}) \
                    ON CONFLICT (key) DO NOTHING;'
        try:
            n = self.execute_many(sql, values_list)
        except Exception as e:
            traceback.print_exc()
            self.check_conn()
            return self.insert_many(sql_table, items)
        print(f'表({sql_table})插入数据库, 表：{sql_table}, 插入条数: {len(items)}，成功插入条数: {n}')
        return n
    
    def close(self):
        self.conn.close()

    