# -*- coding: utf-8 -*-

from datetime import datetime
import MySQLdb

class CalHotValue:
    def __init__(self):
        self.db = self.connect()
        self.cursor = self.db.cursor()
        self.result = self.calHotValue()

    # 连接mysql数据库
    def connect(self):
        db = MySQLdb.Connect("localhost", "root", "123456", "websitedb", charset='utf8')
        return db

    # 计算热度值
    def calHotValue(self):
        base_time = datetime.now()
        sql = "select aid, vd_cate_id, comment, likes, vd_time, play_num from videos"
        self.cursor.execute(sql)
        result_list = self.cursor.fetchall()
        result = list()

        for row in result_list:
            if (int(row[1])>2):
                hot_value = row[2] * 0.02 + row[3] * 0.05 + row[5]*0.00001
            else:
                hot_value = row[3]*0.1
            result.append((row[0],row[1],hot_value))
        print("新闻热度值计算完毕,返回结果 ...")
        return result

    # 将热度值写入数据库
    def writeToMySQL(self):
        sql = """truncate table vdhot"""
        try:
           self.cursor.execute(sql)
           self.db.commit()
           print("delete successfully!")
        except:
           self.db.rollback()
        for row in self.result:
            sql_w = "insert into vdhot( vd_id,vd_cate_id,vd_hot ) values('%s', '%s' ,'%s')" % (row[0],row[1],row[2])
            try:
                self.cursor.execute(sql_w)
                self.db.commit()
            except:
                print("rollback",row)
                self.db.rollback()
        print("热度数据写入数据库：newsrec.newhot")

if __name__ == "__main__":
    print("开始计算新闻的热度值 ...")
    chv = CalHotValue()
    chv.writeToMySQL()

