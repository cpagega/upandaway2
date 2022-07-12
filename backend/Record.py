import sqlite3
from datetime import datetime

class Record:
    queryParams = {}
    rows = []
    queryString = ""
    def __init__(self,tableName):
        self.tableName = tableName
        self.conn = sqlite3.connect('database.db', check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()

    def insert(self,arg):
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        itemsToInsert = [None, dt_string] + arg.split(',')
        numColumns = len(itemsToInsert)
        sql = f"INSERT INTO {self.tableName} VALUES (" + ",".join(numColumns * ["?"]) + ")"
        print(sql)
        self.cur.execute(sql, itemsToInsert)

    def addQuery(self,param,value):
        self.queryParams[param] = value

    def queryBuilder(self):
        self.queryString = f"SELECT * FROM {self.tableName} WHERE "
        for index, key in enumerate(self.queryParams):
            self.queryString += f"{key} = \'{self.queryParams[key]}\'"
            if index != len(self.queryParams) - 1:
                self.queryString += " AND WHERE "

    def query(self):
        #self.queryBuilder()
        print(self.queryString)
        #self.cur.execute(self.queryString)
        self.cur.execute(f"SELECT * FROM {self.tableName}")
        self.rows = self.cur.fetchall()

    def results(self):
        for row in self.rows:
            yield dict(row)

    def commit(self):
        self.conn.commit()

    





