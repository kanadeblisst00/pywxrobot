#-*- coding: utf-8 -*-
import sqlite3
import traceback


class SqliteDatabase:

    def __init__(self, config, create_table_sql=None, db_table=None):
        self.config = config
        self.conn = sqlite3.connect(**config)
        self.conn.row_factory = sqlite3.Row
        if create_table_sql and db_table:
            self.create_table_if_not_exists(db_table, create_table_sql)
    
    def execute(self, sql:str, value:tuple=None, cursor=None):
        try:
            cursor1 = cursor or self.conn.cursor()
            if value:
                cursor1.execute(sql, value)
            else:
                cursor1.execute(sql)
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
        cursor = self.conn.cursor()
        if self.execute(sql, value):
            for row in cursor.fetchall():
                yield dict(row)
        cursor.close()
    
    def execute_many(self, sql, values, cursor=None) -> int:
        try:
            cursor1 = cursor or self.conn.cursor()
            cursor1.executemany(sql, values)
        except Exception as e:
            print("execute_many:"+'-'*100)
            print(sql)
            print(e)
            self.conn.rollback()
            return 0
        else:
            self.conn.commit()
            return len(values)
        finally:
            if not cursor:
                cursor1.close()
    
    def create_table_if_not_exists(self, db_table, sql):
        cursor = self.conn.cursor()
        sql1 = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{db_table}';"
        self.execute(sql1, cursor=cursor)
        if cursor.fetchone():
            return
        self.execute(sql)

    def insert(self, sql_table, item):
        keys_list = list(item.keys())
        values = ', '.join(['?']*len(keys_list))
        keys = ', '.join(keys_list)
        sql = f'INSERT INTO {sql_table} ({keys}) VALUES ({values}) '
        return self.execute(sql, tuple(item.values()))

    def insert_many(self, sql_table, items):
        if not items:
            return
        values_list = []
        keys_list = sorted(items[0])
        values = ', '.join(['?']*len(keys_list))
        keys = ', '.join([f'"{key}"' for key in keys_list])
        for item in items:
            d = sorted(item.items(), key=lambda x:keys_list.index(x[0]))
            d = tuple([i[1] for i in d])
            values_list.append(d)
        sql = f'INSERT INTO {sql_table} ({keys}) VALUES ({values});'
        try:
            n = self.execute_many(sql, values_list)
        except Exception:
            traceback.print_exc()
            return 0
        return n
    
    def close(self):
        self.conn.close()

    