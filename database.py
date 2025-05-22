import psycopg2
from psycopg2 import sql
from psycopg2.extras import DictCursor

class Database:
    def __init__(self, dbname, user, password, host='localhost', port='5432'):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.conn.autocommit = True
    
    def execute(self, query, params=None, fetch=False):
        with self.conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(query, params)
            if fetch:
                return cursor.fetchall()
    
    def close(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
    
    def __del__(self):
        self.close()
